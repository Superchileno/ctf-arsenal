import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/"

nper = 2048
f, t, S = signal.spectrogram(x, fs=rate, nperseg=nper, noverlap=nper-256, window="hann", scaling="spectrum")
Sdb = gaussian_filter(10*np.log10(S+1e-20), sigma=(1.5, 1.0))
m = (f >= 0) & (f <= 4500)
a, b = np.searchsorted(t, 0.5), np.searchsorted(t, 4.9)
sub = Sdb[m][:, a:b]
print("sub", sub.shape)

lo, hi = np.percentile(sub, 50), np.percentile(sub, 99.7)
# rotar 90 grados: ahora eje vertical = tiempo
R = np.rot90(sub, k=1)
print("rot", R.shape)
plt.figure(figsize=(16, 10), dpi=100)
plt.imshow(R, aspect="auto", cmap="inferno", vmin=lo+(hi-lo)*0.35, vmax=hi, interpolation="nearest")
plt.axis("off"); plt.tight_layout()
plt.savefig(out+"rot90.png"); plt.close()

R2 = np.rot90(sub, k=-1)
plt.figure(figsize=(16, 10), dpi=100)
plt.imshow(R2, aspect="auto", cmap="inferno", vmin=lo+(hi-lo)*0.35, vmax=hi, interpolation="nearest")
plt.axis("off"); plt.tight_layout()
plt.savefig(out+"rot270.png"); plt.close()
print("ok")
