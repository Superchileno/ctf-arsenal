# Desafío 34 — Observa (Expediente 01)

| Campo | Valor |
|---|---|
| Categoría | forense de documentos / ZIP cifrado + reparación de firma + texto en blanco |
| Dificultad | media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> **Observa — El Archivo de los Ausentes — Expediente 01: «Aquí no ha pasado nada»** […]
> A las 03:17 de la madrugada llegó un paquete desde una cuenta que, según el sistema, ya no existe.
> […] El último analista dejó una nota: «La miré una vez y no vi nada. La miré de nuevo, por si acaso.
> Confirmo: sigo sin ver nada». […] «Que no lo veas no significa que no esté ahí».
>
> Tu misión: investiga la evidencia recibida y descubre qué intentaron esconder.

## Reconocimiento

`Observa.zip` (12.135 B, SHA256 `711f016f...9af02216`) contiene **un solo archivo cifrado**:

| Entrada | Tamaño | Cifrado | Método |
|---|---|---|---|
| `por_aqui.docx` | 12.862 B (comprimido 11.995) | **ZipCrypto** | deflate |

Metadatos: `flag_bits 0x9` (cifrado + data descriptor), CRC `0x5e1dce6e`, fecha 2026-10-19 19:54:28.
Sin comentario de archivo, sin campo extra y sin cola tras el EOCD: no hay pista de contraseña en el ZIP.

## Análisis

### 1) Contraseña del ZIP

Se extrajo el hash con `zip2john` y se atacó con `rockyou`:

```bash
zip2john Observa.zip > hash.txt
gzip -dc /usr/share/wordlists/rockyou.txt.gz | john --stdin hash.txt
# jhonny  (Observa.zip/por_aqui.docx)
```

Contraseña: **`jhonny`**. Se verificó que el CRC del DOCX descifrado coincide
(`0x5e1dce6e`), por lo que la clave es correcta y el contenido íntegro.

> Nota: la lista central del ZIP **no** está cifrada (solo los datos), así que se pueden listar
> entradas sin contraseña; la lectura sí la exige.

### 2) «No se abre»: firma del DOCX dañada

Al descifrar, el archivo empieza así:

```
50 15 78 04 14 00 00 00 08 00 00 00 21 00 ...
```

Un DOCX (OOXML) es un ZIP cuyo encabezado local debe empezar por `50 4B 03 04` (`PK\x03\x04`).
Aquí los **cuatro primeros bytes están sustituidos** (`50 15 78 04`), por lo que ninguna herramienta lo
reconoce como documento: es el «no lo veo» del enunciado. El resto del archivo está intacto
(CRC válido del DOCX tal como se guardó) y la lista central permite enumerar sus 10 partes.

Reparación: restaurar `data[0:4] = b"PK\x03\x04"`. El DOCX se abre con normalidad.

### 3) El texto está en blanco

En `word/document.xml` hay dos runs (duplicados) con **`w:color w:val="FFFFFF"`** — blanco sobre blanco:

```
La bandera es flag{ejemplo}
```

No hay cabeceras/pies, comentarios, texto `vanish`, resaltado ni imágenes en este paquete: el secreto es
el color del texto.

## Solución (pasos reproducibles)

```bash
# 1) Contraseña (rápido con rockyou)
zip2john Observa.zip > hash.txt
gzip -dc /usr/share/wordlists/rockyou.txt.gz | john --stdin hash.txt   # -> jhonny

# 2) Descifrar + reparar firma + extraer runs blancos
python3 solucion/resolver_observa.py Observa.zip jhonny
# [1] entradas: ['por_aqui.docx']
# [2] DOCX descifrado: 12862 B; cabecera 5015780414000000
#     cabecera dañada -> reparando a PK\x03\x04
# [3] runs en blanco: ['La bandera es flag{ejemplo}', ...]
# [4] FLAG: flag{ejemplo}
```

Equivalente manual:

```bash
unzip -P jhonny Observa.zip            # por_aqui.docx (firma dañada)
python3 - <<'EOF'
d = bytearray(open('por_aqui.docx','rb').read())
d[0:4] = b'PK\x03\x04'
open('por_aqui_reparado.docx','wb').write(d)
EOF
unzip por_aqui_reparado.docx -d docx
grep -o 'TRAMACTF{[^}]*}' docx/word/document.xml
```

## Flag

```
flag{ejemplo}
```

## Evidencia y artefactos

| Ruta | Contenido |
|---|---|
| `Observa.zip` | Evidencia entregada (12.135 B) |
| `work/hash.txt` | Hash `pkzip` para John |
| `work/por_aqui.docx` | DOCX descifrado (firma dañada, tal cual) |
| `work/por_aqui_reparado.docx` | DOCX con `PK\x03\x04` restaurado |
| `work/flag.txt` | Flag extraída |
| `solucion/resolver_observa.py` | Descifra, repara la firma y extrae los runs en blanco |
| `flag.txt` | Flag del reto |

## Lecciones / notas

- Un ZIP puede **listarse sin contraseña** (la lista central no se cifra), pero no leerse; no confundir
  «puedo ver las entradas» con «puedo abrirlo».
- `rockyou` sigue siendo suficiente para contraseñas humanas débiles (`jhonny`).
- **Reparar la firma** de un contenedor (ZIP/DOCX/PNG) es rutina forense: los CRC permiten confirmar que
  el resto del archivo está íntegro.
- Texto en **blanco sobre blanco** (`w:color FFFFFF`) es invisible en el visor y sigue presente en el XML;
  conviene revisar también `vanish`, tamaños ínfimos, comentarios y cabeceras/pies.
- El CRC del DOCX corresponde al archivo ya dañado: la corrupción de los 4 bytes fue deliberada antes de
  empaquetarlo.

## Backups

| Archivo | Backup |
|---|---|
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-204617` |
