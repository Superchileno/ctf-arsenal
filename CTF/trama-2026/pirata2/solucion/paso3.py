#!/usr/bin/env python3
"""
Pirata 2 — tercera pasada.
1. Todo el texto de todas las partes (doc, header, footer, notes).
2. Caracteres invisibles / espacios raros (estego de whitespace, zero-width).
3. LSB del PNG del encabezado (planos R/G/B y alfa) buscando texto.
"""
import re
import zipfile
from collections import Counter
from pathlib import Path

from PIL import Image

DOCX = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/acta_henry_every.docx")

with zipfile.ZipFile(DOCX) as z:
    partes = [n for n in z.namelist() if n.endswith(".xml") and n.startswith("word/")]
    print("=== texto por parte ===")
    for n in partes:
        x = z.read(n).decode("utf-8", "replace")
        textos = re.findall(r"<w:t[^>]*>(.*?)</w:t>", x, re.S)
        if any(t.strip() for t in textos):
            print(f"--- {n}")
            for t in textos:
                if t.strip():
                    print(f"    {t!r}")

    print("\n=== caracteres invisibles en todo el paquete ===")
    invisibles = {"\u200b": "ZWSP", "\u200c": "ZWNJ", "\u200d": "ZWJ", "\ufeff": "BOM",
                  "\u2060": "WJ", "\u00a0": "NBSP", "\u2007": "FIGSP", "\u202f": "NNBSP"}
    for n in z.namelist():
        if not n.endswith((".xml", ".rels")):
            continue
        x = z.read(n).decode("utf-8", "replace")
        c = Counter(ch for ch in x if ch in invisibles)
        if c:
            print(f"  {n}: {[(invisibles[k], v) for k, v in c.items()]}")

    print("\n=== docProps/app.xml ===")
    print(z.read("docProps/app.xml").decode())

# --- LSB del PNG ----------------------------------------------------------
img = Image.open(DOCX.parent / "docx/word/media/image1.png").convert("RGB")
ancho, alto = img.size
print(f"\nPNG {ancho}x{alto}")
px = list(img.getdata())

for canal, nombre in ((0, "R"), (1, "G"), (2, "B")):
    bits = [p[canal] & 1 for p in px]
    for orden, etiqueta in ((list, "msb-first"), (lambda b: b[::-1], "reversed")):
        bs = orden(bits)
        by = bytes(int("".join(str(b) for b in bs[i:i+8]), 2) for i in range(0, len(bs) - 7, 8))
        imprimible = sum(32 <= b < 127 for b in by[:200])
        if imprimible > 60:
            print(f"  plano {nombre} {etiqueta}: {by[:120]!r}")
        elif b"TRAMACTF" in by:
            print(f"  plano {nombre} {etiqueta}: FLAG {by[:200]!r}")
