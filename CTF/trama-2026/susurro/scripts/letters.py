import numpy as np
from scipy.io import wavfile

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
f0 = 110.25
win = 1024
hop = 64
fr = np.lib.stride_tricks.sliding_window_view(x, win)[::hop] * np.hanning(win)
n = np.fft.rfftfreq(win, 1/rate)
F = np.abs(np.fft.rfft(fr, axis=1))

hs = np.arange(20, 40)            # 2.2 - 4.4 kHz
amps = np.array([F[:, np.argmin(np.abs(n-h*f0))] for h in hs]).T
A = 20*np.log10(amps+1e-9)
print("filas:", [(int(h), round(h*f0)) for h in hs])

# bursts del analisis de envolvente
bursts = [(0.569,0.818),(0.851,1.063),(1.087,1.362),(1.458,1.534),
          (1.939,2.160),(2.184,2.459),(2.474,2.714),(2.746,2.986),
          (3.028,3.240),(3.300,3.530),(3.563,3.793),(3.844,4.065),
          (4.116,4.337),(4.388,4.609)]

ramp = " .:-=+*#%@"
def letter(t0, t1, ncols=18, thr_db=3.0):
    a, b = int(t0*rate/hop), int(t1*rate/hop)
    sub = A[a:b]
    ref = sub.max(axis=1, keepdims=True)      # por frame, el armonico mas fuerte
    R = sub - ref
    ci = np.linspace(0, R.shape[0], ncols+1).astype(int)
    rows = []
    for h in range(R.shape[1]-1, -1, -1):
        line = ""
        for c in range(ncols):
            s, e = ci[c], max(ci[c]+1, ci[c+1])
            v = np.median(R[s:e, h])
            line += "#" if v > -thr_db else "."
        rows.append(line)
    return rows

allrows = {}
for i,(t0,t1) in enumerate(bursts):
    r = letter(t0,t1)
    allrows[i] = r
    print(f"\n--- burst {i}  {t0:.3f}-{t1:.3f}s ---")
    for k,line in enumerate(r):
        print(f"{hs[len(hs)-1-k]*f0:5.0f}|{line}")

# tira horizontal de todas las letras en 7 filas centrales
print("\n\n===== TIRA (filas h26..h33) =====")
sel = list(range(len(hs)-1, -1, -1))
band = [i for i,h in enumerate(hs) if 26 <= h <= 33]
for h in sorted(band, reverse=True):
    row = ""
    for i in range(len(bursts)):
        r = allrows[i]
        k = len(hs)-1-hs.tolist().index(h)
        row += r[k] + " "
    print(f"{h*f0:5.0f}|{row}")
