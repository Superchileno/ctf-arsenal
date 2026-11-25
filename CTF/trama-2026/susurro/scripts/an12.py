import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/"

f, t, S = signal.spectrogram(x, fs=rate, nperseg=4096, noverlap=3840, window="hann", scaling="spectrum")
Sdb = 10*np.log10(S+1e-20)
print("S", Sdb.shape)

# suavizar en frecuencia para fusionar el peine de armonicos (sigma ~ 3 bins = 32 Hz)
Ss = gaussian_filter(Sdb, sigma=(3.0, 0.0))
# suavizar en tiempo ligeramente
Ss = gaussian_filter(Ss, sigma=(0.0, 1.0))

m = (f >= 2200) & (f <= 5000)
sub = Ss[m]
print("banda", f[m][0], f[m][-1], "filas", sub.shape)

chunks = [(0.5, 1.6), (1.6, 2.7), (2.7, 3.8), (3.8, 4.85)]
for i, (t0, t1) in enumerate(chunks):
    a = np.searchsorted(t, t0); b = np.searchsorted(t, t1)
    Z = sub[:, a:b]
    lo, hi = np.percentile(Z, 2), np.percentile(Z, 99.5)
    plt.figure(figsize=(16, 5), dpi=110)
    plt.pcolormesh(t[a:b], f[m], Z, shading="auto", cmap="magma", vmin=lo+ (hi-lo)*0.55, vmax=hi)
    plt.title(f"{t0}-{t1}s")
    plt.ylabel("Hz")
    plt.tight_layout()
    plt.savefig(out+f"ink_{i}.png")
    plt.close()
    print("guardado", i, Z.shape, round(lo,1), round(hi,1))
