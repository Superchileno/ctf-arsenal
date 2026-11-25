#!/usr/bin/env python3
"""
Pirata 1 — detector DTMF de barrido completo.
Busca pares de frecuencias DTMF simultáneos y estables (>40 ms) y decodifica dígitos.
"""
import wave
from pathlib import Path

import numpy as np

W = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
with wave.open(str(W / "senal_malapata.wav")) as w:
    fr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64)

FILAS = [697, 770, 852, 941]
COLS = [1209, 1336, 1477, 1633]
TECLAS = [["1", "2", "3", "A"], ["4", "5", "6", "B"],
          ["7", "8", "9", "C"], ["*", "0", "#", "D"]]

N = 1024
HOP = 256
ventana = np.hanning(N)
n = (len(x) - N) // HOP
print(f"tramas: {n}, ventana {N/fr*1000:.1f} ms, salto {HOP/fr*1000:.1f} ms")

# energía Goertzel simple por FFT de la ventana
mag = np.empty((n, N // 2 + 1), dtype=np.float32)
for i in range(n):
    mag[i] = np.abs(np.fft.rfft(x[i*HOP:i*HOP+N] * ventana))
fre = np.fft.rfftfreq(N, 1/fr)

def nivel(f):
    i = int(round(f / (fr / N)))
    return mag[:, max(0, i-1):i+2].max(axis=1)

fil = np.stack([nivel(f) for f in FILAS])   # 4 x n
col = np.stack([nivel(f) for f in COLS])    # 4 x n
print("nivel medio filas:", fil.mean(axis=1).round(0))
print("nivel medio cols:", col.mean(axis=1).round(0))

# comprobar simultaneidad: mejor fila y mejor columna, y que ambas destaquen
i_f = fil.argmax(axis=0)
i_c = col.argmax(axis=0)
v_f = fil.max(axis=0)
v_c = col.max(axis=0)
fuerte = (v_f > np.percentile(v_f, 99.0)) & (v_c > np.percentile(v_c, 99.0))

estado = np.where(fuerte, i_f * 4 + i_c, -1).astype(np.int16)
# segmentos estables
digitos = []
i = 0
while i < n:
    if estado[i] >= 0:
        j = i
        while j < n and estado[j] == estado[i]:
            j += 1
        dur = (j - i) * HOP / fr
        if dur >= 0.04:
            idx = estado[i]
            digitos.append((round(i * HOP / fr, 2), round(dur, 3),
                            TECLAS[idx // 4][idx % 4]))
        i = j
    else:
        i += 1

print(f"\nposibles tonos DTMF: {len(digitos)}")
for d in digitos[:60]:
    print(f"  t={d[0]:8.2f}s  dur={d[1]:.3f}s  tecla={d[2]}")
print("secuencia:", "".join(d[2] for d in digitos))
