#!/usr/bin/env python3
"""Realza diferencias sutiles en el PNG (texto casi invisible)."""
from collections import Counter
from pathlib import Path

from PIL import Image

PNG = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/docx/word/media/image1.png")
W = PNG.parent.parent.parent.parent  # .../pirata2/work
img = Image.open(PNG).convert("RGB")
px = img.load()
ancho, alto = img.size

colores = Counter(img.getdata())
print("colores con algún canal entre 235 y 254:")
for c, n in sorted(colores.items()):
    if any(235 <= v <= 254 for v in c) and all(v >= 235 for v in c):
        print("   ", c, n)

salida = Image.new("L", (ancho, alto))
p = salida.load()
for y in range(alto):
    for x in range(ancho):
        r, g, b = px[x, y]
        # cualquier píxel "blanco sucio" que no sea el fondo puro ni el gris base
        if r > 235 and g > 235 and b > 235 and (r, g, b) not in ((255, 255, 255), (245, 245, 245)):
            p[x, y] = 0
        else:
            p[x, y] = 255
salida.save(W / "mask_casi_blanco.png")
print("guardado", W / "mask_casi_blanco.png")
