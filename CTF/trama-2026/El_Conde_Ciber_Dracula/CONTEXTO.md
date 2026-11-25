# Desafío 12 — El Conde Ciber-Drácula

| Campo | Valor |
|---|---|
| Categoría | OSINT + forense de video (stream en vivo, metadatos de hora, OCR de frames) |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |
| Charla | «El lado oscuro de la IA: cómo los atacantes ya usan IA contra personas y empresas en Chile» — **Daniela Inostroza Mancilla**, 23 OCT 2026, 18:00–18:45 (Chile) |

## Flag

```
flag{ejemplo}
```

*«Las señales ya no existen»* — coherente con el cierre del evento («La señal se cierra
pronto. Entra en la trama…»).

## Enunciado (resumen)

El Conde se infiltró en una conferencia de ciberseguridad y alteró la presentación de una
expositora. Durante la transmisión mostró la flag **dividida en tres partes, cada una en
Base64**. Hay que encontrar el video por OSINT y unir los fragmentos.

## OSINT: ubicar la transmisión

1. **Programa oficial** — `www.nodotrama.cl` publica la parrilla: la charla con ese título
   exacto es de **Daniela Inostroza Mancilla**, **23 OCT 2026 18:00–18:45**.
2. **Canal** — `@NodoTramaOficial` (`UCB5UNOX9_1HpgufdG0uTNzQ`).
   - `cKONzqyGMnk` — *¡TRAMA CTF 2026 HA COMENZADO!* — 12:51Z–16:58Z (jornada mañana).
   - **`GXwU585x0HA` — *NodoTrama CTF - Dia 1 - Jornada Tarde*** — inicio `2026-10-23T18:49:22Z`
     (15:49 Chile). La charla cae en el **offset 131–176 min** de este stream.
3. El stream estaba **en vivo** al momento del reto (21:00–21:45Z = 18:00–18:45 Chile).

## El hallazgo: los fragmentos están en la esquina del slide

En el frame del inicio de la charla (`sq 3922`, ≈21:00Z) se ve, abajo a la derecha de la
presentación, una marca en fuente monoespaciada verde tenue:

```
VFJBTUFDVEZ7bDRz      ->  TRAMACTF{l4s
```

Los otros dos aparecen en slides posteriores:

| # | sq (segmento) | Hora aprox. (Chile) | Marca en el slide | Decodifica a |
|---|---|---|---|---|
| 1 | 3910–3944 | 18:00 | `VFJBTUFDVEZ7bDRz` | `TRAMACTF{l4s` |
| 2 | 4152–4170 | ≈18:08 | `X3MzbjRsM3NfeTRf` | `_s3n4l3s_y4_` |
| 3 | 4244–4356 | ≈18:12 | `bjBfM3gxc3Qzbn0=` | `n0_3x1st3n}` |

Concatenación: `flag{ejemplo}`

## Solución (pasos reproducibles)

### 1. Obtener la URL del stream en vivo

```bash
yt-dlp -F "https://www.youtube.com/watch?v=GXwU585x0HA"        # ver formatos
yt-dlp -f 232 -g "https://www.youtube.com/watch?v=GXwU585x0HA" > hls_720.txt
```

### 2. Retroceder en el DVR (el truco del reto)

El manifiesto HLS es una **ventana deslizante de 15 min** (450 segmentos de 2 s,
`#EXT-X-MEDIA-SEQUENCE` y `#EXT-X-PROGRAM-DATE-TIME`). `ffmpeg -ss` **no** puede ir más
atrás, pero los segmentos son direccionables por número de secuencia:

```bash
URL=$(head -1 hls_720.txt)
curl -s "$URL" -o pl.m3u8                     # refrescar firma
SEG=$(grep -m1 '^https' pl.m3u8)
BASE=$(grep -oE '/sq/[0-9]+/' pl.m3u8 | head -1 | tr -dc '0-9')

# pedir un segmento antiguo cambiando /sq/BASE/ por /sq/N/
curl -s "$(echo "$SEG" | sed "s#/sq/${BASE}/#/sq/3922/#")" -o seg.ts
ffmpeg -i seg.ts -frames:v 1 -update 1 frame.png
```

Mapeo temporal: `t(sq) = PROGRAM_DATE_TIME + (sq - MEDIA_SEQUENCE) × 2 s`.
Con base `sq 4333 = 21:13:42Z`, `sq 3922 ≈ 21:00:00Z` = inicio de la charla.

### 3. Barrido y extracción de la marca

```bash
# 1 frame cada 20 s a lo largo de la charla (sq 3400 → 5250)
bash solucion/barrido_dvr.sh 10 3400 5250

# recorte de la esquina + canal verde + OCR (psm 7, whitelist base64)
python3 solucion/extraer_marcas.py
```

`solucion/extraer_marcas.py` hace por cada frame:

```python
g = img.crop((1040, 624, 1268, 654)).split()[1]   # canal VERDE (texto verde sobre negro)
g = ImageOps.autocontrast(g).resize((g.width*10, g.height*10), Image.LANCZOS)
# tesseract --psm 7 -c tessedit_char_whitelist=<A-Za-z0-9+/=>
```

### 4. Decodificar

```python
import base64
frags = ["VFJBTUFDVEZ7bDRz", "X3MzbjRsM3NfeTRf", "bjBfM3gxc3Qzbn0="]
print("".join(base64.b64decode(f).decode() for f in frags))
# flag{ejemplo}
```

## Notas técnicas (lo que costó)

- **No hay subtítulos**: el stream no expone `captionTracks` ni `timedtext` (0 bytes). Todo
  hay que sacarlo de los píxeles.
- **El OCR genérico falla**: la marca mide ~8 px de alto y es verde tenue. Funciona solo
  con *canal verde + autocontraste + ×10 + psm 7 + whitelist*. Aun así confunde `D↔0`,
  `B↔8`, `b↔6`; la validación final es **semántica**: `bDRz→l4s` encaja con
  `s3n4l3s` (femenino), mientras que `b0Rz→oDs` no significa nada.
- **El crop debe ser ancho**: la marca puede tener 16–20 caracteres y se corre hacia la
  izquierda; una caja estrecha la trunca (fue el primer error).
- Los tres fragmentos están separados en el tiempo (~18:00, 18:08 y 18:12), no seguidos.
- Alternativa más lenta pero segura: `yt-dlp --live-from-start -f 135` descarga el stream
  completo desde el inicio (DASH), evitando el límite de 15 min del DVR.

## Resultado

```
flag{ejemplo}
```

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag final |
| `solucion/barrido_dvr.sh` | barrido de segmentos DVR + extracción de frames |
| `solucion/extraer_marcas.py` | recorte de la marca (canal verde) + OCR + agrupación |
| `solucion/extraer_marca.py` | recorte simple de la marca (una carpeta) |
| `solucion/recortar_esquina.py` | recorte de esquina con autocontraste |
| `solucion/buscar_fragmentos.py` | heurística de detección de Base64 en OCR |
| `work/dvr/` | 334 frames del stream (sq 3400–5250) |
| `work/lecturas_ocr.tsv` | OCR por frame |
| `work/LEER_3922.png`, `LEER_4160.png`, `LEER_4320.png` | recortes ampliados de los 3 fragmentos |
| `work/hls_720.txt`, `work/pl.m3u8` | manifiesto HLS y playlist usados |
