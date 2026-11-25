import numpy as np
from scipy.io import wavfile

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
f0 = 110.25
win = 512            # 11.6 ms -> mejor resolucion temporal
hop = 128
fr = np.lib.stride_tricks.sliding_window_view(x, win)[::hop] * np.hanning(win)
n = np.fft.rfftfreq(win, 1/rate)
F = np.abs(np.fft.rfft(fr, axis=1))

hs = np.arange(20, 38)   # 2.2 - 4.1 kHz
amps = np.array([F[:, np.argmin(np.abs(n-h*f0))] for h in hs]).T
A = 20*np.log10(amps+1e-9)

# referencia por frame = maximo entre armonicos de la banda
ref = A.max(axis=1, keepdims=True)
R = A - ref                  # dB relativo al armonico mas fuerte del frame

def show(t0, t1, ncols, thr=1.5):
    a, b = int(t0*rate/hop), int(t1*rate/hop)
    sub = R[a:b]
    ci = np.linspace(0, sub.shape[0], ncols+1).astype(int)
    print(f"\n--- {t0}-{t1}s (thr {-thr} dB) ---")
    for h in range(sub.shape[1]-1, -1, -1):
        row = []
        for c in range(ncols):
            s, e = ci[c], max(ci[c]+1, ci[c+1])
            v = np.median(sub[s:e, h])
            row.append("#" if v > -thr else " ")
        line = "".join(row)
        print(f"{hs[h]*f0:5.0f}|{line}")
        print(f"     |{line}")

show(0.52, 1.58, 106, 1.5)
