#!/usr/bin/env python3
"""Comprueba si hay bytes ocultos entre entradas del ZIP (huecos) o en los datos."""
import struct
from pathlib import Path

DOCX = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/acta_henry_every.docx")
d = DOCX.read_bytes()
pos = 0
while True:
    pos = d.find(b"PK\x03\x04", pos)
    if pos < 0:
        break
    (ver, flags, comp, t, f, crc, csize, usize, nlen, elen) = struct.unpack("<HHHHHIIIHH", d[pos+4:pos+30])
    nombre = d[pos+30:pos+30+nlen].decode("utf-8", "replace")
    inicio_datos = pos + 30 + nlen + elen
    fin_datos = inicio_datos + csize
    # el siguiente PK\x03\x04 o el descriptor de datos
    siguiente = d.find(b"PK\x03\x04", fin_datos)
    hueco = siguiente - fin_datos if siguiente > 0 else -1
    print(f"{nombre:42s} datos {inicio_datos}-{fin_datos} hueco_hasta_siguiente={hueco}")
    pos = fin_datos
