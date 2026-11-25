# Desafío 23 — La Hermandad de las Sombras (fiesta-sombras-2026)

| Campo | Valor |
|---|---|
| Categoría | OSINT + esteganografía (ZIP anexado) + cifrado clásico (César) |
| Dificultad | fácil-media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> La Hermandad de las Sombras ha enviado una invitación cifrada a todos sus miembros para la fiesta de
> Halloween en el castillo del Conde Cyber-Drácula. Para no levantar sospechas, el Conde ha publicado la
> invitación en un repositorio público de GitHub bajo el nombre **fiesta-sombras-2026**.
>
> La invitación es una imagen que parece inofensiva, pero el Conde es un experto en ocultar secretos.
> Dicen que dentro de esa imagen hay un archivo comprimido, y dentro de ese archivo, un mensaje cifrado
> con un hechizo antiguo (uno de los cifrados más clásicos de la historia).
>
> 1. Encontrar el repositorio en GitHub.
> 2. Extraer el archivo oculto en la imagen.
> 3. Descifrar el mensaje para obtener la flag.

## Reconocimiento

Búsqueda en la API de GitHub:

```bash
curl -s "https://api.github.com/search/repositories?q=fiesta-sombras-2026"
```

→ **`CondeCyberDracula/fiesta-sombras-2026`** (descripción «Shall we dance?», rama `main`).

El árbol del repo solo tiene `README.md` (316 B), pero el README incrusta dos imágenes de
`github.com/user-attachments/assets/...`:

| Imagen | Tamaño | Detalle |
|---|---|---|
| `imagen1.png` | 975.303 B | PNG grande, sin datos anexados |
| `Pista_Invitacion.png` | 36.916 B | En realidad es **JPEG** (`JFIF`), 600×400 |

Ambas se descargaron con `curl -L` (las URLs de user-attachments redirigen).

## Análisis

La imagen pequeña (`Pista_Invitacion.png`) no termina en el marcador `FFD9` de JPEG: **después** de él
hay un ZIP completo. Búsqueda directa de la firma:

```python
data.find(b'PK\x03\x04')   # 0x8f92 (36.754)
```

Contenido del ZIP anexado (`secreto.zip`): un único archivo `secreto.txt` (40 B, sin cifrado ZIP).
Su contenido:

```
flag{ejemplo}
```

Es un **César** clásico. Comparando el inicio con el formato de la bandera (`TRAMACTF`), el
desplazamiento es **−3**:

```
W→T  U→R  D→A  P→M  D→A  F→C  W→T  I→F
```

Aplicando `−3` a todo el texto (solo letras, se conservan dígitos, `_`, `{`, `}`):

```
flag{ejemplo}
```

Comprobación: el único desplazamiento (de los 26) que produce el prefijo `TRAMACTF{` es `−3`.

## Solución (pasos reproducibles)

```bash
# 1) Repositorio
curl -s "https://api.github.com/repos/CondeCyberDracula/fiesta-sombras-2026/git/trees/main?recursive=1"

# 2) Imágenes del README
curl -L -o work/imagen1.png https://github.com/user-attachments/assets/6685636d-622c-40e1-bcaf-f03045623852
curl -L -o work/Pista_Invitacion.png https://github.com/user-attachments/assets/7889da77-03f1-4d85-8cd7-a04a5984ade8

# 3) ZIP anexado tras el EOI del JPEG
python - <<'EOF'
import pathlib, zipfile, io
b = pathlib.Path('work/Pista_Invitacion.png').read_bytes()
off = b.find(b'PK\x03\x04')                 # 0x8f92
z = zipfile.ZipFile(io.BytesIO(b[off:]))
print(z.read('secreto.txt'))                # WUDPDFWI{...}
EOF

# 4) César -3
python - <<'EOF'
s = 'flag{ejemplo}'
print(''.join(chr((ord(c)-65-3)%26+65) if c.isupper() else
              chr((ord(c)-97-3)%26+97) if c.islower() else c for c in s))
EOF
```

En `solucion/resolver_sombras.py` está la cadena completa automatizada (descarga, carving del ZIP,
César y validación del prefijo).

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `work/Pista_Invitacion.png` | JPEG de 36.916 B con ZIP anexado desde `0x8f92` |
| `work/imagen1.png` | Imagen grande del README (sin payload) |
| `work/secreto.zip` | ZIP carved (1 archivo, 243 B) |
| `work/secreto.txt` | Mensaje cifrado con César |
| `solucion/resolver_sombras.py` | Resolución automatizada |
| `flag.txt` | Flag descifrada |

## Lecciones / notas

- **OSINT**: el nombre del repo (`fiesta-sombras-2026`) basta para localizarlo en la API de GitHub; el
  README es el único archivo y las imágenes viven en `user-attachments`, no en el árbol del repo.
- **JPEG + ZIP anexado**: localizar `PK\x03\x04` con una búsqueda binaria es más rápido que `binwalk` y
  no requiere extraer los datos a disco.
- Los datos posteriores al marcador `FFD9` no afectan a la visualización de la imagen: pasan inadvertidos.
- **César**: el prefijo conocido de la bandera (`TRAMACTF{`) revela el desplazamiento; con 26 pruebas
  queda confirmado sin ambigüedad.
- La flag conserva el estilo "1337" del texto cifrado (`Fi3sta`, `m3d14n0ch3`), porque el César solo
  transforma letras.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-191018` |
