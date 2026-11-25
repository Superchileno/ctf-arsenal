# Pirata 2 — El acta de Henry Every (DG-004)

| Campo | Valor |
|---|---|
| Categoría | Forense de documentos (DOCX) — texto oculto en encabezado/pie |
| Evidencia | `Pirata_2.zip` → `acta_henry_every.docx` (25 753 B) |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |
| Dato de navegación | **`38.776970`** (pie de página, texto blanco) |

## Enunciado (resumen)

Expediente DG-004: acta de inventario archivada bajo el nombre de **Henry Every**.
El funcionario «solo examinó el texto central» y firmó «TODO EN ORDEN» en ocho
segundos. La nota final avisa: *«desconfiar de cualquier conclusión basada
únicamente en lo que aparece a primera vista»*.

## Solución

Un `.docx` es un ZIP. El texto del cuerpo (`word/document.xml`) es solo una parte:
las **cabeceras y pies** viven en `word/header1.xml` y `word/footer1.xml`, y no se
ven en una lectura rápida.

```bash
unzip acta_henry_every.docx -d docx
grep -o 'TRAMACTF{[^}]*}' docx/word/header1.xml
grep -o '<w:t[^>]*>[^<]*</w:t>' docx/word/footer1.xml
```

- **Cabecera** — párrafo con `w:color w:val="FFFFFF"` (blanco sobre blanco) y
  `sz 16` (8 pt): la flag.
- **Pie** — mismo truco de color: ` 38.776970`, el **fragmento de navegación**
  que pide el expediente de cierre (Pirata 3).

Verificación de que no hay más texto oculto (blanco / `vanish` / tamaño 1) en
ninguna otra parte del paquete: solo esos dos runs.

Verificado de forma independiente con `solucion/extraer_texto_oculto.py`:

- `word/header1.xml` → run `FFFFFF`, `sz=16` (8 pt): la flag.
- `word/footer1.xml` → run `FFFFFF`: ` 38.776970` (con un espacio inicial).
- `word/document.xml` → solo el acta visible (sin `vanish` ni color blanco).
- `word/media/image1.png` (1500×195): PNG limpio, `IEND` al final, sin datos anexados;
  su `descr` es el texto automático de Word («Dibujo en blanco y negro…»).

## Flag

```
flag{ejemplo}
```

## Dato para Pirata 3

```
DG-004 → 38.776970
```

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `Pirata_2.zip` | evidencia original |
| `flag.txt` | flag final |
| `CONTEXTO.md` | este writeup |
| `work/acta_henry_every.docx` | documento extraído |
| `work/docx/` | paquete OOXML descomprimido (header/footer incluidos) |
| `solucion/extraer_texto_oculto.py` | parser de runs: extrae texto con `w:color FFFFFF` de header/footer/document |
| `work/auditar_docx.py` | auditoría auxiliar (alt text, vanish, imagen) |

## Backups

| Archivo | Backup |
|---|---|
| `ctf/pirata2/CONTEXTO.md` | `ctf/backups/CONTEXTO_pirata2.md.20261023-192857` |
