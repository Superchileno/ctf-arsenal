import numpy as np
from scipy.io import wavfile

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
f0 = 110.25
win = 2048
hop = 110
frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop]
frames = frames * np.hanning(win)
n = np.fft.rfftfreq(win, 1/rate)
F = np.abs(np.fft.rfft(frames, axis=1))

hs = np.arange(1, int(6000/f0)+1)
amps = []
for h in hs:
    k = np.argmin(np.abs(n - h*f0))
    amps.append(F[:, k-1:k+2].max(axis=1))
A = 20*np.log10(np.array(amps).T + 1e-9)

# normalizar POR FRAME (elimina la envolvente temporal comun)
Z = A - A.mean(axis=1, keepdims=True)
# normalizar por armonico para igualar ruido
Z = Z/ (Z.std(axis=0, keepdims=True)+1e-9)

def show(t0, t1, h0, h1, ncols, title):
    a = int(t0*rate/hop); b = int(t1*rate/hop)
    sub = Z[a:b, h0:h1]
    ci = np.linspace(0, sub.shape[0], ncols+1).astype(int)
    ramp = " .:-=+*#%@"
    print(title)
    for h in range(sub.shape[1]-1, -1, -1):
        row = []
        for c in range(ncols):
            s, e = ci[c], max(ci[c]+1, ci[c+1])
            v = np.mean(sub[s:e, h])
            # v en unidades de sigma
            i = int(np.clip((v+1.5)/3.0, 0, 0.999)*(len(ramp)-1))
            row.append(ramp[i])
        print(f"{hs[h0+h]*f0:5.0f}|" + "".join(row))
    print()

show(0.55, 1.60, 15, 42, 105, "=== A: 0.55-1.60 s ===")
show(1.60, 2.65, 15, 42, 105, "=== B: 1.60-2.65 s ===")
show(2.65, 3.70, 15, 42, 105, "=== C: 2.65-3.70 s ===")
show(3.70, 4.80, 15, 42, 105, "=== D: 3.70-4.80 s ===")
