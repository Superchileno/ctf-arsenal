#!/usr/bin/env python3
"""Busca posicionamiento raro de texto (marcos, offsets, sangrías negativas)."""
import re
from pathlib import Path

D = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/docx")
for parte in ("word/document.xml", "word/header1.xml", "word/footer1.xml"):
    x = (D / parte).read_text(errors="replace")
    print(f"--- {parte}: {len(x)} bytes")
    for et in ("w:framePr", "w:position", "w:ind", "w:sz w:val=\"2\"", "w:sz w:val=\"4\"",
               "w:color", "w:vanish", "w:specVanish"):
        n = x.count(et)
        if n:
            print(f"    {et}: {n}")
    for m in re.finditer(r"<w:ind[^>]*/>", x):
        print("      ", m.group(0))
    for m in re.finditer(r"<w:framePr[^>]*/>", x):
        print("      ", m.group(0))
print()
x = (D / "word/document.xml").read_text(errors="replace")
print("sectPr:", re.findall(r"<w:sectPr.*?</w:sectPr>", x, re.S))
print("\nparrafos:", x.count("<w:p "))
print("runs:", x.count("<w:r>"))
