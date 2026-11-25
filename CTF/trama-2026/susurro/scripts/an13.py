import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/"

f, t, S = signal.spectrogram(x, fs=rate, nperseg=4096, noverlap=3900, window="hann", scaling="spectrum")
Sdb = 10*np.log10(S+1e-20)
Ss = gaussian_filter(Sdb, sigma=(2.5, 0.8))

m = (f >= 2300) & (f <= 4300)
sub = Ss[m]
chunks = [(0.5, 1.65), (1.65, 2.8), (2.8, 3.85), (3.85, 4.85)]
for i, (t0, t1) in enumerate(chunks):
    a = np.searchsorted(t, t0); b = np.searchsorted(t, t1)
    Z = sub[:, a:b]
    lo, hi = np.percentile(Z, 5), np.percentile(Z, 99.8)
    plt.figure(figsize=(22, 7), dpi=100)
    plt.pcolormesh(t[a:b], f[m], Z, shading="auto", cmap="gray", vmin=lo + (hi-lo)*0.5, vmax=hi)
    plt.title(f"{t0}-{t1} s")
    plt.tight_layout()
    plt.savefig(out+f"ink2_{i}.png"); plt.close()
    print(i, Z.shape, round(lo,1), round(hi,1))
