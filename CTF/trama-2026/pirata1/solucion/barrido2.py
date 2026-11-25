#!/usr/bin/env python3
"""
Pirata 1 — segundo barrido:
  * tramos de silencio digital (muestras a 0) donde suelen esconderse datos;
  * byte bajo / alto de cada muestra como posible ASCII;
  * periodicidad de las muestras (¿ruido insertado?);
  * búsqueda de cabeceras de archivo (PK, PNG, etc.) en las muestras.
"""
import re
import wave
from pathlib import Path

import numpy as np

W = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
with wave.open(str(W / "senal_malapata.wav")) as w:
    fr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.int32)

print("muestras:", len(x), "| ceros:", int((x == 0).sum()), f"({(x == 0).mean()*100:.2f}%)")

# --- tramos de ceros ------------------------------------------------------
cero = (x == 0).astype(np.int8)
cambios = np.flatnonzero(np.diff(cero))
tramos = []
for i in range(0, len(cambios) - 1, 2):
    ini, fin = cambios[i] + 1, cambios[i + 1] + 1
    if cero[ini] and fin - ini > 100:
        tramos.append((ini / fr, (fin - ini) / fr))
print("tramos de silencio (>100 muestras):", tramos[:15], "total", len(tramos))

# --- byte bajo / alto como ASCII -----------------------------------------
for nombre, arr in (("byte bajo", (x & 0xFF)), ("byte alto", ((x >> 8) & 0xFF))):
    b = bytes(int(v) & 0xFF for v in arr[:2000000])
    impr = sum(32 <= c < 127 for c in b) / len(b)
    hits = [m.start() for m in re.finditer(rb"TRAMACTF", b)]
    print(f"{nombre}: imprimibles={impr:.2%} TRAMACTF={hits[:5]}")

# --- cabeceras de archivo dentro de las muestras --------------------------
b = x.astype("<i2").tobytes()
for magic, nombre in ((b"PK\x03\x04", "ZIP"), (b"\x89PNG", "PNG"), (b"%PDF", "PDF"),
                      (b"ID3", "MP3"), (b"OggS", "OGG"), (b"TRAMACTF", "FLAG")):
    pos = b.find(magic)
    print(f"  {nombre}: {pos}")

# --- ¿ruido añadido? energía en banda 18-22k por tramo --------------------
from numpy.fft import rfft, rfftfreq
bloques = len(x) // fr
altos = []
for i in range(bloques):
    seg = x[i*fr:(i+1)*fr].astype(float)
    e = np.abs(rfft(seg))
    f = rfftfreq(len(seg), 1/fr)
    altos.append((i, float(e[(f > 17000)].mean()), float(e.mean())))
altos.sort(key=lambda t: -t[1] / (t[2] + 1e-9))
print("\ntramos con más proporción de 17-22 kHz:")
for t in altos[:8]:
    print("   seg", t[0], "alta=", round(t[1], 1), "media=", round(t[2], 1))
