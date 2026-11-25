#!/usr/bin/env python3
"""Análisis del PNG del encabezado: colores casi-blancos, datos tras IEND, LSB."""
import struct
from collections import Counter
from pathlib import Path

from PIL import Image

PNG = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/docx/word/media/image1.png")
datos = PNG.read_bytes()

iend = datos.rfind(b"IEND")
print(f"IEND en {iend}, tamaño {len(datos)}, cola tras IEND: {len(datos) - (iend+8)} bytes")
if len(datos) > iend + 8:
    print("  cola:", datos[iend+8:iend+120])

img = Image.open(PNG).convert("RGB")
print("tamaño:", img.size)
colores = Counter(img.getdata())
print("colores distintos:", len(colores))
print("top:", colores.most_common(8))

casi = [(c, n) for c, n in colores.items() if any(200 <= v <= 254 for v in c) and all(v >= 200 for v in c)]
print("casi blancos:", len(casi), sum(n for _, n in casi))

# Mapas de bits no estándar: LSB con desplazamiento / bit 2
px = list(img.getdata())
for canal in (0, 1, 2):
    for bit in (0, 1, 2):
        bits = [(p[canal] >> bit) & 1 for p in px]
        for inicio in (0, 1, 2, 3, 4, 5, 6, 7):
            bs = bits[inicio:]
            by = bytes(int("".join(map(str, bs[i:i+8])), 2) for i in range(0, len(bs) - 7, 8))
            if b"TRAMACTF" in by or (sum(32 <= b < 127 for b in by[:80]) > 60 and len(by) > 10):
                print(f"  canal={canal} bit={bit} off={inicio}: {by[:100]!r}")
