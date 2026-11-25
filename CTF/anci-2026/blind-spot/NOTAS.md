# ANCI — Reto "Blind Spot" (HackRocks)

**URL:** https://<host>/blind-spot/
**Formato flag:** `flag{..}`
**Objetivo:** token almacenado en el entorno (variable de entorno del contenedor).

## Enunciado (resumen)

Plataforma institucional de intercambio de información. Tiene una herramienta de
"vista previa" que recibe documentos **YAML** y devuelve una representación
normalizada de su estructura. La pista: "qué podría ocurrir si un usuario utiliza
funcionalidades de una manera distinta de la prevista" → abuso de la
deserialización / del parser.

## Estado (2026-10-29 13:5x UTC)

Servicio **caído / saturado**. Evidencia:

| Petición | Resultado |
|---|---|
| `GET /` | `403 Forbidden` (nginx, 146 bytes) |
| `GET /blind-spot` | `301` → `/blind-spot/` |
| `GET /blind-spot/` | cuelga y luego `504 Gateway Time-out` (~60 s, nginx) |
| `GET /blind-spot/{health,api,docs,openapi.json,preview,static/,favicon.ico}` | ReadTimeout (upstream no responde) |
| `GET /api` (raíz) | `502 Bad Gateway` |
| `GET /login`, `/robots.txt` | `404` |

Lectura: nginx está vivo, el upstream (contenedor de la app) no responde. Se
reintenta más tarde (ver `check.py`).

## Hipótesis principal

La "vista previa YAML" es casi con seguridad **deserialización YAML insegura**
(PyYAML `yaml.load()` sin `SafeLoader`, o `FullLoader`/`UnsafeLoader`), lo que
permite **RCE** al construir objetos Python desde el documento:

- `!!python/object/apply:os.system ["..."]`  → ejecución directa
- `!!python/object/apply:subprocess.check_output [[...]]` → salida en el render
- `!!python/object/new:...` / `!!python/object/apply:builtins.eval` → variantes

Como pide "token almacenado en el entorno", el payload debería leer
`os.environ` (o `/proc/self/environ`) y devolverlo en la respuesta normalizada.

Hipótesis alternativas (a descartar cuando vuelva):
1. **SSRF** vía etiquetas/anchors o `!include` (si el parser resuelve URLs).
2. **XXE/entidades** si internamente convierte YAML→XML.
3. **Path traversal / lectura de ficheros** en el nombre del documento.
4. RCE **ciega** (de ahí "blind spot"): sin salida en la respuesta, exfiltración
   OOB por DNS/HTTP a un listener propio.

## Plan de explotación (cuando el servicio responda)

1. `python check.py` → confirmar que `/blind-spot/` responde 200 y volcar el HTML
   para identificar el endpoint real del formulario (`action`, JS `fetch`).
2. Enviar un YAML benigno y ver el formato de la "representación normalizada"
   (así se sabe dónde aparecería la salida del comando).
3. Escalar payloads en este orden:
   - `!!python/name:os.system` / `!!python/object/apply:os.system ["id"]`
   - `!!python/object/apply:subprocess.check_output [["id"]]`
   - lectura de entorno: `["/bin/sh","-c","env"]` o `os.environ`
   - si no hay salida → variante OOB (ver `payloads.yaml`) con listener
     (`python -m http.server` / `ncat -lvnp` / interactsh).
4. Extraer `flag{...}` del entorno y registrarlo aquí.

## Payloads preparados

Ver `payloads.yaml` (comentado). No enviar nada hasta confirmar que el endpoint
está arriba.

## Autorización

Reto CTF público de HackRocks; pruebas limitadas a `<host>`.
