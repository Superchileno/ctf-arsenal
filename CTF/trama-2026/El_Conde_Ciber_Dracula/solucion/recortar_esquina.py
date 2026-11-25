#!/usr/bin/env python3
"""
Desafío 12 - El Conde Ciber-Drácula
Recorta la marca/​fragmento de la esquina inferior derecha del slide usando el
CANAL VERDE (el texto es verde tenue sobre fondo oscuro) y prepara la imagen
para OCR.

Uso: python3 recortar_esquina.py <carpeta_frames> <carpeta_salida> [x0 y0 x1 y1]
"""
import glob
import os
import sys

from PIL import Image, ImageOps

SRC = sys.argv[1] if len(sys.argv) > 1 else "dvr"
OUT = sys.argv[2] if len(sys.argv) > 2 else "esquinas"
if len(sys.argv) >= 7:
    CAJA = tuple(int(v) for v in sys.argv[3:7])
else:
    CAJA = (1135, 622, 1240, 650)   # marca en la esquina del slide (1280x720)
ESCALA = 10

os.makedirs(OUT, exist_ok=True)
n = 0
for ruta in sorted(glob.glob(os.path.join(SRC, "*.png"))):
    base = os.path.basename(ruta).replace(".png", "")
    img = Image.open(ruta).convert("RGB")
    if img.size != (1280, 720):
        img = img.resize((1280, 720), Image.LANCZOS)
    g = img.crop(CAJA).split()[1]                 # canal verde
    g = ImageOps.autocontrast(g)
    g = g.resize((g.width * ESCALA, g.height * ESCALA), Image.LANCZOS)
    g.save(os.path.join(OUT, base + ".png"))
    n += 1
print(f"[+] recortes: {n} -> {OUT} (caja {CAJA})")
