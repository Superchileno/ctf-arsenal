# La misma nota (Práctica 17) — CONTEXTO

**Reto:** `lamismanota` (forense de partituras / MuseScore)
**Fecha de análisis:** 2026-10-24
**Evidencias:** `practica_17.mscz` (88.959 B), `revision_17.txt` (563 B), `anotaciones.zip` (299 B)

| Dato | Valor |
|---|---|
| Flag | ✅ `flag{ejemplo}` |
| Password del zip | `6D2A91C47B3E` |
| Naturaleza del reto | 12 notas **reescritas enarmónicamente** (mismo sonido, distinta grafía) |

---

## 1. Material

- `practica_17.mscz` = ZIP de MuseScore 4.7.5 con `mi heart is broken.mscx` (XML de 480.810 B),
  `score_style.mss`, `automation.json`, `audiosettings.json`, `viewsettings.json`, `META-INF/container.xml`.
- `revision_17.txt` = informe del corrector: 105 compases, alturas y duraciones **sin cambios**,
  **12 inconsistencias de escritura**, más la regla de conteo.
- `anotaciones.zip` = ZIP **cifrado** (ZipCrypto) con `mensaje.txt` (102 B).

## 2. La pista

> «No cambió lo que toca. Cambió la forma en que lo escribió.»
> «Si suena igual, no busques otra nota. Mira cómo quedó escrita.»

En MusicScore cada nota tiene:
- `<pitch>` → altura MIDI (lo que **suena**),
- `<tpc>` → *tonal pitch class* = posición en el círculo de quintas (cómo está **escrita**).

`tpc = 14 + quintas`:

| tpc | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 21 | 22 | 23 | 24 | 25 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nota | Cb | Gb | Db | Ab | Eb | Bb | F | C | G | D | C# | G# | D# | A# | E# |

La obra está en **Sol bemol mayor / Mi bemol menor** (6 bemoles): Cb, Db, Eb, F, Gb, Ab, Bb.
Distribución global de `tpc` (1378 notas):

```
Cb 215 | Ab 321 | Eb 242 | Gb 139 | Db 146 | Bb 90 | F 164 | C 24 | G 15 ...
```

En ese contexto **cualquier nota escrita con sostenido** es una reescritura enarmónica
(Db→C#, Ab→G#, Eb→D#, Bb→A#, F→E#): suena exactamente igual y, al no necesitar signo visible,
la partitura impresa se ve idéntica. Eso es «lo que cambió».

## 3. Las 12 inconsistencias

Notas con `tpc` 21-25 y **sin** `<Accidental>` (no se imprime ningún signo):

| # | compás | pentagrama | índice (0-7) | tpc | escrita como | suena como | pitch |
|---|---|---|---|---|---|---|---|
| 1 | 10 | superior | 6 | 25 | **E#** | F | 77 |
| 2 | 16 | inferior | 5 | 24 | **A#** | Bb | 70 |
| 3 | 20 | superior | 2 | 23 | **D#** | Eb | 75 |
| 4 | 40 | inferior | 2 | 23 | **D#** | Eb | 63 |
| 5 | 48 | inferior | 1 | 24 | **A#** | Bb | 70 |
| 6 | 50 | superior | 1 | 24 | **A#** | Bb | 82 |
| 7 | 80 | inferior | 4 | 23 | **D#** | Eb | 63 |
| 8 | 82 | superior | 4 | 21 | **C#** | Db | 73 |
| 9 | 87 | superior | 7 | 23 | **D#** | Eb | 75 |
| 10 | 96 | inferior | 3 | 24 | **A#** | Bb | 70 |
| 11 | 100 | superior | 3 | 22 | **G#** | Ab | 80 |
| 12 | 103 | inferior | 6 | 25 | **E#** | F | 53 |

(Excluida una 13.ª con `tpc=16`, D natural en el compás 72, que **sí** lleva
`<Accidental>accidentalNatural</Accidental>` y por tanto es una alteración legítima, no una
inconsistencia: son 12 exactas, como dice el informe.)

Script: `solucion/parse3.py` (recorre pentagramas/compases y filtra por `tpc`).

## 4. La regla de conteo → password

`revision_17.txt`:

> cada inconsistencia está en un compás con 16 notas individuales;
> 8 en el pentagrama superior y 8 en el inferior;
> el corrector cuenta primero las 8 del superior, de izquierda a derecha;
> después las 8 del inferior, también de izquierda a derecha;
> el contador comienza en 0.

→ índice global = `idx` (superior) ó `8 + idx` (inferior). Cada valor cae en **0-15 = un dígito
hexadecimal**, y las 12 en orden de compás dan:

| compás | 10 | 16 | 20 | 40 | 48 | 50 | 80 | 82 | 87 | 96 | 100 | 103 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| índice | 6 | 13 | 2 | 10 | 9 | 1 | 12 | 4 | 7 | 11 | 3 | 14 |
| hex | **6** | **D** | **2** | **A** | **9** | **1** | **C** | **4** | **7** | **B** | **3** | **E** |

```
password = 6D2A91C47B3E        (12 nibbles = 6 bytes)
```

## 5. Apertura del zip y flag

```bash
unzip -P 6D2A91C47B3E anotaciones.zip       # -> mensaje.txt
```

```bash
python3 solucion/parse3.py                  # lista las 12 anomalías
unzip -o -P "$(python3 solucion/indices_hex.py)" anotaciones.zip -d salida
```

Contenido de `mensaje.txt`:

```
La reproducción nunca cambió. La escritura sí.

flag{ejemplo}
```

Nota: el password debe ir en **mayúsculas** (`6D2A91C47B3E`); en minúsculas `unzip` da
«incorrect password».

## 6. Archivos del proyecto

| Ruta | Contenido |
|---|---|
| `practica_17.mscz`, `revision_17.txt`, `anotaciones.zip` | evidencias originales |
| `flag.txt` | la flag |
| `solucion/parse3.py` | detecta las 12 reescrituras enarmónicas (tpc 21-25 sin accidental) |
| `solucion/indices_hex.py` | calcula el password a partir de los índices y abre el zip |
| `solucion/mensaje.txt` | anotación recuperada |
| `backups/` | copia de las 3 evidencias antes de manipularlas |

## 7. Historial

- **2026-10-24** — Se descomprime el `.mscz` (ZIP → `.mscx` XML). Se identifica que la info
  alterada es `tpc` (grafía) y no `pitch` (sonido). Se aíslan 12 notas con `tpc` 21-25 sin
  accidental (reescrituras enarmónicas Db→C#, Ab→G#, Eb→D#, Bb→A#, F→E#) en los compases
  10, 16, 20, 40, 48, 50, 80, 82, 87, 96, 100, 103. Aplicando la regla de conteo del informe
  (0-15, superior y luego inferior) se obtiene `6D2A91C47B3E`, password del ZIP.
  Recuperada `mensaje.txt` con la flag
  **`flag{ejemplo}`**.
