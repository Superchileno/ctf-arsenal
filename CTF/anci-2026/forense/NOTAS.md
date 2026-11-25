# ANCI — Reto "Forense" / `cold-ledger` (HackRocks)

**Paquete:** `cold-ledger.zip` → `mft.csv`, `usn.csv`, `unalloc.raw` (16 MiB = 0x1000000)
**Flag:** `flag{ejemplo}`
**Estado:** ✅ RESUELTO

---

## 1. Contenido del paquete

| Archivo | Tamaño | Rol |
|---|---|---|
| `mft.csv` | 825 B | Registros MFT (Nombre, borrado, timestamps, DataRun) |
| `usn.csv` | 861 B | Journal USN (CREATE / DATA_OVERWRITE / DELETE) |
| `unalloc.raw` | 16 MiB | Espacio no asignado (clústeres 0..4095, 4 KiB/clúster) |

## 2. Correlación de artefactos

`mft.csv`:

| Entry | Seq | Nombre | Borrado | DataRun | Nota |
|---|---|---|---|---|---|
| 1204 | 2 | `export_live.csv` | No | 80 | exportación viva (ruido) |
| **4821** | **4** | **`frostbook_ledger.bin`** | **Sí** | **240** | **libro maestro** |
| 4902 | 2 | `frostbook_draft.bin` | Sí | 910 | señuelo |
| 4955 | 1 | `frostbook_scratch.tmp` | Sí | 1500 | señuelo |
| 5201 | 3 | `payroll_cache.bin` | Sí | 60 | no relacionado |

`usn.csv` (línea de tiempo del libro real):

```
09:12:44.100  FILE_CREATE      frostbook_ledger.bin
09:14:02.220  DATA_OVERWRITE   frostbook_ledger.bin
09:16:11.500  FILE_DELETE      frostbook_ledger.bin
```

El `DataRun` es el **clúster inicial**. Con clúster de 4096 B:

```
clúster 240  → 240 × 4096 = 0xF0000 = 983 040  (libro maestro)
clúster 910  → 0x38E000 = 3 727 360            (draft)
clúster 1500 → 0x5DC000 = 6 144 000            (scratch)
```

Las tres posiciones coinciden exactamente con cabeceras `FBLK` en `unalloc.raw`,
lo que confirma el tamaño de clúster y descarta falsos positivos.

## 3. Formato del artefacto `FBLK`

En `0xF0000` (clúster 240):

```
46 42 4c 4b              "FBLK" (magic)
01 00 00 00              versión 1
9e 00 00 00              longitud del JSON de cabecera = 0x9E
{"product":"Frostbook","kind":"cold_ledger",
 "token_xor_hex":"202e2d2c...23203b",
 "xor_hint":"FBLK","batch":"q1-night"}
<datos del libro cifrados>
```

El propio artefacto indica cómo recuperar el token: `token_xor_hex` está cifrado
con **XOR usando la clave `xor_hint` = `FBLK`** (repetición de la magic).

## 4. Recuperación del token

```
hex : 20 2e 2d 2c 3d 24 3e 24 35 36 2e 24 29 29 13 27 23 26 2b 2e 34 1d 2f 39 25 1d 23 20 3b
key : 46 42 4c 4b 46 42 4c 4b 46 42 4c 4b 46 42 4c 4b 46 42 4c 4b 46 42 4c 4b 46 42 4c 4b
xor : 66 6c 61 67 7b 66 72 6f 73 74 62 6f 6f 6b 5f 6c 65 64 67 65 72 5f 63 72 63 5f 6f 6b 7d
```

→ **`flag{ejemplo}`**

Señuelos encontrados y descartados:

- clúster 910 (`draft_ledger`, batch `q1-draft`): `token_xor_hex = "deadbeef"`.
- clúster 1500 (`scratch`, batch `tmp`): `token_xor_hex = "cafebabe"`.

## 5. Metodología (resumen)

1. Leer `mft.csv`/`usn.csv` → identificar el archivo real por nombre, estado
   borrado, secuencia y cronología (create → overwrite → delete).
2. Convertir `DataRun` (clúster) a offset: `clúster × 4096`.
3. Buscar firmas `FBLK` en `unalloc.raw` (magic + versión 1 + JSON válido) y
   cruzar offsets con los DataRun → 3 artefactos, 2 señuelos.
4. Parsear la cabecera JSON y aplicar XOR con `xor_hint`.
5. Validar con el formato `flag{...}`.

## 6. Artefactos generados

- `scan.py` — búsqueda de cadenas (`flag{`, `frostbook`, ...).
- `hexdump.py` — volcado del clúster 240 y del draft.
- `fblk.py` — parser inicial del formato.
- `scan_fblk.py` — parser robusto: enumeración de los 3 artefactos + decodificación.

## 7. Notas de remediación (contexto real)

- El borrado lógico (MFT/USN `FILE_DELETE`) no destruye datos: sin
  sobreescritura segura ni cifrado en reposo, el contenido permanece en espacio
  no asignado y es recuperable.
- Para datos financieros: cifrado en reposo (BitLocker/EFS), borrado seguro o
  crypto-shredding, y retención/backups verificados.
- El formato "seguridad por oscuridad" (token XOR con la propia magic) es
  trivialmente reversible; usar AEAD (AES-GCM) con clave gestionada aparte.
- Conservar y correlacionar MFT + USN + `$LogFile` para reconstruir la línea de
  tiempo del borrado.
