# ANCI — Reto "Discodroid" / kernel pwn (HackRocks)

**Paquete:** `discodroid.zip` → `Image`, `rootfs.cpio`, `patch.diff`, `run.sh`
**Servicio:** `nc <host> 28808` (consola serie de un QEMU)
**Flag:** `flag{ejemplo}`
**Estado:** ✅ RESUELTO (2026-10-29)

---

## 1. Entorno

`run.sh` arranca QEMU con:

```
-cpu qemu64,+smep,+smap -m 256M -kernel Image -initrd rootfs.cpio
-drive file=flag.txt ... -snapshot -nographic -smp 2 -nic none
-append "rdinit=/init console=ttyS0 kaslr pti=on loglevel=0 oops=panic panic=-1"
```

`init` (initramfs) copia `/dev/vda` (el disco con el flag) a
`/root/flag-<md5>.txt` (chmod 700), hace `chmod 000 /dev/vda` y lanza
`setsid cttyhack su -s /bin/sh nonroot`. Nosotros entramos como `nonroot`
(uid 1000), sin binarios SUID y con `/root` inaccesible.

Kernel: **7.2.2** (build custom, clang 21, `PREEMPT_DYNAMIC`, x86-64).

## 2. Análisis de la vulnerabilidad

`patch.diff` elimina en `fs/splice.c` el `pipe_buf_get()` de la ruta de
transferencia **parcial** entre dos tuberías. Se verificó en el `Image`
descomprimido (`vmlinux-to-elf` + objdump):

- `do_splice` (con `splice_pipe_to_pipe` inlineado) **sí conserva** la llamada
  `ops->get` en la ruta parcial (por eso `splice()` no era explotable).
- En cambio, `do_tee` (con `link_pipe` inlineado) **copia el `pipe_buffer` sin
  llamar a `ops->get`**:

```
mov 0x18(ibuf),%r9    ; flags
mov %r9,0x18(obuf)
mov (ibuf),%r10       ; page
mov 0x10(ibuf),%rdi   ; ops
mov %r10,(obuf)       ; page copiada SIN get_page()
and $0xeb,%r9b        ; limpia CAN_MERGE
```

Esto coincide con la pista: *"tee puede dejar una referencia a una página de
canalización que perdure más allá de la ruta de cierre"*.

### Primera dificultad: reciclado de páginas de tubería

`anon_pipe_buf_release()` en este kernel **no libera** la página si el
`refcount == 1` y la tubería tiene un slot `tmp_page` libre: la guarda para
reutilizarla. Para forzar la liberación real hay que **cerrar la tubería**:
`free_pipe_info()` libera también `tmp_page` → la página vuelve al buddy.

Comprobación (`diag4.c`): tras `tee()` + `close()` de la tubería origen, una
escritura en otra tubería reutiliza la página (el clon de `tee` lee `'Z'`).

## 3. Exploit: Dirty Pagetable

1. `pipe(A)`, escribir 1 página → página anónima **P** (migratetype unmovable:
   las páginas de tubería usan `GFP_HIGHUSER`, no `MOVABLE`).
2. `tee(A[0] → B[1], 4096)` → clon en B **sin referencia** a P.
3. `close(A[0]); close(A[1])` → `free_pipe_info` libera P; B sigue apuntando a P.
4. Tocar una página de un chunk de 2 MB nuevo (`c1`) → la **página de tablas de
   páginas (PTE)** de ese chunk se asigna con P (mismo migratetype, PCP LIFO).
5. `read(B[0])` → `put_page(P)` libera la página **que sigue instalada como
   PTE page** (UAF de tabla de páginas).
6. Reclamar P como página de una tubería `C` (mismo migratetype) escribiendo
   las PTEs que queramos. `C` conserva P en `tmp_page`, por lo que
   `read(C[0])` + `write(C[1])` permite **reescribir las PTEs** por lotes.
7. `mprotect()` sobre el chunk fuerza el flush de TLB y se lee memoria física
   mapeando PFN tras PFN.

Exploit funcional: `wee6.c` (freestanding, ~9 KB, subido por la consola en
base64). Mapea PFN 0..0xFFFF (256 MiB), salta el hueco MMIO 0xA0–0xFF, y busca
`flag{` al inicio de cada página.

Resultado:

```
FOUND pfn=ffbe
flag{ejemplo}
```

(`pfn=0xFFBE` ≈ 255,9 MiB: página de page-cache del flag, en la parte alta de
la RAM.)

## 4. Cadena resumida

```
tee() sin get_page  →  close(origen) libera la página
  →  la página se reasigna como PTE page
  →  drenar el clon libera la PTE page (UAF)
  →  reclamar como página de tubería controlada
  →  PTEs arbitrarias  →  leer memoria física  →  flag
```

## 5. Artefactos

| Archivo | Descripción |
|---|---|
| `Image`, `rootfs.cpio`, `run.sh`, `patch.diff` | Paquete original |
| `extract.sh`, `sym.sh`, `tee2.sh` | Extracción de vmlinux y análisis de `do_tee` |
| `diag3.c`, `diag4.c` | Pruebas del UAF (drain vs. close) |
| `wee2.c`–`wee6.c` | Iteraciones del Dirty Pagetable |
| `wee6` / `wee6.b64` | Exploit final y su base64 |
| `run_exploit.py`, `upload_run.py` | Subida e interacción por la consola |

## 6. Remediación (contexto real)

- Restaurar `pipe_buf_get()` en `link_pipe()` (tee) y en todas las rutas de
  clonado de `pipe_buffer`; el callback `.get` debe tomar la referencia de la
  página *antes* de copiar la estructura.
- Añadir pruebas de regresión con `tee()` + `close()` y `splice()` parciales
  bajo KASAN.
- Mitigaciones de kernel: `CONFIG_DEBUG_VM`/KASAN, `init_on_free`,
  `page_alloc.shuffle=1`, y no exponer kernels heredados sin mantenimiento.
- El flag no debería depender solo de permisos de archivo dentro del guest:
  usar un TPM/attestation o un servicio externo de entrega.
