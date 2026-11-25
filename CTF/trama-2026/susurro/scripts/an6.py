import numpy as np
from scipy.io import wavfile
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/"

# frecuencia fundamental estimada del peine
f0 = 108.6
win = 2048
hop = 220  # 5 ms

frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop]
frames = frames * np.hanning(win)
print("frames", frames.shape)

# freqs de armonicos hasta 20 kHz
hs = np.arange(1, int(20000/f0)+1)
fr = hs*f0
# amplitud via DFT en bins cercanos
n = np.fft.rfftfreq(win, 1/rate)
F = np.abs(np.fft.rfft(frames, axis=1))  # (nfr, nfreq)
idx = np.searchsorted(n, fr)
amp = F[:, idx]  # (nfr, nharm)

A = 20*np.log10(amp+1e-9)
# normalizar cada armonico por su mediana temporal
A2 = A - np.median(A, axis=0, keepdims=True)
# transponer: filas = armonico (freq), columnas = tiempo
img = A2.T
v = np.percentile(np.abs(img), 99)
plt.figure(figsize=(30, 12), dpi=100)
plt.pcolormesh(np.arange(img.shape[1])*hop/rate, fr/1000, img, shading="auto", cmap="viridis", vmin=-v, vmax=v)
plt.ylabel("kHz (armonico)"); plt.xlabel("t (s)"); plt.colorbar()
plt.tight_layout(); plt.savefig(out+"harmonics_norm.png"); plt.close()

# solo banda 2.5-4.5 kHz
m = (fr >= 2400) & (fr <= 4600)
img2 = A2[:, m].T
v2 = np.percentile(np.abs(img2), 99.5)
plt.figure(figsize=(30, 5), dpi=100)
plt.pcolormesh(np.arange(img2.shape[1])*hop/rate, fr[m]/1000, img2, shading="auto", cmap="magma", vmin=-v2, vmax=v2)
plt.ylabel("kHz"); plt.xlabel("t (s)")
plt.tight_layout(); plt.savefig(out+"harm_band.png"); plt.close()
print("ok", img.shape, img2.shape)
