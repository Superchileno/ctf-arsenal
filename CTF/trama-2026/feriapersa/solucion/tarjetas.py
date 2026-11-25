#!/usr/bin/env python3
"""Extrae las tarjetas de una respuesta del buscador (texto plano por tarjeta)."""
import re
import sys
from html import unescape


def tarjetas(html: str):
    out = []
    for m in re.finditer(r'(?s)<article class="producto-card([^"]*)">(.*?)</article>', html):
        clase, cuerpo = m.group(1), m.group(2)
        txt = re.sub(r"<[^>]+>", "|", cuerpo)
        txt = re.sub(r"\|+", "|", unescape(txt)).strip("|")
        img = re.search(r'src="([^"]+)"', cuerpo)
        out.append({"clase": clase, "img": img.group(1) if img else "", "txt": txt})
    return out


if __name__ == "__main__":
    html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    for i, t in enumerate(tarjetas(html), 1):
        print(f"[{i:02d}] clase={t['clase']!r} img={t['img'].split('/')[-1]}")
        print(f"     {t['txt'][:300]}")
