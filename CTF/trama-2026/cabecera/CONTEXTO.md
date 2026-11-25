# Desafío 32 — CABECERA PERDIDA // Última transmisión

| Campo | Valor |
|---|---|
| Categoría | forense de archivos / reparación de cabecera (PNG) |
| Dificultad | fácil-media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **CABECERA PERDIDA // ÚLTIMA TRANSMISIÓN** — 03:17 — Señal interrumpida. Uno de los nodos
> periféricos de la red dejó de transmitir sin emitir ninguna alerta previa. […] el sistema encontró un
> fragmento entre los residuos de sincronización y los bloques descartados de aquella madrugada.
>
> El archivo estaba asociado a la última actividad del nodo, pero el motor de recuperación lo clasificó
> como **ilegible**. Los intentos automáticos de reconstrucción fallaron […]
>
> Tu misión es analizar el archivo, recuperar la información que aún conserva y descubrir qué dejó el
> nodo en su última transmisión.

## Reconocimiento

`fragmento_0317.bin` — 78.849 B. `file` no lo reconoce (`data`) y `binwalk` solo detecta un flujo zlib
en el offset 41. La cabecera en hexadecimal:

```
000000  00 50 4e 47 0d 0a 1a 0a   .PNG....
000008  00 00 00 0d 49 48 44 52   ....IHDR
000010  00 00 06 40 00 00 03 84   ...@....
```

La firma PNG es `89 50 4E 47 0D 0A 1A 0A`; aquí el **primer byte es `00` en lugar de `89`**. Todo el
resto del archivo está intacto, pero con la firma inválida ningún visor lo abre: de ahí que el motor de
recuperación lo declarara «ilegible».

## Análisis

1. **Reparación**: cambiar el byte 0 a `0x89`.
2. **Validación de estructura**: se recorren los chunks y se recalcula el CRC de cada uno.

```
IHDR len=13     crc=OK
IDAT len=65536  crc=OK
IDAT len=13244  crc=OK
IEND len=0      crc=OK
datos tras IEND: 0 | integridad: True
```

El PNG resultante es **1600×900 RGB** y se abre sin problemas. Es un panel de terminal que representa
la «última transmisión» del nodo VF-0317 (malla VECTOR, bloque 03 recuperado).

3. **Payload visible**: el panel `PAYLOAD // BLOQUE 03` muestra un volcado hexadecimal:

```
0000  54 52 41 4D 41 43 54 46 7B 4C
000A  34 5F 53 33 4E 34 4C 5F 52 30
0014  54 34 5F 43 30 4E 53 33 52 56
001E  34 5F 53 55 5F 31 44 33 4E 54
0028  31 44 34 44 5F 30 33 31 37 7D
```

Decodificado como ASCII:

```
flag{ejemplo}
```

### Nota sobre la extracción del payload

El volcado está **renderizado en la imagen** (no hay metadatos ni texto embebido). Se transcribió por
inspección visual del PNG restaurado. Se probó OCR (`tesseract` con whitelist `0-9A-F`) como alternativa:
el motor confunde de forma sistemática los dígitos `5` y `2` del font del panel, por lo que la
transcripción manual es más fiable. La parte crítica del reto —y la que resuelve el «ilegible»— es la
reparación de la cabecera.

## Solución (pasos reproducibles)

```bash
# Reparar firma, validar CRC y decodificar el payload
python3 solucion/reparar_fragmento.py fragmento_0317.bin work/cabecera_restaurada.png
# firma original : 00504e470d0a1a0a
# firma reparada : 89504e470d0a1a0a
# IHDR/IDAT/IDAT/IEND: crc=OK
# FLAG: flag{ejemplo}
```

Equivalente mínimo:

```bash
python3 - <<'EOF'
d = bytearray(open('fragmento_0317.bin','rb').read())
d[0] = 0x89
open('cabecera_restaurada.png','wb').write(d)
EOF
# abrir la imagen y leer el panel PAYLOAD // BLOQUE 03
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `fragmento_0317.bin` | Evidencia original (78.849 B, firma dañada) |
| `work/cabecera_restaurada.png` | PNG reparado (1600×900), CRC válidos |
| `work/validar_png.py` | Validador de chunks/CRC |
| `solucion/reparar_fragmento.py` | Reparación + validación + decodificación del payload |
| `flag.txt` | Flag del reto |

## Lecciones / notas

- **Un solo byte** en la firma basta para que un formato entero se vuelva «ilegible» para las
  herramientas automáticas; el contenido sigue ahí.
- Siempre conviene comprobar el **CRC de los chunks** tras reparar: confirma que el daño era solo la
  cabecera y que los datos no están corruptos.
- El payload puede estar **renderizado** en la imagen (hex dump, captura de terminal), no solo en
  metadatos; toca leer la imagen además de analizarla.
- OCR no siempre es fiable con fonts de panel/terminal (dígitos `5` y `2` confundidos); validar el
  resultado contra la estructura esperada (`TRAMACTF{…}`) es imprescindible.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-203411` |
