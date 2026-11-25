# ANCI — CTF "Sigcall"

**Evento:** CTF ANCI — reto de análisis de binario / pwn
**Nombre interno:** Sigcall
**Servicio:** `nc <host> 28807`
**Formato de flag:** `flag{..}`
**Objetivo:** analizar el binario provisto, entender el servicio y superar sus
protecciones para leer el token almacenado en el sistema.
**Fecha de registro:** 2026-10-29
**Estado:** ✅ **RESUELTO** — flag: `flag{ejemplo}`

> Writeup completo en [`RESOLUCION.md`](RESOLUCION.md). Artefacto provisto: `rop.txt`.

---

## Enunciado

> Durante una revisión de seguridad de la infraestructura tecnológica de una
> institución, el equipo de operaciones identificó un servicio denominado
> Sigcall, que permanece escuchando conexiones de red y cuyo funcionamiento
> interno no ha sido completamente documentado.
>
> Aunque inicialmente parece tratarse de una herramienta inofensiva, existen
> sospechas de que su interacción con el sistema operativo podría exponer
> recursos protegidos a usuarios no autorizados.
>
> Este escenario representa un riesgo presente en infraestructuras
> institucionales: la existencia de servicios expuestos que, al interactuar con
> componentes privilegiados del sistema operativo, podrían facilitar la
> explotación de vulnerabilidades y comprometer la seguridad del servidor.
>
> Tu misión consiste en analizar el Archivo proporcionado, investigar el
> funcionamiento del servicio y determinar si es posible superar sus mecanismos
> de protección para recuperar el token almacenado en el sistema.

---

## Reconocimiento del servicio (black-box)

`<host>` → `203.0.113.10`, puerto `28807/TCP` abierto.

Secuencia observada:

```
$ nc <host> 28807
gimme:
<stdin>              <- el servicio lee datos del socket
\n                   <- imprime un salto de linea y termina
```

- El banner es exactamente `gimme:\n` (7 bytes).
- Tras enviar cualquier entrada, el programa imprime `\n` y cierra la conexión.
- No hay eco de la entrada ni salida de comandos: `hello`, `%p`, `%s`, `%n`,
  `id`, `env`, `cat /flag.txt`, etc. producen lo mismo (solo `\n`).
- No responde a números de señal (`0..64`, `SIG*`): **no** hace `raise(atoi())`.
- La conexión se mantiene abierta si no se envían datos (no hay timeout de app).

### Desbordamiento de pila

Al enviar entradas largas el proceso muere y el shell del servicio lo reporta
por el propio socket:

```
/home/ctf/run: line 2: <pid> Segmentation fault (core dumped) ./vuln
```

Esto revela además:

- El servicio ejecuta un script `/home/ctf/run` cuya línea 2 lanza `./vuln`.
- El binario se llama `vuln` y corre como usuario `ctf` en `/home/ctf`.
- `stderr` del proceso llega al socket (mensajes de bash).

Barrido de longitudes (byte `A`):

| Bytes enviados | Resultado |
|---|---|
| 16 – 136 | termina normal (solo `\n`) |
| 140 – 300 | **Segmentation fault** (core dumped) |

→ Umbral entre **136 y 140** bytes. Compatible con `char buf[128]` + 8 bytes de
`rbp` guardado: **offset hasta RIP = 136**. (Sin canary: no aparece
"stack smashing detected"; probablemente `-fno-stack-protector`.)

## Análisis del binario (confirmado)

Con `rop.txt` y el binario `vuln` descargado del contenedor:

- ELF 64-bit x86-64, **no PIE** (base `0x400000`), **NX**, **sin canary**, Partial RELRO.
- `main` (0x4011f5): buffer `[rbp-0x80]` (128 B) y `read(0, buf, 0x200)` →
  **offset hasta RIP = 136**, payload máximo 512 bytes.
- `0x401161` es `syscall ; ret` (el listado no mostraba el `ret`).
- No hay función "win" ni `system`/`execve` importados.

## Explotación (resumen)

**SROP**: se escribe `"/bin/sh\0"` en `0x404028` con `mov [rdi], r9`, se hace
`rt_sigreturn` (rax=15) y el frame ejecuta `execve("/bin/sh", {NULL}, NULL)`.
Payload de 472 bytes → shell como `ctf`. La flag está en
`/home/ctf/flag.txt` (no en `/flag.txt`).

Resultado: **`flag{ejemplo}`** — ver `RESOLUCION.md` y `exploit.py`.

## Archivos de la carpeta

- `CONTEXTO.md` — este documento.
- `RESOLUCION.md` — writeup completo (análisis, SROP, remediación).
- `rop.txt` — artefacto provisto (gadgets).
- `exploit.py` — exploit final reproducible (472 B, SROP).
- `srop_shell.py` — primera versión (528 B; funcionó por el truncamiento a 512).
- `enum_ctf.py` — reconocimiento dentro del contenedor.
- `download.py` — descarga `vuln`/`run` vía base64.
- `vuln`, `run.sh` — binario y wrapper obtenidos del servicio.
- `probe2.py`, `scan.py`, `candidates.py`, `sigtest.py` — sondeo black-box inicial.

## Autorización

Reto CTF de HackRocks/ANCI. Pruebas limitadas al host y puerto indicados.
