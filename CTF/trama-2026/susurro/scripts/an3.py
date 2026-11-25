import numpy as np
from scipy.io import wavfile
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/"

f, t, S = signal.spectrogram(x, fs=rate, nperseg=2048, noverlap=1536, window="hann", scaling="spectrum")
Sdb = 10*np.log10(S + 1e-20)

# normalizacion por frecuencia (resalta estructura en cada banda)
med = np.median(Sdb, axis=1, keepdims=True)
Sn = Sdb - med
plt.figure(figsize=(28, 10), dpi=100)
plt.pcolormesh(t, f, Sn, shading="auto", cmap="inferno", vmin=-6, vmax=6)
plt.ylim(0, 22000)
plt.xlabel("t (s)"); plt.ylabel("Hz"); plt.title("normalizado por frecuencia, 0-22 kHz")
plt.tight_layout(); plt.savefig(out+"np_full_norm.png"); plt.close()

# banda alta 6-22 kHz sin normalizar
plt.figure(figsize=(28, 8), dpi=100)
plt.pcolormesh(t, f, Sdb, shading="auto", cmap="inferno", vmin=Sdb.max()-55, vmax=Sdb.max()-10)
plt.ylim(6000, 22050)
plt.xlabel("t (s)"); plt.ylabel("Hz"); plt.title("6-22 kHz")
plt.tight_layout(); plt.savefig(out+"np_high.png"); plt.close()

# banda 0-600 Hz
plt.figure(figsize=(28, 8), dpi=100)
plt.pcolormesh(t, f, Sn, shading="auto", cmap="inferno", vmin=-8, vmax=8)
plt.ylim(0, 600)
plt.xlabel("t (s)"); plt.ylabel("Hz"); plt.title("0-600 Hz norm")
plt.tight_layout(); plt.savefig(out+"np_sub.png"); plt.close()

# envolvente global
env = np.abs(signal.hilbert(x))
w = 441
envs = np.convolve(env, np.ones(w)/w, mode="same")
plt.figure(figsize=(20,4)); plt.plot(np.arange(len(envs))/rate, envs); plt.xlabel("s"); plt.title("envolvente"); plt.grid(True)
plt.tight_layout(); plt.savefig(out+"env.png"); plt.close()
# RMS por tramo de 5 ms para ver huecos
rms = [np.sqrt(np.mean(x[i:i+441]**2)) for i in range(0, len(x)-441, 441)]
print("RMS 5ms primeros 60:", np.round(rms[:60]).astype(int).tolist())
print("gaps (rms<50) tiempos:", [round(i*0.01,2) for i,v in enumerate(rms) if v < 50][:80])
