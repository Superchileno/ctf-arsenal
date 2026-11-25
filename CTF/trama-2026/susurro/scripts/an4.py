import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/"

nper, nov = 1024, 960   # 64 Hz hop => 15.6 ms... mejor 7.8ms
f, t, S = signal.spectrogram(x, fs=rate, nperseg=nper, noverlap=nov, window="hann", scaling="spectrum")
Sdb = 10*np.log10(S+1e-20)

for lo, hi, name in [(2400, 4600, "band_text"), (2500, 4200, "band_text2")]:
    m = (f >= lo) & (f <= hi)
    sub = Sdb[m]
    vmax = np.percentile(sub, 99.9); vmin = vmax - 25
    plt.figure(figsize=(30, 8), dpi=100)
    plt.pcolormesh(t, f[m], sub, shading="auto", cmap="magma", vmin=vmin, vmax=vmax)
    plt.xlabel("t (s)"); plt.ylabel("Hz")
    plt.tight_layout(); plt.savefig(out+name+".png"); plt.close()
    print(name, "guardado", vmin, vmax)
