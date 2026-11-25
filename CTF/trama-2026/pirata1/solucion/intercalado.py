#!/usr/bin/env python3
"""
Pirata 1 — ¿el «mono» es en realidad dos pistas intercaladas?
Si lo fuera, las muestras pares y las impares tendrían contenidos distintos
(una sería el podcast y la otra el mensaje).
"""
import wave
from pathlib import Path

import numpy as np

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
with wave.open(str(W / "senal_malapata.wav")) as w:
    fr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64)

pares = x[0::2]
impares = x[1::2]
print("pares:", len(pares), "impares:", len(impares))
print("rms pares:", pares.std().round(1), "rms impares:", impares.std().round(1))
print("correlación:", np.corrcoef(pares[:len(impares)], impares)[0, 1].round(4))

# espectros medios de cada mitad
for nombre, s in (("pares", pares), ("impares", impares)):
    esp = np.abs(np.fft.rfft(s[:fr*30]))
    f = np.fft.rfftfreq(fr*30, 1/44100)
    banda = {f"{lo//1000}-{hi//1000}k": esp[(f >= lo) & (f < hi)].mean()
             for lo, hi in ((0, 1000), (1000, 4000), (4000, 8000), (8000, 16000), (16000, 22050))}
    print(nombre, {k: round(v) for k, v in banda.items()})

# diferencia: ¿una mitad contiene algo reconocible?
d = np.abs(pares[:len(impares)] - impares)
print("\ndiferencia media:", d.mean().round(1), "max:", d.max())
