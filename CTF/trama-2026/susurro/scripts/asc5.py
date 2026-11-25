import numpy as np
from scipy.io import wavfile

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
f0 = 110.25
win = 2048
hop = 110   # 2.5 ms
frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop]
frames = frames * np.hanning(win)
n = np.fft.rfftfreq(win, 1/rate)
F = np.abs(np.fft.rfft(frames, axis=1))
if F.max() < 1e-6: print("escala rara")
print("F max", F.max())

hs = np.arange(1, int(5000/f0)+1)
amps = []
for h in hs:
    k = np.argmin(np.abs(n - h*f0))
    amps.append(F[:, k-1:k+2].max(axis=1))
A = 20*np.log10(np.array(amps).T + 1e-9)
print("A shape", A.shape, "min/max", A.min().round(1), A.max().round(1))

# percentiles por armonico -> niveles
lo = np.percentile(A, 5, axis=0)
hi = np.percentile(A, 95, axis=0)
print("rango dinamico por armonico (dB):", np.round(hi-lo,1))

def show(t0, t1, h0, h1, ncols=120):
    a = int(t0*rate/hop); b = int(t1*rate/hop)
    sub = A[a:b, h0:h1]
    lo_ = lo[h0:h1]; hi_ = hi[h0:h1]
    Z = (sub - lo_)/(hi_-lo_+1e-9)
    Z = np.clip(Z, 0, 1)
    ci = np.linspace(0, Z.shape[0], ncols+1).astype(int)
    ramp = " .:-=+*#%@"
    out = []
    for h in range(Z.shape[1]-1, -1, -1):
        row = []
        for c in range(ncols):
            s, e = ci[c], max(ci[c]+1, ci[c+1])
            v = np.mean(Z[s:e, h])
            row.append(ramp[min(len(ramp)-1, int(v*(len(ramp)-1.001)))])
        out.append(f"{hs[h0+h]*f0:5.0f}|" + "".join(row))
    print("\n".join(out))

print("\n=== 0.55-1.55 s, armonicos 2.2-4.4 kHz ===")
show(0.55, 1.55, 19, 40)
