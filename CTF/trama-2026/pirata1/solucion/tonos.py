#!/usr/bin/env python3
"""
Pirata 1 — detector de tonos persistentes (Morse / balizas).
Para cada trama mide cuánto sobresale cada bin respecto de sus vecinos (±5 bins).
Un tono fijo (aunque esté bajo la voz) destaca siempre en la misma frecuencia.
"""
from pathlib import Path

import numpy as np

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
mag = np.load(W / "mag.npy")          # (tramas, bins), hop 46 ms
fre = np.load(W / "fre.npy")
n, nb = mag.shape
print("tramas:", n, "bins:", nb)

# mediana móvil de 11 bins como "fondo local"
from numpy.lib.stride_tricks import sliding_window_view
relleno = np.pad(mag, ((0, 0), (5, 5)), mode="edge")
ventanas = sliding_window_view(relleno, 11, axis=1)      # (n, nb, 11)
fondo = np.median(ventanas, axis=2)
ratio = mag / np.maximum(fondo, 1e-6)

conteo = (ratio > 15).sum(axis=0)
top = np.argsort(conteo)[-25:][::-1]
print("\nfrecuencias con más tramas de «pico estrecho fuerte»:")
for i in top:
    print(f"  {fre[i]:8.1f} Hz  tramas={conteo[i]:5d}  ({conteo[i]/n*100:4.1f}%)  "
          f"ratio_med={np.median(ratio[:, i]):6.1f}")

# ¿alguna frecuencia con picos en una ventana temporal concreta?
best = top[0]
idx = np.flatnonzero(ratio[:, best] > 15)
if len(idx):
    print(f"\nla mejor ({fre[best]:.0f} Hz) aparece en {len(idx)} tramas, "
          f"de t={idx[0]*0.046:.1f}s a t={idx[-1]*0.046:.1f}s")
    # agrupar en rachas
    rachas, ini = [], idx[0]
    for a, b in zip(idx, idx[1:]):
        if b - a > 10:
            rachas.append((ini*0.046, a*0.046))
            ini = b
    rachas.append((ini*0.046, idx[-1]*0.046))
    print("rachas (s):", [(round(a, 1), round(b, 1)) for a, b in rachas[:15]])
