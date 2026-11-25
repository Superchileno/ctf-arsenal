# Desafío 11 — 6puntos ("SEÑAL DETECTADA // ORIGEN DESCONOCIDO")

| Campo | Valor |
|---|---|
| Categoría | OSINT / geolocalización por EXIF + reconstrucción de secuencia |
| Estado | ✅ Resuelto |
| Evidencia | `seis_pulsos.zip` (1.762.380 B) → 6 JPEG de 1440×900 |
| Flag | `flag{ejemplo}` |

## Enunciado (resumen)

Durante **seis días consecutivos**, el nodo **VF0** transmitió una fotografía por jornada.
No había mensajes ni coordenadas declaradas. El índice original se perdió y los nombres de
archivo se regeneraron (`IMG_xxxx`), borrando el orden de emisión. Hay que examinar las
fotos, identificar los seis lugares y reconstruir la secuencia.

## Evidencia

```
work/
├── IMG_19B7.jpg  258 kB
├── IMG_2E8C.jpg  271 kB
├── IMG_7C2E.jpg  276 kB
├── IMG_A91F.jpg  349 kB
├── IMG_D440.jpg  240 kB
└── IMG_F03A.jpg  373 kB
```

Todas: `1440x900`, `Make: TRAMA`, `Model: VF0`, `Software: TRAMA Recovery Engine 2.6`,
`ImageDescription: Recovered image fragment / route index unavailable`.

## Análisis

### 1. El EXIF no fue borrado (y ahí está todo)

La descripción dice «route index unavailable», pero el resto del bloque EXIF sigue intacto:

| Archivo | `DateTimeOriginal` | GPS |
|---|---|---|
| `IMG_7C2E.jpg` | 2026-10-17 03:17 | 33°01'28.20"S, 71°33'06.48"W |
| `IMG_2E8C.jpg` | 2026-10-18 04:21 | 33°40'46.88"S, 70°59'05.35"W |
| `IMG_19B7.jpg` | 2026-10-19 09:13 | 34°58'58.04"S, 71°14'21.95"W |
| `IMG_A91F.jpg` | 2026-10-20 17:04 | 35°25'36.98"S, 71°39'56.02"W |
| `IMG_F03A.jpg` | 2026-10-21 20:26 | 40°34'26.00"S, 73°08'01.00"W |
| `IMG_D440.jpg` | 2026-10-22 23:08 | 40°52'03.50"S, 72°35'13.60"W |

Dos regalos:

- **Fechas**: seis días consecutivos (17→22 de octubre) → el **orden de emisión** se
  reconstruye sin ambigüedad (era justo lo que los nombres de archivo ya no daban).
- **GPS**: seis coordenadas en Chile que bajan en latitud (33,0° → 40,9°) → un recorrido
  **norte → sur**, coherente con la secuencia temporal.

### 2. Geocodificación inversa (Nominatim)

| # | Fecha/hora | Archivo | Coordenadas (decimal) | Municipio | Ciudad de referencia |
|---|---|---|---|---|---|
| 1 | 17-10 03:17 | `IMG_7C2E` | −33.02450, −71.55180 | Viña del Mar | Viña del Mar (Plaza Vergara / calle Arlegui) |
| 2 | 18-10 04:21 | `IMG_2E8C` | −33.67969, −70.98482 | El Monte | El Monte (plaza e Iglesia) |
| 3 | 19-10 09:13 | `IMG_19B7` | −34.98279, −71.23943 | Curicó | Curicó (calle Carmen / Plaza de Armas) |
| 4 | 20-10 17:04 | `IMG_A91F` | −35.42694, −71.66556 | Talca | Talca (1 Oriente / Plaza de Armas) |
| 5 | 21-10 20:26 | `IMG_F03A` | −40.57389, −73.13361 | Osorno | Osorno (Plaza de Armas / Catedral San Mateo) |
| 6 | 22-10 23:08 | `IMG_D440` | −40.86764, −72.58711 | Puerto Octay (comuna) | **Lago Rupanco** (orilla oeste, La Pellinada Alto) |

Validación cruzada: la búsqueda geográfica de Wikipedia/Commons confirma cada punto
(«Plaza Vergara» a 15 m en Viña, «Iglesia de El Monte» a 579 m, «Plaza de Armas de Curicó»
a 276 m, «Plaza de Armas de Talca» a 64 m, «Catedral de San Mateo» a 76 m en Osorno).

### 3. Confirmación visual de las fotos

- `IMG_7C2E`: calle comercial con árboles, cartel **«MARANATHA, CIA — fabricamos puertas,
  ventanas, celosías, bow windows»** y local **NISSAN**.
- `IMG_2E8C`: plaza con palmeras, estatua sobre pedestal, iglesia de ladrillo al fondo y
  cartel municipal verde (`SE PROHÍBE ARROJAR BASURA…`, no es un topónimo).
- `IMG_19B7`: calle de casas continuas con una fachada azul alta, camionetas con patente
  chilena.
- `IMG_A91F`: tacón vehicular bajo plátanos, letrero amarillo **«ESCOLARES»**.
- `IMG_F03A`: casona de madera de dos pisos, letreros **«Maka»** y medallón **Kunstmann**.
- `IMG_D440`: playa de piedras, islote con vegetación, boyas y agua calma con cordillera al
  fondo → orilla del **Lago Rupanco**, sector La Pellinada / Laguna Bonita (comuna de
  Puerto Octay).

### 4. Construcción de la flag

Regla del enunciado: *eliminar tildes y espacios* y *concatenar los seis nombres con `_`*.
La pista del reto («algunas ciudades pueden contener un nombre más corto») apunta a que, dentro de la
comuna de Puerto Octay, el lugar real es el **Lago Rupanco**; se usa su nombre corto, `Rupanco`.

```
Viña del Mar → VinadelMar
El Monte     → ElMonte
Curicó       → Curico
Talca        → Talca
Osorno       → Osorno
Rupanco      → Rupanco
```

Y la comprobación que cierra el diseño: las iniciales forman **VECTOR**, el nombre del CTF
(*Vector Fantasma*):

```
V E C T O R
```

```
flag{ejemplo}
```

## Solución (pasos reproducibles)

```bash
# 1) volcar EXIF de las seis imágenes
bash solucion/extraer_exif.sh

# 2) extraer fecha + GPS, ordenar y geocodificar
python3 solucion/resolver_secuencia.py --online
```

Salida real del script:

```
Secuencia de pulsos (orden por DateTimeOriginal):
 1. 2026:10:17 03:17:00  IMG_7C2E.jpg  -33.02450, -71.55180  -> Viña del Mar
 2. 2026:10:18 04:21:00  IMG_2E8C.jpg  -33.67969, -70.98482  -> El Monte
 3. 2026:10:19 09:13:00  IMG_19B7.jpg  -34.98279, -71.23943  -> Curicó
 4. 2026:10:20 17:04:00  IMG_A91F.jpg  -35.42694, -71.66556  -> Talca
 5. 2026:10:21 20:26:00  IMG_F03A.jpg  -40.57389, -73.13361  -> Osorno
 6. 2026:10:22 23:08:00  IMG_D440.jpg  -40.86764, -72.58711  -> Rupanco
Nombres normalizados: ['VinadelMar', 'ElMonte', 'Curico', 'Talca', 'Osorno', 'Rupanco']
Iniciales: VECTOR
FLAG: flag{ejemplo}
```

### A mano

```bash
exiftool -DateTimeOriginal -GPSPosition work/*.jpg | sort   # orden + coordenadas
# pegar cada coordenada en Nominatim/OSM y anotar el municipio
```

## Notas sobre el punto 6 (la clave del diseño)

La foto 6 está tomada en la **orilla oeste del Lago Rupanco**, en la comuna de
**Puerto Octay** (sector La Pellinada Alto). La geocodificación inversa devuelve `Puerto Octay`,
pero la pista del reto («algunas ciudades pueden contener un nombre más corto») indica que hay que
usar el nombre más corto contenido en esa comuna: **`Rupanco`** (el lago).

La confirmación es elegante: con `Rupanco` las iniciales de los seis lugares forman **VECTOR**,
el nombre del CTF (*Vector Fantasma*):

```
Viña del Mar  -> V
El Monte      -> E
Curicó        -> C
Talca         -> T
Osorno        -> O
Rupanco       -> R
```

Con `Puerto Octay` las iniciales serían `VECTOP` y no cerrarían el patrón. Por eso la flag correcta
lleva `Rupanco` y no `PuertoOctay` ni `LagoRupanco`.

## Lecciones / notas

- **«No hubo coordenadas declaradas»** = las coordenadas no venían en un mensaje, venían
  en el EXIF. Revisar metadatos antes de gastar tiempo en esteganografía (aquí no hay).
- **Borrar el nombre del archivo no borra el tiempo**: `DateTimeOriginal` reconstruye el
  orden. Los timestamps además son consecutivos, lo que valida la hipótesis.
- La **coherencia geográfica** (latitud monótona decreciente, 33°→41°) es una validación
  independiente del orden: si el orden fuera otro, el recorrido no tendría sentido.
- Los carteles de las fotos (MARANATHA, ESCOLARES, Kunstmann/Maka) sirven como control
  visual de que el municipio geocodificado es el correcto.
- El enunciado pide explícitamente **quitar los espacios**, por eso `VinadelMar` y `ElMonte`
  van sin separación interna (los `_` solo separan los seis nombres entre sí).
- **El patrón de iniciales (VECTOR)** es la validación final: si una elección de nombre rompe la
  palabra, esa elección es incorrecta. La pista del «nombre más corto» resuelve la ambigüedad del
  punto 6 a favor de `Rupanco`.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `seis_pulsos.zip` | evidencia original |
| `CONTEXTO.md` | este writeup |
| `flag.txt` | flag final |
| `solucion/resolver_secuencia.py` | EXIF → orden → geocodificación → flag |
| `solucion/extraer_exif.sh` | volcado EXIF de las 6 fotos |
| `solucion/geocodificar.py` | geocodificación inversa (Nominatim) |
| `solucion/recortes.py` | recortes ampliados de carteles/patentes (`work/zoom/`) |
| `solucion/tiles.sh` | tiles OSM del punto 6 (`work/mapa/`) |
| `solucion/salida.txt` | salida del script |
| `work/` | las 6 fotos + `zoom/` + `mapa/` |

## Backups

| Archivo | Backup |
|---|---|
| `ctf/6puntos/CONTEXTO.md` | `ctf/backups/CONTEXTO_6puntos.md.20261023-205751` |
| `ctf/CONTEXTO_CTF.md` (índice) | `ctf/backups/CONTEXTO_CTF.md.20261023-211034` |
