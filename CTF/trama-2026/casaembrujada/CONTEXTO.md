# Desafío 02 — La Mansión Blackwood

| Campo | Valor |
|---|---|
| Categoría | MISC / esteganografía en imagen (LSB) |
| Enunciado afirma | «interferencia digital estática en ciertas áreas» + «huella digital que los métodos de análisis estándar no detectan» |
| Estado | ✅ Resuelto |
| Evidencia | `casaembrujada.png` — 481.081 B, 400×400, 8-bit RGB, no entrelazado |
| SHA256 | `12b4f39ab4cdfda3a77d79c570ddaa49563340830b97abe6e81d8968a1118aa4` |

## Flag

```
flag{ejemplo}
```

## Enunciado (resumen)

Investigadores paranormales fotografían la fachada de la Mansión Blackwood. En la imagen
hay «interferencia digital estática» en ciertas zonas, pero ningún fantasma visible. La
actividad paranormal dejó una huella «que los métodos de análisis estándar no detectan».
Hay que desenterrar la bandera.

## Reconocimiento

```bash
$ file casaembrujada.png
PNG image data, 400 x 400, 8-bit/color RGB, non-interlaced

$ exiftool casaembrujada.png
# solo metadatos básicos del PNG: sin comentarios, sin campos EXIF/XMP, sin Software

$ binwalk casaembrujada.png
# solo "PNG image" + "Zlib compressed data" (los IDAT normales)

$ pngcheck -v casaembrujada.png
# estructura correcta, sin chunks extra ni datos después del IEND

$ strings -n 8 casaembrujada.png
# ruido de compresión, ninguna cadena legible
```

Descartado en 1 minuto: metadatos, chunks PNG extra (tEXt/zTXt/iTXt), archivos embebidos
después del IEND, y texto en `strings`. Es decir, **el mensaje está dentro de los píxeles**.

## Análisis

La pista «estática / interferencia» apunta a manipulación de bits de bajo peso: si se
oculta información en el bit menos significativo (LSB) de cada canal, el ojo solo percibe
un ruido sutil — exactamente «estática digital».

Comprobación estadística sobre los tres canales:

```
canal R: LSB media = 0.4995
canal G: LSB media = 0.4999
canal B: LSB media = 0.4996
```

Un 0.5 casi perfecto = los LSB son prácticamente aleatorios (en una foto normal suelen
estar sesgados hacia el valor real del píxel). Señal clásica de **payload LSB**.

Visualización de los planos (`work/plane_*_bit*.png`): los planos de bit 0 no muestran
figura reconocible, solo estática → el payload está al principio del stream, no dibujado
en una región.

## Solución (pasos reproducibles)

### Script (guardado en `solucion/lsb_extract.py`)

```python
import re
import numpy as np
from PIL import Image

arr = np.array(Image.open("casaembrujada.png").convert("RGB"))
# aplanar en orden: píxel 0 (R,G,B), píxel 1 (R,G,B)... fila a fila
bits = ((arr.reshape(-1) >> 0) & 1).astype(np.uint8)
data = np.packbits(bits).tobytes()          # 8 bits -> 1 byte, MSB primero
print(re.match(rb"[\x20-\x7e]{4,}", data).group(0).decode())
```

Ejecución:

```bash
python3 solucion/lsb_extract.py casaembrujada.png 0
# [+] bit LSB = 0
# [+] mensaje: flag{ejemplo}
```

### Alternativa con herramientas

```bash
# zsteg prueba automáticamente todas las combinaciones (necesita: gem install zsteg)
zsteg -a casaembrujada.png | grep -i trama

# o con steghide/stegsolve para inspección visual, o:
python3 -c "from PIL import Image; ..."   # equivalente al script de arriba
```

En Windows también sirve abrir la imagen en **StegSolve** → *Data Extract* → Bit 0, orden
RGB, y ver el texto en la vista *Text*.

## Explicación técnica

- PNG 400×400×3 canales = 480.000 bits de capacidad en el bit 0.
- El mensaje ocupa los primeros **38 bytes = 304 bits**, es decir, los LSB del píxel 0
  en adelante (R=bit0 del byte 0, G=bit0 del byte 1, B=bit0 del byte 2, y así).
- Los bytes se empaquetan MSB-first: `np.packbits` por defecto respeta ese orden.
- Tras los 38 bytes el stream sigue siendo ruido de la foto (de ahí que no hubiera más
  texto y que un `strings` sobre el archivo crudo nunca lo revelara: el mensaje nunca
  existe como bytes contiguos en el PNG, solo como bits de color).

## Lecciones / notas

- Ante una imagen y la palabra «estática», «ruido» o «invisible»: **probar LSB primero**.
- `binwalk`/`foremost`/`strings` fallan por diseño en LSB: el payload no está en el
  contenedor, está codificado en el dominio del color.
- La prueba de fuego es la **entropía del LSB** (media ≈ 0.5) y el plano de bits.
- Orden de lectura: probar píxel-interleaved (RGB,RGB…) antes que plano-por-canal
  (RRR…GGG…BBB…); en este reto solo funciona el primero desde el offset 0.
- La flag: *«Me dan miedo los fantasmas»*, con `$` en lugar de `s` (leetspeak).

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `casaembrujada.png` | evidencia original |
| `flag.txt` | flag extraída |
| `CONTEXTO.md` | este writeup |
| `solucion/lsb_extract.py` | extractor LSB parametrizable (bit 0–7) |
| `solucion/salida.txt` | salida de la ejecución |
| `work/plane_<canal>_bit<0-2>.png` | planos de bits para inspección visual |
