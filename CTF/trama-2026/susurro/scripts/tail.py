import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/"

# zona "silenciosa" 4.61-7.26 s: amplificar y mirar
seg = x[int(4.61*rate):]
print("cola muestras", len(seg), "max", np.abs(seg).max())
seg = seg*200.0
nper=2048
f,t,S = signal.spectrogram(seg, fs=rate, nperseg=nper, noverlap=nper-64, window="hann", scaling="spectrum")
Sd = 10*np.log10(S+1e-20)
m=(f>=0)&(f<=6000)
vmax=np.percentile(Sd[m],99.9); vmin=vmax-45
plt.figure(figsize=(24,9), dpi=100)
plt.pcolormesh(t+4.61, f[m], Sd[m], shading="auto", cmap="turbo", vmin=vmin, vmax=vmax)
plt.title("cola 4.61-7.26s amplificada x200")
plt.ylabel("Hz")
plt.tight_layout(); plt.savefig(out+"tail_amp.png"); plt.close()
print("guardado", vmin, vmax)

# tambien la intro 0-0.569
seg2 = x[:int(0.569*rate)]*200.0
f,t,S2 = signal.spectrogram(seg2, fs=rate, nperseg=nper, noverlap=nper-64, window="hann", scaling="spectrum")
Sd2 = 10*np.log10(S2+1e-20)
m2=(f>=0)&(f<=6000)
vmax2=np.percentile(Sd2[m2],99.9); vmin2=vmax2-45
plt.figure(figsize=(24,9), dpi=100)
plt.pcolormesh(t, f[m2], Sd2[m2], shading="auto", cmap="turbo", vmin=vmin2, vmax=vmax2)
plt.title("intro 0-0.569s amplificada x200")
plt.ylabel("Hz")
plt.tight_layout(); plt.savefig(out+"intro_amp.png"); plt.close()
print("guardado2", vmin2, vmax2)
