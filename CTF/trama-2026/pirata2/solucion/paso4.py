#!/usr/bin/env python3
"""Busca contenido textual en etiquetas «no visibles» del OOXML."""
import re
import zipfile
from pathlib import Path

DOCX = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/acta_henry_every.docx")
ETIQUETAS = ["w:delText", "w:instrText", "w:comment", "w:fldSimple", "w:hyperlink",
             "w:bookmarkStart", "w:docPart", "w:altChunk", "w:txbxContent",
             "w:customXml", "w:sdt", "w:proofErr"]

with zipfile.ZipFile(DOCX) as z:
    for n in z.namelist():
        if not n.endswith((".xml", ".rels")):
            continue
        x = z.read(n).decode("utf-8", "replace")
        for et in ETIQUETAS:
            if et in x:
                print(f"{n}: contiene <{et}>")
        for tag in ("w:delText", "w:instrText"):
            for m in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", x, re.S):
                print(f"   {tag}: {m.group(1)!r}")
    print("\n=== settings.xml (recortado) ===")
    s = z.read("word/settings.xml").decode("utf-8", "replace")
    for m in re.finditer(r"<w:(documentProtection|attachedTemplate|rsid|zoom|defaultTabStop|trackChanges|doNotTrackMoves|removePersonalInformation)[^>]*>", s):
        print("  ", m.group(0))
    print("\n=== document.xml: atributos con texto raro ===")
    d = z.read("word/document.xml").decode("utf-8", "replace")
    for m in re.finditer(r'w:(descr|title|name|val)="([^"]{20,})"', d):
        print(f"   {m.group(1)}={m.group(2)[:120]!r}")
