import numpy as np
from scipy.io import wavfile

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
f0 = 110.25
win = 2048
hop = 220
fr = np.lib.stride_tricks.sliding_window_view(x, win)[::hop] * np.hanning(win)
n = np.fft.rfftfreq(win, 1/rate)
F = np.abs(np.fft.rfft(fr, axis=1))
hs = np.arange(18, 42)          # 1.98 - 4.6 kHz
amps = []
for h in hs:
    k = np.argmin(np.abs(n - h*f0))
    amps.append(F[:, k-1:k+2].max(axis=1))
A = 20*np.log10(np.array(amps).T + 1e-9)      # (nfr, nhar)
mx = A.max(axis=0, keepdims=True)
Zn = A - mx                                    # dB bajo el maximo de cada armonico
print("niveles: percentiles por armonico (abs):")
for i, h in enumerate(hs):
    print(f"h{h} {h*f0:6.0f}Hz  max {A[:,i].max():6.1f}  p50 {np.percentile(A[:,i],50):6.1f}  p90 {np.percentile(A[:,i],90):6.1f}")

def show(t0, t1, thr, ncols=140):
    a = int(t0*rate/hop); b = int(t1*rate/hop)
    sub = Zn[a:b]
    ci = np.linspace(0, sub.shape[0], ncols+1).astype(int)
    print(f"\n--- {t0}-{t1}s  thr {thr} dB ---")
    for h in range(sub.shape[1]-1, -1, -1):
        row = []
        for c in range(ncols):
            s, e = ci[c], max(ci[c]+1, ci[c+1])
            v = np.median(sub[s:e, h])
            row.append("#" if v > thr else " ")
        line = "".join(row)
        print(f"{hs[h]*f0:5.0f}|{line}")
        print(f"     |{line}")

for thr in (-12,):
    show(0.50, 1.60, thr, 120)
