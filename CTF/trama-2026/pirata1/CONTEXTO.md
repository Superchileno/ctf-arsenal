# Pirata 1 — El capitán que debía hasta el café (DG-003)

| Campo | Valor |
|---|---|
| Categoría | Esteganografía de audio — LSB del PCM + zlib |
| Evidencia | `Pirata_1.zip` (22 764 882 B) → `senal_malapata.wav` (26 604 452 B) |
| SHA-256 ZIP | `4159c8a65a223043e354d30c068b547fcfcead47ab2e909e7589359d592b954f` |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |
| Dato de navegación | **`19.914434`** (DG-003) |

## Enunciado (resumen)

Tras el desastre de los respaldos aparece un audio vinculado al capitán **Malapata**.
El operador que lo escuchó dictaminó: *«Suena a audio común y corriente. Si hay un
mensaje, debe venir de polizón»*. La jefatura quiso archivar («no armen otro cahuín
por un pirata»). Hay que recuperar el mensaje escondido y, si aparece, el dato de
navegación.

## El artefacto

```
senal_malapata.wav — RIFF WAVE PCM 16 bit, mono, 44 100 Hz, 301,6 s
chunks: fmt  |  LIST (IART=Mumablue, IGNR=Podcast, INAM=El pirata Malapata,
                      IPRD=Pequehistorias, ISFT=Lavf58.76.100)  |  data
```
Es un podcast real (*Pequehistorias*), reconvertido a WAV con ffmpeg: la pista de que
el autor lo pasó por PCM de 16 bits para poder esconder bits en el LSB.

## Vectores descartados (por orden)

| Vector | Resultado |
|---|---|
| Datos anexados / polyglot / cola tras el ZIP | ❌ |
| Espectrograma (0–22 kHz, lin/log/cbrt; bandas 5–9 kHz; normalizado por bin) | ❌ solo voz/música |
| Detector DTMF (Goertzel, 51 957 tramas) y multimon-ng (POCSAG, AFSK, Morse, EAS…) | ❌ |
| Tonos persistentes (pico vs. fondo local) | ❌ |
| steghide (sin passphrase y 10 típicas) | ❌ |
| Estéreo oculto (pares/impares) | ❌ correlación 0,977 (mono real) |
| Submuestreo `x[::N]`, 2 bits/muestra, bytes pares/impares, texto invertido | ❌ |
| ASR (faster-whisper) del audio normal y al revés | ❌ solo el cuento |

## El hallazgo

Al volcar el **bit 0 de cada muestra** (MSB-first, 8 bits por byte) la secuencia no
era ruido: empezaba con una cabecera propia.

```
44 47 4c 44 | 00 00 01 16 | 78 da ...
"DGLD"        278 (BE)      zlib
```

Contenedor: `"DGLD"` + longitud (4 B big-endian) + **zlib(deflate)** con el texto.

### Solución

```python
import wave, zlib, struct, numpy as np
x = np.frombuffer(wave.open("senal_malapata.wav").readframes(10**9), dtype="<i2")
bits = (x & 1).astype(np.uint8)
b = (bits[:len(bits)//8*8].reshape(-1, 8) * (1 << np.arange(7, -1, -1))).sum(axis=1).astype(np.uint8).tobytes()
assert b[:4] == b"DGLD"
largo = struct.unpack(">I", b[4:8])[0]
print(zlib.decompress(b[8:8+largo]).decode())
```

### Mensaje

```
DOL GULDUR — BITACORA RECUPERADA / DG-003

El capitan Malapata declaro que su botin era patrimonio historico.
Contabilidad respondio que igual tenia que rendir los gastos.

MENSAJE INTERCEPTADO:
flag{ejemplo}

ANOTACION DE NAVEGACION (no desechar):
19.914434,

PD: Si preguntan por el cafe, yo no fui.
```

## Flag

```
flag{ejemplo}
```

## Dato para Pirata 3

```
DG-003 → 19.914434   (con coma final: primer pedazo del rumbo)
```

## Por qué fallaban los análisis previos

- El mensaje **no está en texto plano** en el LSB: va **comprimido con zlib** dentro de
  un contenedor con magic `DGLD`. Buscar `TRAMACTF` en los bytes empaquetados no lo
  encuentra (fue el error de la primera pasada).
- El audio es un podcast real: cualquier análisis espectral muestra voz y música
  normales; el payload no toca el dominio de la frecuencia.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `Pirata_1.zip` | evidencia original |
| `flag.txt` | flag final |
| `CONTEXTO.md` | este writeup |
| `solucion/contenedor.py` | ⭐ extrae el contenedor `DGLD` del LSB y descomprime |
| `solucion/lsb_codecs.py` | volcado de flujos LSB y prueba de códecs |
| `solucion/barrido_wav.py`, `barrido2.py`, `bits.py`, `submuestreo.py`, `intercalado.py`, `chunks.py`, `espectro.py`, `espectro_norm.py`, `tonos.py`, `dtmf.py`, `asr.py` | análisis previos (descartados) |
| `work/` | WAV, `contenedor_lsb.bin`, espectrogramas y `esp/*.png` |
