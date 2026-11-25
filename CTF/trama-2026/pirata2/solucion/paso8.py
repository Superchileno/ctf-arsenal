#!/usr/bin/env python3
"""Busca texto en elementos DrawingML (<a:t>) y en cualquier otra etiqueta de texto."""
import re
import zipfile
from pathlib import Path

DOCX = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/acta_henry_every.docx")

with zipfile.ZipFile(DOCX) as z:
    for n in z.namelist():
        if not n.endswith((".xml", ".rels")):
            continue
        x = z.read(n).decode("utf-8", "replace")
        hallazgos = []
        for tag in ("a:t", "w:t", "a:fld", "vt:lpstr", "vt:lpwstr", "dc:description",
                    "cp:keywords", "dc:title", "dc:subject", "cp:category"):
            for m in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", x, re.S):
                v = m.group(1).strip()
                if v:
                    hallazgos.append((tag, v))
        if hallazgos:
            print(f"--- {n}")
            for tag, v in hallazgos:
                print(f"    <{tag}> {v[:200]!r}")
