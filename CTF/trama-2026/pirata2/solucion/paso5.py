#!/usr/bin/env python3
"""Anomalías del contenedor ZIP y de las partes poco visibles."""
import re
import struct
import zipfile
from pathlib import Path

DOCX = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/acta_henry_every.docx")
datos = DOCX.read_bytes()

# --- comentario global del ZIP -------------------------------------------
i = datos.rfind(b"PK\x05\x06")
coment_len = int.from_bytes(datos[i+20:i+22], "little")
coment = datos[i+22:i+22+coment_len]
print(f"comentario ZIP: {coment!r}")

# --- extra fields de cada cabecera local ---------------------------------
pos = 0
print("\ncabeceras locales:")
while True:
    pos = datos.find(b"PK\x03\x04", pos)
    if pos < 0:
        break
    (ver, flags, comp, t, f, crc, csize, usize, nlen, elen) = struct.unpack("<HHHHHIIIHH", datos[pos+4:pos+30])
    nombre = datos[pos+30:pos+30+nlen].decode("utf-8", "replace")
    extra = datos[pos+30+nlen:pos+30+nlen+elen]
    if extra:
        print(f"  {nombre:40s} extra={extra!r}")
    pos += 4

with zipfile.ZipFile(DOCX) as z:
    for n in ("word/footnotes.xml", "word/endnotes.xml"):
        x = z.read(n).decode("utf-8", "replace")
        print(f"\n=== {n} ===")
        print(re.sub(r"\s+", " ", x)[:1200])

    print("\n=== nombres/valores raros en styles.xml ===")
    s = z.read("word/styles.xml").decode("utf-8", "replace")
    for m in re.finditer(r'w:(name|styleId)="([^"]{12,})"', s):
        v = m.group(2)
        if not v.startswith(("Normal", "Tabla", "Título", "Encabezado", "Piedepgina", "Default")):
            print("   ", m.group(1), v)
