#!/usr/bin/env python3
"""Chunks del PNG y búsqueda de texto en metadatos de todas las partes."""
import re
import struct
import zipfile
from pathlib import Path

PNG = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/docx/word/media/image1.png")
d = PNG.read_bytes()
pos = 8
print("chunks PNG:")
while pos < len(d):
    ln = struct.unpack(">I", d[pos:pos+4])[0]
    tipo = d[pos+4:pos+8].decode("latin1")
    cuerpo = d[pos+8:pos+8+ln]
    print(f"  {tipo} len={ln}" + (f"  {cuerpo[:80]!r}" if tipo not in ("IDAT",) else ""))
    pos += 12 + ln
    if tipo == "IEND":
        break

DOCX = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/acta_henry_every.docx")
print("\nposibles cadenas largas sin espacios en todas las partes:")
with zipfile.ZipFile(DOCX) as z:
    for n in z.namelist():
        if not n.endswith((".xml", ".rels")):
            continue
        x = z.read(n).decode("utf-8", "replace")
        for m in re.finditer(r">([A-Za-z0-9+/=_-]{16,})<", x):
            s = m.group(1)
            if "http" in s or s.startswith(("w:", "a:", "pic:")):
                continue
            print(f"   {n}: {s[:100]}")
