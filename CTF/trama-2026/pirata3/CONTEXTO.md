# Pirata 3 — El tesoro y la boleta fantasma (DG-005)

| Campo | Valor |
|---|---|
| Categoría | Geolocalización — unión de fragmentos + Open Location Code (10 caracteres) |
| Evidencia | `Pirata_3.zip` → `ACTA_DE_CIERRE.txt` |
| Estado | ✅ Resuelto (2 lecturas posibles; ver abajo) |
| Flag propuesta | `flag{ejemplo}` |

## Los dos fragmentos

| Expediente | Origen | Fragmento |
|---|---|---|
| **DG-003** (Pirata 1) | LSB del WAV `senal_malapata.wav`, contenedor `DGLD`+zlib | **`19.914434`** (con coma) |
| **DG-004** (Pirata 2) | pie del DOCX `acta_henry_every.docx` (texto blanco) | **`38.776970`** |

El acta de cierre pide: unir ambos respetando el orden de los expedientes, calcular el
**Plus Code global de 10 caracteres** (8 símbolos + `+` + 2) y montar:

```
flag{ejemplo}
```

## Cálculo (librería oficial `openlocationcode`)

```python
from openlocationcode import openlocationcode as olc
olc.encode(38.776970, 19.914434, 10)   # -> '8FCXQWG7+QQ'
olc.encode(19.914434, 38.776970, 10)   # -> '7GFWWQ7G+QQ'
```

| Lectura | Coordenadas | Plus Code | Dónde cae |
|---|---|---|---|
| **A** — orden literal del acta (lat, lon) | 19.914434, 38.776970 | `7GFWWQ7G+QQ` | Sudán, desierto inland (mar Rojo a ~170 km) |
| **B** — mapa «al revés» (lat = DG-004) | 38.776970, 19.914434 | `8FCXQWG7+QQ` | **Mar Jónico, mar abierto** (agua) |

### Por qué se propone B

Tres guiños del propio expediente apuntan al agua y a invertir el orden:

1. «Un tesoro **enterrado en el agua** cuenta como depósito a plazo».
2. El expediente se titula **«Cierre de caja en alta mar»**, y en Pirata 1 el capitán
   alega navegar en **aguas internacionales**.
3. El cartógrafo «**movió el mapa al revés**» antes de dar con el botín.

## Entrega

```
flag{ejemplo}
```

Si la plataforma rechazara esta lectura, la alternativa literal (orden de expedientes)
es:

```
flag{ejemplo}
```

## Verificación

```bash
python3 solucion/pluscode.py     # ambas lecturas con la librería oficial
```

Decodificación de ida y vuelta (la librería devuelve el centro de la celda):

```
8FCXQWG7+QQ -> (38.776937, 19.914437)
7GFWWQ7G+QQ -> (19.914437, 38.776937)
```

## Flag

```
flag{ejemplo}
```

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `Pirata_3.zip` | evidencia original |
| `flag.txt` | flag final (lectura B) |
| `CONTEXTO.md` | este writeup |
| `solucion/pluscode.py` | cálculo de ambos Plus Codes |
| `work/ACTA_DE_CIERRE.txt` | acta extraída |
| `work/ESTADO.md` | notas de la fase bloqueada (cuando faltaban los fragmentos) |
