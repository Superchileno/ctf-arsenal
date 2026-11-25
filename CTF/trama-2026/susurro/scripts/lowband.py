import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/"

nper=2048
f,t,S = signal.spectrogram(x, fs=rate, nperseg=nper, noverlap=nper-128, window="hann", scaling="spectrum")
Sd = gaussian_filter(10*np.log10(S+1e-20), sigma=(2.0,1.0))
m = (f>=150)&(f<=2400)
a,b = np.searchsorted(t,0.5), np.searchsorted(t,4.9)
Z = Sd[m][:,a:b]
lo,hi = np.percentile(Z,45), np.percentile(Z,99.8)
plt.figure(figsize=(26,8), dpi=100)
plt.pcolormesh(t[a:b], f[m], Z, shading="auto", cmap="magma", vmin=lo+(hi-lo)*0.45, vmax=hi)
plt.ylabel("Hz"); plt.title("150-2400 Hz (posible segundo mensaje)")
plt.tight_layout(); plt.savefig(out+"lowband.png"); plt.close()
print(Z.shape, round(lo,1), round(hi,1))
