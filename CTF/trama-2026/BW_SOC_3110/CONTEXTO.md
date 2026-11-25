# Desafío 03 — Señal desde Blackwood (BW_SOC_3110)

| Campo | Valor |
|---|---|
| Categoría | MISC / forense de archivos (datos anexados a imagen · file carving) |
| Enunciado afirma | imagen «que pesa varios megabytes más de lo que sus dimensiones deberían permitir» |
| Estado | ✅ Resuelto |
| Evidencia | `BW_SOC_3110.png` — 4.389 B, PNG 600×400, 8-bit RGB, no entrelazado |
| SHA256 | `85910bf4a5af373f9035840a8606415bd336d5bf38f9778eb5fb92720f2f61da` |

## Flag

```
flag{ejemplo}
```

Nota encontrada junto a la flag: *«Enhorabuena, has mirado debajo de la alfombra.»*

## Enunciado (resumen)

El SOC detecta una transmisión desde un servidor abandonado del pabellón psiquiátrico de
Blackwood Estate: **una sola imagen** oscura y borrosa. En los registros de red el archivo
pesa «varios megabytes más de lo que sus dimensiones deberían permitir». Hay que auditar la
imagen, ignorar la ilusión visual y sacar el mensaje oculto. Habla de transmisiones de bajo
ancho de banda con mensajes «prohibidos».

## Reconocimiento

```bash
$ ls -l BW_SOC_3110.png
-rwxrwxrwx 1 lmiranda lmiranda 4389 ... BW_SOC_3110.png     # 4,4 kB, no MB

$ file BW_SOC_3110.png
PNG image data, 600 x 400, 8-bit/color RGB, non-interlaced

$ exiftool BW_SOC_3110.png
...
Warning : [minor] Trailer data after PNG IEND chunk      # <-- AQUÍ está el hallazgo

$ binwalk BW_SOC_3110.png
0     0x0     PNG image, 600 x 400, 8-bit/color RGB
41    0x29    Zlib compressed data, default compression
4098  0x1002  Zip archive data, ... name: flag.txt
4175  0x104F  Zip archive data, ... name: nota.txt
4367  0x110F  End of Zip archive, footer length: 22
```

La pista «pesa más de lo que debería» se confirmó en el **trailer**: `exiftool` avisa de
datos después del `IEND` y `binwalk` encuentra un **ZIP completo** embebido a partir del
byte 4098. 4098 es exactamente donde termina el PNG.

## Análisis

```
[ PNG: signature + IHDR + IDAT + ... + IEND ]  bytes 0        .. 4097
[ ZIP anexado: PK\x03\x04 ... EOCD          ]  bytes 4098     .. 4388
```

Detalle técnico que hace perder tiempo si se calcula mal el corte: el chunk `IEND` ocupa
**12 bytes** = longitud (4) + tipo `"IEND"` (4) + CRC (4). `data.find(b"IEND")` devuelve el
offset del **tipo** (4090), así que el final real es `iend + 8 = 4098`, no `iend + 12`.
Cortar 4 bytes tarde rompe el ZIP («missing 77 bytes in zipfile» / «overlapped
components»).

No había nada en el dominio de los píxeles (la imagen es una foto oscura legítima): el
secreto estaba **fuera** del flujo de imagen, en el contenedor.

## Solución (pasos reproducibles)

### Script (guardado en `solucion/carve_trailer.py`)

```python
data = open("BW_SOC_3110.png", "rb").read()
fin_png = data.find(b"IEND") + 8            # tipo 4 + CRC 4
extra = data[fin_png:]                      # 291 bytes anexados
z = extra.find(b"PK\x03\x04")               # firma de ZIP
open("embed.zip", "wb").write(extra[z:])
```

```bash
$ python3 solucion/carve_trailer.py BW_SOC_3110.png
[i] PNG válido hasta el byte 4098
[i] tamaño total 4389 -> 291 bytes anexados tras el IEND
[i] firma ZIP en offset 0 del trailer
[+] guardado embed.zip (291 bytes)
[+] contenido del ZIP:
    - flag.txt (37 bytes)
      flag{ejemplo}
    - nota.txt (47 bytes)
      Enhorabuena, has mirado debajo de la alfombra.
```

### Alternativas de una línea

```bash
# carve desde el offset que da binwalk
dd if=BW_SOC_3110.png of=embed.zip bs=1 skip=4098 status=none && unzip embed.zip

# o directo con binwalk / foremost / bulk_extractor
binwalk -e BW_SOC_3110.png
foremost -t png,zip -i BW_SOC_3110.png -o out/

# el clásico "zip dentro de imagen"
unzip -l BW_SOC_3110.png     # funciona: ignora el prefijo y lee el EOCD
```

## Explicación técnica

Un PNG (y cualquier formato con fin de archivo explícito) **no reclama** los bytes que van
después del marcador final: los lectores de imagen paran en `IEND` y el resto queda como
relleno invisible. Eso permite esconder ahí un ZIP, un 7z, un PDF o bytes cifrados sin
alterar ni un píxel. Es distinto de la esteganografía LSB (desafío 02), donde el payload
vive **dentro** de los valores de color.

Señales de detección en un SOC:
- tamaño desproporcionado respecto a las dimensiones y a la compresión esperada;
- `Trailer data after PNG IEND chunk` (exiftool);
- firmas de archivo (`PK`, `7z`, `%PDF`, `Rar!`) más allá del fin del contenedor
  (`binwalk`, `file -k`, `trid`);
- `zip`/`unzip` y `7z` aceptan el archivo con el prefijo PNG — truco rápido de validación.

## Lecciones / notas

- **`exiftool` avisa** de datos tras el IEND: es el «reconocimiento barato» que resuelve
  el reto en un comando.
- Cuidado con la aritmética del chunk `IEND`: 12 bytes en total, pero `find("IEND")`
  empieza en el tipo → `+8`.
- Un ZIP concatenado a otro archivo sigue siendo válido: el EOCD se localiza desde el
  final, no desde el principio.
- El peso «varios megabytes» del enunciado es narrativa: aquí eran 291 bytes. El indicio
  real era la **proporción** tamaño/dimensiones.
- Contraste útil para el informe: este reto es *append* (fuera de la imagen), no LSB
  (dentro de los píxeles).

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `BW_SOC_3110.png` | evidencia original |
| `flag.txt` | flag extraída |
| `CONTEXTO.md` | este writeup |
| `solucion/carve_trailer.py` | carver del ZIP anexado tras el IEND |
| `solucion/salida.txt` | salida de la ejecución |
| `work/trailer.bin` | bytes posteriores al IEND (287 B, sin la firma) |
| `work/embed.zip` | ZIP carveado (291 B) |
| `work/extraido/flag.txt`, `work/extraido/nota.txt` | archivos del ZIP |
