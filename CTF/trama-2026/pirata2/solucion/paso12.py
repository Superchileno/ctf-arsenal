#!/usr/bin/env python3
"""Imprime el texto del encabezado carácter a carácter (detecta homoglifos)."""
import unicodedata
import zipfile
from pathlib import Path

DOCX = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/acta_henry_every.docx")
with zipfile.ZipFile(DOCX) as z:
    x = z.read("word/header1.xml").decode("utf-8", "replace")
import re
txt = re.search(r"<w:t[^>]*>(.*?)</w:t>", x, re.S).group(1)
print(repr(txt))
print()
for ch in txt:
    cp = ord(ch)
    if cp > 127 or ch in "O0Il1|":
        try:
            nom = unicodedata.name(ch)
        except ValueError:
            nom = "?"
        print(f"  {ch!r} U+{cp:04X} {nom}")
print("\nlongitud:", len(txt))
print("ASCII puro:", txt.isascii())
print("bytes:", txt.encode())
