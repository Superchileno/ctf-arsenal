# Desafío 25 — El Archivo Imposible

| Campo | Valor |
|---|---|
| Categoría | esteganografía / polyglot PNG+ZIP + capas (gzip, ASCII85, ZIP cifrado) |
| Dificultad | media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **El Archivo Imposible — El respaldo que nadie pidió** — TRAMA CTF 2026 · Expediente 13 […]
> «Nada de documentos comprimidos. Desde hoy, todos los respaldos se guardan como imágenes. Así los
> hackers no van a cachar nada». […] un funcionario encontró un único archivo en la carpeta de
> evidencias. Se abría sin problemas y parecía una imagen bastante normal. […]
>
> «No todo lo que se ve es todo lo que hay. El respaldo sigue ahí, aunque nadie quiera hacerse cargo».
>
> Tu misión: investiga la evidencia, determina qué contiene realmente y recupera el mensaje que quedó
> escondido. No necesitas acceder a ningún servicio externo.

## Reconocimiento

`El_Archivo_Imposible.zip` (12.635 B, SHA256 `cc6d42dc...f1d19e73`) contiene un único archivo:

```
archivo_imposible.png   14.030 B   PNG 640×360, RGB de 8 bits, sin entrelazado
```

`binwalk` delata el polyglot:

```
0      PNG image, 640 x 360, 8-bit/color RGB, non-interlaced
114    Zlib compressed data, default compression
13660  Zip archive data, at least v2.0, compressed size: 254, uncompressed size: 249, name: nivel2.gz
14008  End of Zip archive, footer length: 22
```

Dos chunks `tEXt` dentro del PNG:

| keyword | valor |
|---|---|
| `pista` | `polyglot: png+zip` |
| `clave_nivel4` | **`pr1sma_oculto`** |

## Análisis (cadena de 4 niveles)

```
archivo_imposible.png
 └─ [tras IEND, offset 0x355c] ZIP nivel1 (370 B)
     └─ nivel2.gz (249 B)
         └─ gunzip → 287 B de texto ASCII85
             └─ a85decode → ZIP nivel3 (236 B)
                 └─ flag.txt (cifrado ZIP, 42 B)  ← contraseña: pr1sma_oculto
```

1. **Polyglot PNG+ZIP**: el PNG es válido y se abre con normalidad; tras el chunk `IEND` (offset
   `0x3554`) hay un ZIP completo desde `0x355c`. La firma `PK\x03\x04` se localiza con una búsqueda
   binaria directa.
2. **`nivel1.zip` → `nivel2.gz`**: un gzip de 249 B, sin cifrado.
3. **gunzip → texto de 287 B**: parece basura (`:eLln$31A4!!#9B;…`) pero el alfabeto y el relleno final
   corresponden a **ASCII85** (Adobe/Base85 sin prefijo `~>`).
4. **ASCII85 → `nivel3.zip`**: ZIP de 236 B con un único `flag.txt` de 42 B **cifrado con ZipCrypto**
   (método *stored*).
5. **`flag.txt`**: la contraseña está en el `tEXt clave_nivel4` del propio PNG (`pr1sma_oculto`).

Contenido final:

```
flag{ejemplo}
```

## Solución (pasos reproducibles)

```bash
unzip El_Archivo_Imposible.zip -d work/

python3 solucion/resolver_imposible.py work/archivo_imposible.png
# [1] tEXt: {'clave_nivel4': 'pr1sma_oculto', 'pista': 'polyglot: png+zip'}
# [2] ZIP anexado tras IEND en 0x355c; tamaño 370 B
#     entradas: ['nivel2.gz']
# [3] nivel2.gz -> 287 bytes de texto ASCII85
# [4] ASCII85 -> ZIP de 236 B
# [5] contraseña 'pr1sma_oculto' -> flag{ejemplo}
```

Pasos manuales equivalentes:

```bash
# ZIP anexado
python -c "d=open('archivo_imposible.png','rb').read(); open('n1.zip','wb').write(d[d.find(b'PK\\x03\\x04'):])"
unzip -o n1.zip            # nivel2.gz
gunzip -c nivel2.gz > nivel2.txt
# ASCII85 -> ZIP
python -c "import base64;d=open('nivel2.txt','rb').read().strip();open('n3.zip','wb').write(base64.a85decode(d,adobe=False))"
unzip -P pr1sma_oculto n3.zip   # flag.txt
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `El_Archivo_Imposible.zip` | Evidencia entregada (12.635 B) |
| `work/archivo_imposible.png` | PNG polyglot (14.030 B) |
| `work/nivel1.zip` | ZIP anexado tras `IEND` (370 B) |
| `work/nivel2.gz` / `work/nivel2.out` | gzip y su contenido ASCII85 |
| `work/nivel3.zip` | ZIP interno con `flag.txt` cifrado |
| `work/flag.txt` | Flag extraída |
| `flag.txt` | Copia de la flag en la raíz del desafío |
| `solucion/resolver_imposible.py` | Resolución automatizada de los 4 niveles |

## Lecciones / notas

- **Polyglot PNG+ZIP**: una imagen válida puede ser a la vez un archivo comprimido; el contenido tras
  `IEND` no impide verla y pasa desapercibido.
- **Los metadatos son parte del reto**: los `tEXt` daban la pista (`polyglot: png+zip`) y la contraseña
  del último nivel (`pr1sma_oculto`).
- **ASCII85** no siempre empieza con `<~`; reconocerlo por el alfabeto y el relleno (`z` para ceros) es
  suficiente.
- **ZIP con datos *stored* y cifrado clásico** es vulnerable a *known-plaintext* (`bkcrack`), pero aquí
  la contraseña estaba escondida en el propio archivo, que es la vía prevista.
- "Cambiar la extensión" no es seguridad: el respaldo "imposible" seguía dentro de la imagen, tal como
  decía el correo anónimo.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-191443` |
