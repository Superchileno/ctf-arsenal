#!/usr/bin/env python3
"""
Pirata 1 — espectrograma normalizado por bin.
El espectrograma global (ffmpeg) normaliza con el máximo: una señal oculta débil
queda negra. Aquí se resta a cada bin su mediana temporal y se realza lo que
aparece solo en algunos instantes (texto dibujado, tonos, pulsos).
"""
from pathlib import Path

import numpy as np
from PIL import Image

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
mag = np.load(W / "mag.npy")
fre = np.load(W / "fre.npy")
print("matriz:", mag.shape, "resolución:", fre[1] - fre[0], "Hz")

med = np.median(mag, axis=0)
resto = mag - med                      # lo que sobra sobre el fondo de cada bin
resto = np.clip(resto, 0, None)
print("máximo residuo:", resto.max())

def render(lo, hi, nombre, alto=800, gamma=0.5):
    sel = (fre >= lo) & (fre <= hi)
    sub = resto[:, sel]
    # normalizar por columna (cada instante) para ver estructura
    maxcol = sub.max(axis=0, keepdims=True)
    maxcol[maxcol == 0] = 1
    img = np.power(np.clip(sub / maxcol, 0, 1), gamma)
    img = (img.T[::-1] * 255).astype(np.uint8)      # filas = frecuencia (alta arriba)
    im = Image.fromarray(img)
    im = im.resize((3000, alto), Image.LANCZOS)
    im.save(W / "esp" / f"norm_{nombre}.png")
    print("guardado", nombre, sub.shape)

render(0, 4000, "0_4k")
render(4000, 8000, "4_8k")
render(8000, 16000, "8_16k")
render(0, 1200, "0_1200")
