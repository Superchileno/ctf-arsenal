#!/usr/bin/env python3
"""
Desafío 12 - El Conde Ciber-Drácula
Extrae la marca de la esquina inferior derecha del slide (canal verde, umbral
agresivo, escalado nearest) y la deja lista para OCR o lectura visual.

Uso: python3 extraer_marca.py <carpeta_frames> <carpeta_salida>
"""
import glob
import os
import sys

from PIL import Image, ImageOps

SRC = sys.argv[1] if len(sys.argv) > 1 else "dvr"
OUT = sys.argv[2] if len(sys.argv) > 2 else "marcas"
CAJA = (1145, 626, 1250, 652)      # coordenadas del watermark en 1280x720
UMBRAL = 80
ESCALA = 12

os.makedirs(OUT, exist_ok=True)
n = 0
for ruta in sorted(glob.glob(os.path.join(SRC, "*.png"))):
    base = os.path.basename(ruta).replace(".png", "")
    img = Image.open(ruta).convert("RGB")
    if img.size != (1280, 720):
        img = img.resize((1280, 720), Image.LANCZOS)
    g = img.crop(CAJA).split()[1]                    # canal verde
    g = ImageOps.autocontrast(g)
    g = g.point(lambda v: 255 if v >= UMBRAL else 0)
    g = g.resize((g.width * ESCALA, g.height * ESCALA), Image.NEAREST)
    g.save(os.path.join(OUT, base + ".png"))
    n += 1
print(f"[+] marcas: {n} -> {OUT}")
