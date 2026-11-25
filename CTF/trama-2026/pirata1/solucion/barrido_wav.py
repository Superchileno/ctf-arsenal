#!/usr/bin/env python3
"""
Pirata 1 — primer barrido del WAV:
  * energía por banda (¿hay algo por encima de la voz?)
  * LSB de las muestras (bits 0..3) buscando texto
  * diferencias de bit entre muestras consecutivas
"""
import numpy as np
from pathlib import Path
import wave

W = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
ruta = W / "senal_malapata.wav"

with wave.open(str(ruta)) as w:
    n, sw, fr, nf, comp, nombre = w.getparams()
    datos = w.readframes(nf)
print(f"{n} canal(es), {sw*8} bits, {fr} Hz, {nf} frames, {nf/fr:.1f} s, {len(datos)} bytes")

x = np.frombuffer(datos, dtype="<i2").astype(np.int32)
print("muestras:", len(x), "min/max:", x.min(), x.max())

# --- energía por banda en tramas de 1 s -----------------------------------
bloque = fr
nbloques = len(x) // bloque
print(f"\ntramas de 1 s: {nbloques}")
sospechosas = []
for i in range(nbloques):
    seg = x[i*bloque:(i+1)*bloque].astype(np.float64)
    esp = np.abs(np.fft.rfft(seg))
    freqs = np.fft.rfftfreq(len(seg), 1/fr)
    e_alta = esp[(freqs > 10000) & (freqs < 20000)].mean()
    e_total = esp.mean()
    if e_alta > e_total * 0.5 and e_alta > 1:
        sospechosas.append((i, round(e_alta, 1), round(e_total, 1)))
print("tramos con energía >10 kHz comparable al total:", sospechosas[:20], "... total:", len(sospechosas))

# --- LSB --------------------------------------------------------------
def bits_a_texto(bits):
    b = np.packbits(np.array(bits, dtype=np.uint8))
    return b.tobytes()

for bit in range(4):
    bits = ((x >> bit) & 1).astype(np.uint8)
    for off in range(8):
        t = bits_a_texto(bits[off:len(bits) - (len(bits) - off) % 8])
        if b"TRAMACTF" in t:
            print(f"  LSB bit={bit} off={off}: FLAG en bruto")
        elif sum(32 <= c < 127 for c in t[:400]) > 300:
            print(f"  LSB bit={bit} off={off}: {t[:160]!r}")

# --- LSB de la diferencia entre muestras -------------------------------
d = np.abs(np.diff(x))
for bit in range(2):
    bits = ((d >> bit) & 1).astype(np.uint8)
    t = bits_a_texto(bits[:len(bits) - len(bits) % 8])
    if b"TRAMACTF" in t:
        print(f"  diff LSB bit={bit}: FLAG")
    elif sum(32 <= c < 127 for c in t[:400]) > 300:
        print(f"  diff LSB bit={bit}: {t[:160]!r}")

print("\nlisto")
