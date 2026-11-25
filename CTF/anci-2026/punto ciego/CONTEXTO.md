# ANCI — CTF "Punto Ciego" (HackRocks / blind-spot)

**Evento:** CTF ANCI — reto web
**Nombre interno:** Punto Ciego (nombre en la plataforma: `blind-spot`)
**URL:** https://<host>/blind-spot/
**Formato de flag:** `flag{..}`
**Objetivo:** recuperar el token almacenado en el entorno de pruebas (variable de entorno del contenedor).
**Fecha de registro:** 2026-10-29
**Estado:** ✅ **RESUELTO** — flag obtenida: `flag{ejemplo}`

> Detalle técnico completo en [`RESOLUCION.md`](RESOLUCION.md).

---

## Enunciado

> Una institución implementó una plataforma de intercambio de información para
> facilitar la integración de sistemas con organizaciones colaboradoras.
>
> Como parte de sus funcionalidades, la plataforma dispone de una herramienta de
> vista previa que permite cargar documentos en formato **YAML** y obtener una
> representación normalizada de su estructura.
>
> Durante una evaluación de seguridad, surgieron dudas respecto de cómo la
> aplicación procesa los documentos recibidos y qué podría ocurrir si un usuario
> utiliza funcionalidades de una manera distinta de la prevista.
>
> Este escenario se inspira en incidentes reales en los que atacantes
> aprovecharon debilidades en aplicaciones web expuestas a Internet para
> comprometer servidores institucionales y acceder a recursos internos.
>
> Tu misión consiste en analizar el funcionamiento de la herramienta de vista
> previa, identificar posibles fallas de seguridad y recuperar el token
> almacenado en el entorno de pruebas.

---

## Credencial de acceso (cookie de sesión)

El reto se entrega con una cookie `access` (JWT HS256) ya emitida:

```
access=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzMjg2MTkwLCJpYXQiOjE3OTMyNzUyMTcsImp0aSI6IjliMTlkMDUwNjZiZDRkZjRiMGYyMzk1NGMwZGQ0OGQ1IiwidXNlcl9pZCI6NzI1ODB9.ujK_nJHs29hFwtRtgNd7IZzLuQNqQeSXgkwaVpUcPHY
```

Payload decodificado:

```json
{
  "token_type": "access",
  "exp": 1793286190,
  "iat": 1793275217,
  "jti": "9b19d05066bd4df4b0f23954c0dd48d5",
  "user_id": 72580
}
```

| Campo | Valor |
|---|---|
| Emitido (iat) | 2026-10-29 12:00:17 UTC |
| Expira (exp) | 2026-10-29 15:03:10 UTC (vigencia ~3 h) |
| Algoritmo | HS256 (secreto desconocido) |
| Usuario | `user_id = 72580` |

Uso en peticiones:

```bash
curl -k -b 'access=<JWT>' https://<host>/blind-spot/
```

---

## Análisis preliminar (corregido tras la explotación)

La pista ("usar la funcionalidad de forma distinta a la prevista") apuntaba a
**deserialización YAML insegura**. Se confirmó en una pila **Node.js**, no Python:

- `express@4.19.2` + `js-yaml@3.14.1`
- `POST /api/preview` hace `yaml.load(source)` → **DEFAULT_FULL_SCHEMA** (acepta
  `!!js/function`, `!!js/regexp`, `!!js/undefined`).
- `expandPreview()` invoca los valores de tipo `function` (`return value()`).

Resultado: RCE no autenticada como `node` → `/flag.txt`
(`flag{ejemplo}`). Detalle en `RESOLUCION.md`.

Hipótesis descartadas: SSRF (`!include`), path traversal en el nombre del
documento y RCE ciega con exfiltración OOB (la respuesta JSON devuelve la salida
directamente, por lo que no fue necesario).

Payloads listos en `../blind-spot/payloads.yaml`.

---

## Estado y bitácora

| Fecha (UTC) | Acción | Resultado |
|---|---|---|
| 2026-10-29 13:5x | `GET /blind-spot/` (sin cookie) | `504 Gateway Time-out` tras ~60 s; upstream caído |
| 2026-10-29 14:46 | `GET /blind-spot/` (con cookie) | Timeout del cliente; TCP/443 abierto, app no responde |
| 2026-10-29 14:46 | DNS `<host>` | `203.0.113.10` |
| 2026-10-29 14:49 | `GET /blind-spot/`, `/blind-spot/health`, `/blind-spot/api/preview` (con cookie) | `502 Bad Gateway` (nginx, upstream sin respuesta) |
| 2026-10-29 14:49 | `GET /` y `/api/` | `403` y `502` respectivamente |
| 2026-10-29 14:50 | `GET /blind-spot/` (varios reintentos) | `200` intermitente (~1 de cada 12): front "Schema Preview"; upstream inestable |
| 2026-10-29 14:52 | `GET /api/version` | `{"engine":"yaml","mode":"load"}` → `js-yaml` con esquema completo |
| 2026-10-29 14:52 | `POST /api/preview` con `!!js/function` | **RCE confirmada** (`process.env`, `execSync`) |
| 2026-10-29 14:53 | Lectura de `/flag.txt` | **`flag{ejemplo}`** |
| 2026-10-29 14:54 | Lectura de `/app/app.js` y `package.json` | `js-yaml@3.14.1` + `expandPreview()` que invoca funciones |

**Hallazgo:** `yaml.load()` (js-yaml 3.14.1, DEFAULT_FULL_SCHEMA) acepta
`!!js/function` y `expandPreview()` ejecuta el valor → RCE no autenticada como
usuario `node`. Ver `RESOLUCION.md`.

Archivos de esta carpeta:

- `CONTEXTO.md` — enunciado, cookie, hipótesis y bitácora del evento.
- `RESOLUCION.md` — writeup completo: causa raíz, explotación y remediación.
- `exploit.yaml` — payload mínimo que devuelve la flag.
- `solve.py` — automatiza la explotación (`python solve.py`).
- `cli.py` — cliente con reintentos (el upstream falla ~90 % de las peticiones).
- `check.py` — comprobación de disponibilidad del servicio.
- `index.html` — copia del front obtenido.
- `app_source.js` — código de `/app/app.js` extraído vía RCE (análisis de causa raíz).

Análisis previo y artefactos de sondeo: carpeta hermana `../blind-spot/`
(`NOTAS.md`, `check.py`, `probe*.py`, `payloads.yaml`).

---

## Autorización

Reto CTF público de HackRocks. Pruebas limitadas al host
`<host>` y al alcance del reto.
