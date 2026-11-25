#!/usr/bin/env python3
"""
Desafío 02 - La Mansión Blackwood
Extrae el mensaje oculto en el bit menos significativo (LSB) del PNG.

Orden correcto: píxel a píxel, fila a fila, canal R -> G -> B, bit 0.
Equivalente a: numpy array.reshape(-1) y tomar (valor & 1).
"""
import re
import sys

import numpy as np
from PIL import Image

IMG = sys.argv[1] if len(sys.argv) > 1 else "casaembrujada.png"
BIT = int(sys.argv[2]) if len(sys.argv) > 2 else 0

arr = np.array(Image.open(IMG).convert("RGB"))
bits = ((arr.reshape(-1) >> BIT) & 1).astype(np.uint8)   # R,G,B por píxel, row-major
data = np.packbits(bits).tobytes()

# El mensaje empieza en el primer bit; cortamos en la primera cadena imprimible
m = re.match(rb"[\x20-\x7e]{4,}", data)
if m:
    print(f"[+] bit LSB = {BIT}")
    print(f"[+] mensaje: {m.group(0).decode()}")
else:
    print("[-] no se encontró texto imprimible en el inicio del stream")
