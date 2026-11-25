# Operación Salitre — SAL-16 · «El barco que zarpó sin pedir permiso»

| Campo | Valor |
|---|---|
| Categoría | Forense / crypto (correlación de registros + AES-256-CTR) |
| Dificultad | Media |
| Puntos | — |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |
| Fecha de resolución | 2026-10-24 |

## Enunciado

TRAMA CTF 2026 · Expediente **SAL-16: Aguas turbias, reloj más turbio**. Una imagen
nocturna de CAM-07 en el muelle 3 de Tocopilla muestra un horario; el rastreo marítimo
registra varios movimientos y la naviera afirma que su información está cifrada. Hay que
determinar qué zarpe corresponde realmente a la evidencia, identificar la sesión vinculada
y recuperar el mensaje escondido. La hora de la cámara no es confiable y hay zarpes
simultáneos en puertos distintos.

## Evidencia entregada

| Archivo | Rol |
|---|---|
| `camara_portuaria.png` | Fotograma CAM-07: **03:17**, «Puerto de Tocopilla — muelle 3» |
| `bitacora_sincronizacion.csv` | Desfase de cada cámara respecto de la hora oficial local |
| `informe_marea_norte.pdf` | Huso del expediente: **UTC-03:00**; el rastreo va en UTC |
| `rastreo_maritimo.csv` | Zarpes con puerto, muelle, hora UTC y MMSI |
| `manifiesto_carga.csv` | Folio, buque, puerto, muelle, contenedor y precinto |
| `registro_accesos.csv` | Alias de turno, credencial, cámara y evento |
| `registros_dns.txt` | Export local de TXT `control.salitre.invalid` (sesiones cifradas) |
| `protocolo_resguardo.txt` | Formato de sobres `_meta`/`_pNN` y derivación de llave |
| `notas_redaccion.txt` | Advertencias: no atribuir zarpes por cercanía horaria |

Paquete: `Operacion_Salitre.zip` (21.105 B,
SHA256 `C3E6ECEC91CB0B57A4FF5FD1E1D7E6F4586AF98A7BC5E26AAB7D165AC658E875`),
extraído en `evidencias/` (copia local de trabajo; el ZIP original se conserva).

## Reconocimiento

- La cámara muestra `03:17` y pertenece a **CAM-07 / Tocopilla / muelle 3**.
- La bitácora de sincronización registra para CAM-07 ese mismo turno:
  `hora_mostrada=03:17`, `hora_oficial_local=03:06`, estado **`adelantado`**
  → el reloj va **11 minutos por delante**.
- El informe declara que los registros locales del puerto están en **UTC-03:00** y que
  el rastreo marítimo está en **UTC** (sin desfase de cámaras).
- En el rastreo hay **dos zarpes a las 06:06Z**: `Arauco Star` (Mejillones, muelle 3)
  y `Nordkapp` (Tocopilla, muelle 3). La coincidencia horaria por sí sola no acredita
  nada: hay que cruzar puerto y muelle.

## Análisis

### 1. Hora real del incidente

```
03:17 (mostrada) − 00:11 (desfase adelantado) = 03:06 local
03:06 local (UTC-03:00) + 03:00            = 06:06Z
```

Cualquier otra lectura falla: usar `03:17` como hora buena lleva a `06:17Z` (no existe
zarpe) y usar `03:06` como si fuera UTC lleva a `03:06Z`.

### 2. Acceso vinculado al lugar y la hora

En `registro_accesos.csv`, el único evento de **CAM-07 (Tocopilla, muelle 3)** a las
**03:06 local** es:

| fecha | hora | puerto | muelle | cámara | alias | credencial | evento |
|---|---|---|---|---|---|---|---|
| 2026-01-16 | 03:06 | Tocopilla | 3 | CAM-07 | **cormoran** | PORT-17 | **habilitacion_extraordinaria** |

El alias `cormoran` es el identificador operativo de la sesión buscada.

### 3. Zarpe real: cruce puerto + muelle

| Buque | Puerto | Muelle | Hora UTC | ¿Coincide? |
|---|---|---|---|---|
| Cordillera | Tocopilla | 3 | 05:44 | ✗ (02:44 local; es el ingreso de `petrel`) |
| Arauco Star | **Mejillones** | 3 | 06:06 | ✗ puerto distinto (señuelo del mismo minuto) |
| Punta Negra | Tocopilla | 3 | 06:01 | ✗ (03:01 local; salida de `gaviota`) |
| **Nordkapp** | **Tocopilla** | **3** | **06:06** | **✓** |
| Mar Austral | Tocopilla | 2 | 06:11 | ✗ muelle distinto |
| Bahia Norte | Tocopilla | 3 | 06:31 | ✗ (03:31 local; ingreso de `merlin`) |

Buque: **Nordkapp** (MMSI 725013117).

### 4. Manifiesto

`Nordkapp` → folio **A-1193**, contenedor **NYKU9087**, precinto MX-656, destino
Manzanillo.

### 5. Sesión DNS y llave

La sesión se nombra con el folio en minúsculas y sin guion: **`a1193`**.
Existen `_meta.cormoran.a1193` y `_p01.._p04.cormoran.a1193`.

```
material = FOLIO|CONTENEDOR|ALIAS|HORA_UTC
         = A-1193|NYKU9087|cormoran|2026-01-16T06:06Z
llave    = SHA256(UTF8(material))
         = 2eb4e3187dfbf22e4f43f475e1ebe93d80303f50102fbd3e06f93dfc7baffc94
IV       = 2f369d8134b6198c5a44970fca376c9e   (de _meta)
algoritmo= AES-256-CTR
```

Segmentos concatenados por `NN`, sin separadores:

```
_p01 3bdaa97ece11dd58a2a6564fd1afe330
_p02 586ee98021bb3e885e96e43ec516018c
_p03 3cbc2770555257ac54957a0471c19b49
_p04 ac5d8f442d
```

Texto plano (53 B):

```
flag{ejemplo}
```

SHA-256 del texto plano: `06a831b2484386efef165b6c9450fc118db469e7204128a16aa176b4c54ef47e`
→ **coincide** con el `sha256` publicado en `_meta.cormoran.a1193`.

## Solución reproducible

```bash
# Windows (Python 3 con cryptography) desde ctf/salitre/
python solucion/descifrar_sesion.py
# Control negativo: descifra las 6 sesiones del export
python solucion/verificar_sesiones.py
```

Salida de `descifrar_sesion.py`:

```
[1] CAM-07 muestra 03:17; desfase 0:11:00 -> local 03:06 -> UTC 2026-01-16T06:06Z
[2] Acceso habilitacion_extraordinaria: alias 'cormoran' (PORT-17)
[3] Zarpe 2026-01-16T06:06:00Z: Nordkapp (Tocopilla, muelle 3)
[4] Manifiesto: folio A-1193, contenedor NYKU9087
[5] Clave = SHA256('A-1193|NYKU9087|cormoran|2026-01-16T06:06Z') = 2eb4e318…7baffc94
[6] SHA-256 verificado: 06a831b2…c54ef47e

FLAG: flag{ejemplo}
```

Con `openssl` (equivalente):

```bash
openssl enc -d -aes-256-ctr \
  -K 2eb4e3187dfbf22e4f43f475e1ebe93d80303f50102fbd3e06f93dfc7baffc94 \
  -iv 2f369d8134b6198c5a44970fca376c9e \
  -in sesion_a1193.hex.bin
```

## Controles anti-señuelo

- **Arauco Star (A-1192 / `azul`, Mejillones muelle 3, 06:06Z)**: su sesión sí descifra
  y el SHA-256 valida, pero el contenido es
  `ACTA_INTERNA: desvio hacia muelle secundario registrado.` Es el cebo del «mismo
  minuto UTC»; el puerto la descarta.
- **Las otras cuatro sesiones** (`petrel` A-1188, `gaviota` A-1191, `farero` A-1194,
  `merlin` A-1197) también descifran y son actas internas sin flag
  (`verificar_sesiones.py`).
- **Llave equivocada** (probado): hora de cámara sin corregir (`06:17Z`), hora local
  usada como UTC (`03:06Z`), folio en minúsculas (`a-1193`) o alias en mayúsculas
  (`CORMORAN`) producen basura y **fallan** el SHA-256 publicado; no hay falso positivo.
- El turno de `albatros` (03:07, CAM-07) no tiene sesión DNS; `azul` (03:06) es de
  Mejillones, no de Tocopilla.

## Artefactos

| Ruta | Contenido |
|---|---|
| `solucion/descifrar_sesion.py` | Cadena completa: bitácora → acceso → zarpe → manifiesto → DNS → AES → flag |
| `solucion/verificar_sesiones.py` | Descifra las 6 sesiones y muestra cuál contiene la flag |
| `work/sesiones_descifradas.txt` | Salida del control negativo (las 6 actas) |
| `work/salida_descifrado.txt` | Traza completa del descifrado correcto |
| `work/sesion_a1193.hex` | Ciphertext concatenado de la sesión (para `openssl`) |
| `work/mensaje_recuperado.txt` | Texto plano recuperado |
| `flag.txt` | Flag |

## Lecciones / notas

- Un desfase de cámara **no invalida el evento**: lo desplaza. Hay que corregir con la
  bitácora antes de cruzar con el rastreo.
- «Misma hora UTC» no es «mismo incidente»: puerto y muelle son la clave para no
  confundir al `Arauco Star` con el `Nordkapp`.
- El cifrado autentica el resultado: el SHA-256 del `_meta` convierte una llave mal
  derivada en un fallo detectable, no en una falsa flag.
- La trampa del enunciado («si el reloj está malo, seguro el barco tampoco salió») es
  una falacia: el reloj miente, pero el rastro del barco no.
