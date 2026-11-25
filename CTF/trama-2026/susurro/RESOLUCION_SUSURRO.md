# El Susurro del Conde — investigación parcial (histórico)

**Fecha:** 2026-10-24
**Archivo:** `ChismeAudio.wav` (640.044 B, SHA-256 `7CCD2A904E21D3AF1C09F3C31CF526CFD6700D99246559B0BE91551A77896011`)
**Estado:** ✅ **resuelto** — ver [CONTEXTO.md](CONTEXTO.md) para la resolución final.

> Este documento conserva el análisis que llevó al primer secreto (texto del espectrograma).
> El cierre está en `CONTEXTO.md`: el bit 0 de las muestras contenía un blob Base64 y la
> llave correcta era `SweetBl00d`, no `SweetBlood`.
>
> **Flag:** `flag{ejemplo}`

---

## 1. Contenedor (descartado)

| Comprobación | Resultado |
|---|---|
| Estructura | RIFF / `fmt ` (16 B) + `data` (640.000 B) = 44 + 640000 exacto → **sin chunks extra ni datos anexados** |
| Formato | PCM 16 bits, **mono, 44100 Hz**, 320.000 muestras, 7,256 s |
| `exiftool` | sin metadatos útiles |
| `binwalk` / `strings` | nada |
| **steghide** | soporta el WAV: `info` muestra solo `format` y `capacity: 19.5 KB`, **sin bloque `embedded data`** → no hay contenedor steghide. Probadas 28 passphrases → ninguna extrae |
| LSB (bits 0-3, intro/cuerpo/cola, MSB y LSB-first, con y sin XOR SHA-256) | p1≈0,49, transiciones≈0,52 → **ruido de cuantización, sin payload** |

## 2. Estructura de la señal

- Peine armónico con **F0 = 110,25 Hz** (= 44100/400 → periodo exacto de 400 muestras; sintetizador granular/armónico).
- Armónicos hasta 22 kHz; el "zumbido monótono" del enunciado.
- **Envolvente (umbral 2 % del máximo): 14 ráfagas** = 14 caracteres:

| # | inicio (s) | dur (s) | hueco previo (ms) |
|---|---|---|---|
| 1 | 0,569 | 0,249 | — |
| 2 | 0,851 | 0,212 | 33 |
| 3 | 1,087 | 0,276 | 24 |
| 4 | 1,458 | 0,076 | 96 |
| — | — | — | **404 (espacio)** |
| 5 | 1,939 | 0,221 | |
| 6 | 2,184 | 0,275 | 24 |
| 7 | 2,474 | 0,240 | 15 |
| 8 | 2,746 | 0,240 | 33 |
| 9 | 3,028 | 0,212 | 42 |
| 10 | 3,300 | 0,230 | 60 |
| 11 | 3,563 | 0,230 | 33 |
| 12 | 3,844 | 0,221 | 51 |
| 13 | 4,116 | 0,221 | 51 |
| 14 | 4,388 | 0,221 | 51 |

Total ON: 3,13 s.

## 3. Primer secreto («para los ojos») — RESUELTO

Texto dibujado en el espectrograma en la banda **2,4-4,1 kHz**, implementado como modulación de amplitud del peine armónico (por eso los renders genéricos salen con estrías).

- Render 1:1 (`out/band_1to1.png`) y tiras por glifo (`out/strip.png`, `out/g_0_3.png`, `out/g_4_7.png`, `out/g_8_13.png`, `out/strip_low.png`) permiten leer:

```
KEY: SweetBlood
```

- Verificación cruzada: los glifos 7/8 (posiciones 3 y 4 de la palabra) son **idénticos** entre sí, igual que 11/12 → confirma la estructura `?ee?` y `?oo?` de **S·w·e·e·t·B·l·o·o·d**.
- `:` = ráfaga corta de 76 ms tras un hueco de 96 ms; el espacio = 404 ms.

**Llave candidata: `SweetBlood`** (variantes probadas: `SweetBl00d`, `SweetBL00D`, `SweetBlood1810`, `KEY: SweetBlood`, mayúsculas/minúsculas…).

## 4. Zonas verificadas como vacías

- **Cola 4,61-7,26 s**: tono de ~100 Hz a −43 dB; ampliada ×200 no aparece nada (`out/tail_amp.png`).
- **Intro 0-0,569 s**: fade-in del mismo tono (`out/intro_amp.png`).
- **Banda alta 5-22 kHz**: réplica del mismo patrón (armónicos), sin FSK/SSTV/texto distinto (`out/hi_5_22k.png`, `hi_12_22k.png`).
- **Residuo inter-armónico** (filtro mediana 9 bins a 5,38 Hz/bin): solo los trazos del texto, **nada entre armónicos** (`out/resid.png`) → no hay voz ni datos ocultos bajo el peine.
- **Rotaciones 90°/270°** del espectrograma: sin texto.

## 5. Pendiente

1. Confirmar la transcripción exacta glifo a glifo (mayúsculas/`l` vs `I`/`0` vs `o`) con `out/g_8_13.png`.
2. Probar la llave en herramientas de esteganografía con contraseña sobre WAV: **DeepSound** (Windows), **OpenPuff**, `steghide` (ya descartado como contenedor).
3. Probar descifrado simétrico del tramo 0,569-4,609 s con la llave (AES-256-CBC/CTR con IV nulo o derivado, RC4, XOR con SHA-256), sobre muestras PCM o sobre la matriz de amplitudes armónicas.
4. Revisar si el «secreto para los oídos» es el propio ritmo/melodía de las 14 ráfagas (Morse/Baudot sobre duraciones y huecos).
5. Al obtener la flag: crear `flag.txt`, mover scripts a `solucion/`, y cerrar este contexto.

## 6. Artefactos

- Scripts (en `%TEMP%\opencode\susurro\`): `a1-a4.sh`, `an1-an18.py`, `asc1-asc10.py`, `letters.py`, `strip.py`, `strip2.py`, `glyphs.py`, `lsb_scan.py`, `tail.py`, `lowband.py`, `steghide_brute.sh`.
- Imágenes en `%TEMP%\opencode\susurro\out\` (más de 30, ver §3-§4).
- Copia de scripts y artefactos relevantes en `scripts/` de esta carpeta.
