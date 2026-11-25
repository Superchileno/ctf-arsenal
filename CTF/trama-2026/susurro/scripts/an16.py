import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import median_filter, gaussian_filter, maximum_filter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/"

nper = 8192
f, t, S = signal.spectrogram(x, fs=rate, nperseg=nper, noverlap=nper-256, window="hann", scaling="spectrum")
Sdb = 10*np.log10(S+1e-20)
print("Sdb", Sdb.shape, "df", f[1]-f[0])

# mediana a lo largo de frecuencia (quita picos armonicos estrechos ~2 bins)
base = median_filter(Sdb, size=(9, 1))
resid = Sdb - base
print("resid rango", resid.min().round(1), resid.max().round(1))

m = (f >= 1800) & (f <= 5200)
sub = resid[m]
sub = gaussian_filter(sub, sigma=(0.8, 1.2))

a = np.searchsorted(t, 0.45); b = np.searchsorted(t, 4.90)
Z = sub[:, a:b]
print("Z", Z.shape)
lo, hi = np.percentile(Z, 40), np.percentile(Z, 99.8)
plt.figure(figsize=(24, 7), dpi=100)
plt.pcolormesh(t[a:b], f[m], Z, shading="auto", cmap="inferno", vmin=lo, vmax=hi)
plt.colorbar(); plt.title("residuo (texto?) 1.8-5.2 kHz")
plt.tight_layout(); plt.savefig(out+"resid.png"); plt.close()
print(round(lo,1), round(hi,1))
