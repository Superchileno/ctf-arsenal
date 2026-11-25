#!/usr/bin/env python3
"""
Pirata 1 — buscador de señales ocultas:
  * espectro mediano (tonos persistentes sobresalen)
  * «estacionariedad» por bin (una línea horizontal delata texto/tono)
  * lista de bins anómalos por encima de 4 kHz
"""
import wave
from pathlib import Path

import numpy as np

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
with wave.open(str(W / "senal_malapata.wav")) as w:
    fr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64)

NFFT, HOP = 8192, 2048
ventana = np.hanning(NFFT)
n = (len(x) - NFFT) // HOP
print(f"tramas: {n} (resolución {fr/NFFT:.1f} Hz, salto {HOP/fr*1000:.0f} ms)")
mag = np.empty((n, NFFT // 2 + 1), dtype=np.float32)
for i in range(n):
    seg = x[i*HOP:i*HOP+NFFT] * ventana
    mag[i] = np.abs(np.fft.rfft(seg))
fre = np.fft.rfftfreq(NFFT, 1/fr)

mediana = np.median(mag, axis=0)
# estacionariedad: fracción de tramas en que el bin está entre los 20 mayores
umbral = np.partition(mag, -20, axis=1)[:, -20][:, None]
pico = (mag >= umbral).mean(axis=0)

print("\ntop 15 bins por espectro mediano (Hz, valor, pico%):")
for idx in np.argsort(mediana)[-15:][::-1]:
    print(f"  {fre[idx]:8.1f} Hz  med={mediana[idx]:8.1f}  pico={pico[idx]*100:5.1f}%")

print("\ntop 15 bins por estacionariedad (solo >4 kHz):")
cand = [i for i in range(len(fre)) if fre[i] > 4000]
for idx in sorted(cand, key=lambda i: -pico[i])[:15]:
    print(f"  {fre[idx]:8.1f} Hz  pico={pico[idx]*100:5.1f}%  med={mediana[idx]:8.1f}")

# RMS por trama para detectar secciones añadidas
rms = np.sqrt((mag**2).mean(axis=1))
print("\ntramas con RMS más alto:", np.argsort(rms)[-5:][::-1] * HOP / fr)
np.save(W / "mag.npy", mag)
np.save(W / "fre.npy", fre)
print("guardado mag.npy")
