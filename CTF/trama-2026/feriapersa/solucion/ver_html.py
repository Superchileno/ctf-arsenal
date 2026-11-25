#!/usr/bin/env python3
"""Vuelca a texto legible las páginas descargadas del sitio."""
import glob
import os
import re
import sys
from html import unescape

W = "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/feriapersa/work"

def texto(html: str) -> str:
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?i)</(p|div|li|h[1-6]|tr|section|article|header|footer|form)>", "\n", html)
    html = re.sub(r"<[^>]+>", " ", html)
    html = unescape(html)
    lineas = [re.sub(r"[ \t]+", " ", l).strip() for l in html.splitlines()]
    return "\n".join(l for l in lineas if l)

for ruta in sys.argv[1:]:
    print("=" * 70)
    print(ruta)
    print("=" * 70)
    print(texto(open(ruta, encoding="utf-8", errors="replace").read()))
