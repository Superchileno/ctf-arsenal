import numpy as np
from scipy.io import wavfile

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)

# Estimar f0 con precision (autocorrelacion en la zona de mayor energia)
seg = x[int(1.0*rate):int(3.0*rate)]
seg = seg - seg.mean()
ac = np.correlate(seg[:60000], seg[:60000], mode="full")[59999:]
ac /= ac[0]
# buscar pico entre 200 y 600 muestras (73-220 Hz)
lo, hi = 200, 700
lag = lo + np.argmax(ac[lo:hi])
print("lag", lag, "f0", rate/lag)

f0 = rate/lag
win = 4096
hop = 220
frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop]
frames = frames * np.hanning(win) * 2 / win
n = np.fft.rfftfreq(win, 1/rate)
F = np.abs(np.fft.rfft(frames, axis=1))
print("frames", F.shape, "resolucion Hz", n[1])

hs = np.arange(1, int(5000/f0)+1)
amps = []
for h in hs:
    f0h = h*f0
    k = np.argmin(np.abs(n-f0h))
    amps.append(F[:, k-1:k+2].max(axis=1))
A = 20*np.log10(np.array(amps).T + 1e-12)   # (nfr, nharm)
print("A", A.shape)

# normalizar por armonico (cada fila tiene su nivel base)
A = A - np.median(A, axis=0, keepdims=True)
# binarizar
thr = 6  # dB sobre su mediana
B = (A > thr)

def show(sel_t0, sel_t1, hmin, hmax, nh=None):
    t0i = int(sel_t0*rate/hop); t1i = int(sel_t1*rate/hop)
    sub = B[t0i:t1i, hmin:hmax]
    # comprimir tiempo: bloques de n columnas con OR
    ncols = 110
    idx = np.linspace(0, sub.shape[0], ncols+1).astype(int)
    lines = []
    for h in range(sub.shape[1]-1, -1, -1):
        row = []
        for c in range(ncols):
            a, b = idx[c], idx[c+1]
            if b <= a: b = a+1
            frac = sub[a:b, h].mean()
            row.append("#" if frac > 0.5 else ("+" if frac > 0.25 else ("." if frac > 0.05 else " ")))
        lines.append(f"{hs[hmin+h]*f0:5.0f}|" + "".join(row))
    print("\n".join(lines))

print("\n=== armonicos 20-46 (2.1-5.0 kHz), 0.5-2.0s ===")
show(0.5, 2.0, 19, 46)
