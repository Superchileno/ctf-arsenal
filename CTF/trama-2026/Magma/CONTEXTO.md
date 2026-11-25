# Desafío 07 — Magma (la postal de cinco lucas)

| Campo | Valor |
|---|---|
| Evento | TRAMA CTF 2026 · Expediente STEGO-MG07: *Turismo de profundidad* |
| Categoría | Stego visual / patrón repetido (anomalía frente a un mosaico periódico) |
| Estado | ✅ Resuelto |
| Evidencia | `Magma.zip` (271.461 B, SHA256 `A3A51D06...4FCA6B`) |
| Imagen | `placa_magma.png` — 2100×520, 8-bit RGB |
| SHA256 imagen | `B913E5712E2E3E607DEF03DB0CACE6BF1274D1321AAE90A01AF8235516EB4205` |

## Flag

```
flag{ejemplo}
```

Se compone uniendo las dos líneas encontradas, sin espacios adicionales:

```
línea 1:  TRAMACTF{L4_L4V4_3SC0ND3_
línea 2:  3L_S3CR3T0_3N_PR0FUND1D4D}
```

## Enunciado (resumen)

Una postal del volcán Villarrica vendida como «el volcán en tres dimensiones» parece
**repetir el mismo pedazo de magma unas veinte veces**. El guía deja la pista: *«No todo lo
importante está en la superficie. A veces dos cosas parecen iguales hasta que las miras
desde la distancia correcta»*. Hay que analizar la evidencia, encontrar lo escondido y, si
salen varias líneas, leerlas en orden y unirlas sin espacios extra.

## Evidencia

| Archivo | Tamaño | Rol |
|---|---|---|
| `placa_magma.png` | 284.846 B | postal (textura de magma en mosaico) |
| `lecturas_superficie.csv` | 216 B | 4 lecturas de temperatura (ruido narrativo) |
| `LEEME.txt` | 183 B | «la imagen se conserva sin recomprimir» |

Hashes:

```
zip         A3A51D060DEB629E3E30E98DB66CEE33F467984D59633303361215784D4FCA6B
png         B913E5712E2E3E607DEF03DB0CACE6BF1274D1321AAE90A01AF8235516EB4205
csv         86FEAAF42D05D820AD966985DA644DD8B32DC36AAFC97C89FBC69891AD27A549
```

## Reconocimiento

Descartado rápido (nada que ver con el payload):

```bash
$ exiftool placa_magma.png     # solo campos básicos, sin comentarios ni EXIF
$ binwalk placa_magma.png      # PNG + Zlib (IDAT normales), nada anexado
$ strings -n 8 placa_magma.png # ruido de compresión
# chunks: IHDR, 4x IDAT, IEND  -> 0 bytes tras IEND
```

Análisis estructural de la textura:

```
imagen 2100x520
periodo horizontal óptimo: d = 164 px   (diferencia media 0.81, el resto > 16)
2100 / 164 = 12.8 repeticiones  <- "el mismo pedazo de magma unas veinte veces"
periodo vertical: no hay (d=1 siempre gana) -> el mosaico se repite en horizontal
```

La métrica usada es la autocorrelación desplazada: para cada `d`, la diferencia media entre
la imagen y ella misma desplazada `d` columnas. El mínimo aplastante en `d = 164` (y sus
múltiplos 328, 492) confirma el mosaico.

## Análisis

Si la imagen fuera la misma textura repetida exactamente, la diferencia entre la imagen y
su versión desplazada 164 px sería **cero**. En cambio:

```
píxeles con diferencia ≠ 0: 63.682 de 1.006.720
bbox de esas diferencias:  y 106–374 · x 325–1444
```

Las diferencias se concentran en **dos bandas de filas** (108–179 y 303–374): ahí está
pintado el texto, que "rompe" el patrón. Visualizando la máscara de diferencias **aparecen
las dos líneas legibles**. Ese es el «mirar desde la distancia correcta»: no se ve el
mensaje en la postal, se ve en lo que se desvía de la repetición.

Intuición del método: es la misma idea de un autostereograma o de un "spot the difference".
Cuando un patrón se repite y una zona se altera, la resta contra el periodo cancela la
textura y deja el delta limpio.

## Solución (pasos reproducibles)

### Script (guardado en `solucion/revelar_magma.py`)

```python
a  = np.array(Image.open("work/placa_magma.png").convert("RGB")).astype(np.int16)
d  = detectar_periodo(a.mean(axis=2))            # autocorrelación -> 164
dif = np.abs(a[:, d:, :] - a[:, :-d, :]).sum(axis=2)   # lo que se sale del patrón
mask = (dif > 0).astype(np.uint8) * 255
Image.fromarray(mask).save("work/diff_mask.png")
```

```bash
$ python3 solucion/revelar_magma.py
[i] imagen 2100x520
[i] periodo del mosaico: 164 px -> 12.8 repeticiones horizontales
[i] píxeles fuera del patrón: 63682
[i] bandas de texto detectadas: [(108, 179), (303, 374)]
[+] línea 1: filas 108-179 -> work/linea1.png
[+] línea 2: filas 303-374 -> work/linea2.png
```

Resultado (`work/diff_mask.png`, recortes ampliados en `work/linea1.png` y `linea2.png`):

```
TRAMACTF{L4_L4V4_3SC0ND3_
3L_S3CR3T0_3N_PR0FUND1D4D}
```

### Alternativa manual

```bash
# separar dos capas desplazadas 164 px y restarlas (ImageMagick)
convert work/placa_magma.png -crop 1936x520+164+0 +repage a.png
convert work/placa_magma.png -crop 1936x520+0+0   +repage b.png
composite -compose difference a.png b.png diff.png
convert diff.png -auto-level -negate diff_visible.png
```

Con GIMP: filtro *Difference* entre la capa y una copia desplazada 164 px, luego
*Auto → Ajustar niveles*.

## Resultado

```
flag{ejemplo}
```

*«La lava esconde el secreto en profundidad»* — coherente con el «volcán en tres
dimensiones» y con la nota del guía.

## Lecciones / notas

- **Un patrón repetido es una vulnerabilidad de esteganografía**: si sabes el periodo,
  puedes cancelar la textura y quedarte con el delta. La defensa sería variar el mosaico
  (o usar ruido no periódico), justo lo que hace un autostereograma bien construido.
- El periodo no se adivina: se mide con autocorrelación (mínimo de la diferencia media por
  desplazamiento). Los múltiplos del periodo también minimizan → hay que quedarse con el
  primero.
- El CSV de temperaturas es puro atrezzo: 31.8 / 34.1 / 30.5 / 32.0 no intervienen. No
  todo archivo adjunto es una pista.
- `LEEME.txt` («no recomprimir a JPEG») evita destruir la señal: la compresión con pérdida
  habría borrado las diferencias de baja amplitud.
- Cuando el enunciado habla de «varias líneas» y «unirlas sin espacios adicionales», el
  resultado final es la concatenación literal de los renglones, respetando los `_` de los
  extremos (la línea 1 termina en `_` y la 2 empieza con `3L_`).

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `Magma.zip` | evidencia original |
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag final |
| `solucion/revelar_magma.py` | detección de periodo + máscara de diferencias + recortes |
| `solucion/salida.txt` | salida de la ejecución |
| `work/placa_magma.png` | imagen original |
| `work/lecturas_superficie.csv`, `work/LEEME.txt` | adjuntos (ruido narrativo) |
| `work/diff_mask.png` | máscara completa con las dos líneas |
| `work/linea1.png`, `work/linea2.png` | recortes ampliados ×2 de cada línea |
