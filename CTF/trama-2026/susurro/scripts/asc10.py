import numpy as np
from scipy.io import wavfile

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
f0 = 110.25
win = 1024
hop = 64
fr = np.lib.stride_tricks.sliding_window_view(x, win)[::hop] * np.hanning(win)
n = np.fft.rfftfreq(win, 1/rate)
F = np.abs(np.fft.rfft(fr, axis=1))

hs = np.array([30, 31, 32, 33, 34, 35, 36])   # 3.31 - 3.97 kHz -> 7 filas
amps = np.array([F[:, np.argmin(np.abs(n-h*f0))] for h in hs]).T
A = 20*np.log10(amps+1e-9)
print("niveles p50/p90 por fila:", [(h, round(np.percentile(A[:,i],50),1), round(np.percentile(A[:,i],90),1)) for i,h in enumerate(hs)])

# referencia: por frame, el maximo de la banda
ref = A.max(axis=1, keepdims=True)
R = A - ref

def show(t0, t1, ncols, thr, label):
    a, b = int(t0*rate/hop), int(t1*rate/hop)
    sub = R[a:b]
    ci = np.linspace(0, sub.shape[0], ncols+1).astype(int)
    print(f"\n=== {label}   ({t0}-{t1}s, {ncols} cols, thr -{thr} dB) ===")
    grid = []
    for h in range(sub.shape[1]-1, -1, -1):
        row = []
        for c in range(ncols):
            s, e = ci[c], max(ci[c]+1, ci[c+1])
            v = np.median(sub[s:e, h])
            row.append("#" if v > -thr else ".")
        grid.append("".join(row))
    for r in grid:
        print("  " + r)

# 0.5-4.85s en 110 columnas = 39.5 ms/col
show(0.50, 4.85, 110, 1.0, "A")
show(0.50, 4.85, 110, 2.5, "B")
show(0.50, 4.85, 110, 5.0, "C")
