import numpy as np
from scipy.io import wavfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
print("rate", rate, "n", len(x), "dur", len(x)/rate)
print("mean", x.mean(), "std", x.std())

# Espectrograma global alta resolucion
f, t, S = signal.spectrogram(x, fs=rate, nperseg=4096, noverlap=3072, window="hann", scaling="spectrum")
Sdb = 10*np.log10(S + 1e-20)
print("S shape", S.shape, "max", Sdb.max(), "min", Sdb.min())

plt.figure(figsize=(26, 9), dpi=110)
plt.pcolormesh(t, f, Sdb, shading="auto", cmap="inferno", vmin=Sdb.max()-70, vmax=Sdb.max())
plt.ylim(0, 6000)
plt.xlabel("t (s)"); plt.ylabel("Hz"); plt.title("0-6 kHz")
plt.tight_layout(); plt.savefig("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/np_low.png")
plt.close()

# perfil espectral medio para ver armonicos
prof = Sdb.mean(axis=1)
peaks, props = signal.find_peaks(prof, distance=5)
top = peaks[np.argsort(prof[peaks])[::-1][:40]]
print("picos fuertes (Hz):", sorted(np.round(f[top]).astype(int).tolist()))

# Espectro de una ventana al centro
seg = x[rate*2:rate*2+65536]*np.hanning(65536)
X = np.abs(np.fft.rfft(seg))
fr = np.fft.rfftfreq(65536, 1/rate)
idx = np.argsort(X)[::-1][:30]
print("fft picos:", sorted(np.round(fr[idx]).astype(int).tolist()))
