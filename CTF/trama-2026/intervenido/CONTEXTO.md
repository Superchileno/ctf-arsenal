# Desafío 36 — Documento Intervenido (MC-0421)

| Campo | Valor |
|---|---|
| Categoría | Forense de documentos / esteganografía OOXML (`customXml`) |
| Dificultad | fácil-media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **DOCUMENTO INTERVENIDO // MESA CENTRAL**
> Durante la evacuación de la Mesa Central, los protocolos de contingencia se activaron automáticamente.
> Decenas de informes fueron sellados y transferidos al repositorio de emergencia antes de que los sistemas
> quedaran fuera de servicio. […] De uno de aquellos documentos solo sobrevivió una copia.
> A primera vista, el informe parecía intacto. […] Pero había una inconsistencia. La huella registrada antes
> del cierre no coincidía con la del documento finalmente archivado. […] Según el sistema, el archivo nunca
> había sido alterado. Según la evidencia, algo había cambiado.
> **Tu misión: examinar el documento, descubrir qué ocurrió antes del cierre y recuperar aquello que quedó oculto.**

## Reconocimiento

Evidencia entregada: `documento_intervenido_0421.docx`

| Dato | Valor |
|---|---|
| Tamaño | 56.219 B |
| SHA256 | `C5FE03C2E9AC06CB903EE42F67E18CF9629F771772BF61AEE37D9B3BF3DB6AE9` |
| Partes OOXML | 19 |
| Comentario ZIP | vacío |

Estructura del paquete:

```
[Content_Types].xml
_rels/.rels
docProps/{core,app}.xml, thumbnail.jpeg
customXml/item1.xml            <-- ANOMALÍA
customXml/itemProps1.xml
customXml/_rels/item1.xml.rels
word/document.xml, footer1.xml, settings.xml, styles.xml, ...
word/media/image1.png          (cabecera "TRAMA CTF // VECTOR FANTASMA / MC-0421")
```

La **huella** del enunciado apunta a que el contenido empaquetado no coincide con lo que declara el visor.
La pista técnica está en `customXml/item1.xml`: es el único componente que no existe en un DOCX generado
normalmente por `python-docx` (los metadatos lo delatan: `dc:creator=python-docx`).

## Análisis

### 1) El señuelo del texto visible

El cuerpo (`word/document.xml`) es coherente, pero deja una pista:

```
VF-12 | AISLADO | 04:20:31 | Revisión diferida
· El registro VF-12 queda pendiente de validación manual en el siguiente ciclo.
· La copia visible no contiene adjuntos declarados por el operador.
· No se registran elementos adicionales asociados al informe visible.
```

Nada en `document.xml` está oculto: no hay runs con `w:vanish`, ni texto blanco (`w:color FFFFFF`),
ni cadenas tipo hash. El engaño es la palabra **«copia visible»**: el informe que se ve no es el informe
completo.

### 2) La parte no visible: `customXml/item1.xml`

```xml
<recovery xmlns="urn:trama:cache:v1">
  <state>orphaned</state>
  <channel>VF-12</channel>
  <cache encoding="base64">UEsDBBQAAAAIAFEaR13fZ9jAjgAAAK8AAAARAAAAcmVnaXN0cm9fMDQyMS5kYXQ...</cache>
</recovery>
```

El canal **VF-12** —el nodo que el informe marca como *AISLADO / revisión diferida*— es exactamente el que
dejó un caché de recuperación huérfano.

### 3) Base64 → ZIP → registro

`UEsDBBQ` es `PK\x03\x04`: el `cache` es un **ZIP en base64** de 274 B que contiene una sola entrada,
`registro_0421.dat` (175 B):

```
TRAMA_RECOVERY_CACHE
source=VF-12
timestamp=04:21:17
encoding=hex
payload=5452414D414354467B4C305F3043554C54305F...
```

`encoding=hex` y un `payload` de 100 caracteres hexadecimales → 50 bytes ASCII:

```
flag{ejemplo}
```

El `timestamp=04:21:17` coincide con el `REGISTRO 04:21:17` de la cabecera del documento y con la ventana
de cierre (último evento visible 04:21:03): el caché se escribió **después** del cierre y quedó fuera del
informe «definitivo». Eso explica la inconsistencia de la huella: el archivo que se archivó contiene una
parte (`customXml/item1.xml`) que no estaba en el original y que ningún visor de Word muestra.

## Solución (pasos reproducibles)

Automático:

```bash
python3 solucion/extraer_intervenido.py documento_intervenido_0421.docx
# [1] DOCX: documento_intervenido_0421.docx (56219 B)
# [2] partes OOXML: 19
# [3] cache base64 -> ZIP interno (274 B)
#     entradas: ['registro_0421.dat']
# [4] registro_0421.dat: TRAMA_RECOVERY_CACHE / source=VF-12 / timestamp=04:21:17 / encoding=hex
# [5] payload hex -> 'flag{ejemplo}'
# FLAG: flag{ejemplo}
```

Manual:

```bash
unzip documento_intervenido_0421.docx -d docx
grep -o '<cache encoding="base64">[^<]*' docx/customXml/item1.xml \
  | sed 's/.*>//' | base64 -d > cache.zip
unzip -p cache.zip registro_0421.dat
# payload=...  ->  hex a texto
python3 -c "print(bytes.fromhex('<hex>').decode())"
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `documento_intervenido_0421.docx` | Evidencia entregada (56.219 B, SHA256 `C5FE03C2…DB6AE9`) |
| `work/customXml_item1.xml` | Parte OOXML con el `<cache>` en base64 |
| `work/cache_interna.zip` | ZIP interno decodificado (274 B) |
| `work/registro_0421.dat` | Registro `TRAMA_RECOVERY_CACHE` con el payload hex |
| `solucion/extraer_intervenido.py` | Solución automática (docx → base64 → zip → hex → flag) |
| `flag.txt` | Flag del reto |

## Lecciones / notas

- Un DOCX es un ZIP: conviene **listar todas sus partes** antes de leer el texto. Las partes «de relleno»
  (`customXml/`, `docProps/`, `word/media/`) son el escondite habitual.
- `customXml/item1.xml` no lo genera el usuario: es un datastore XML que Word mantiene para aplicaciones
  externas. Un `<recovery>` con base64 es contenido inyectado, no funcionalidad de Word.
- Doble codificación (base64 → ZIP → hex) es suficiente para que un visor no muestre nada, pero no para
  un analista: reconocer `UEsDBBQ` = `PK\x03\x04` y `encoding=hex` resuelve el caso.
- La narrativa de la «huella» se explica sola: el hash cambia porque se añadió una parte al paquete
  después de sellarlo, sin tocar el texto visible.
- Los metadatos (`dc:creator=python-docx`) delatan que el archivo no salió de Word.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261024-130836` |
