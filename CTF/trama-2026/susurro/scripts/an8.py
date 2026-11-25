import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/"

f, t, S = signal.spectrogram(x, fs=rate, nperseg=2048, noverlap=1800, window="hann", scaling="spectrum")
Sdb = 10*np.log10(S+1e-20)

for lo, hi, name in [(5000, 22050, "hi_5_22k"), (12000, 22050, "hi_12_22k"), (0, 2500, "lo_0_2k5")]:
    m = (f >= lo) & (f <= hi)
    sub = Sdb[m]
    vmax = np.percentile(sub, 99.7); vmin = vmax-30
    plt.figure(figsize=(26, 9), dpi=100)
    plt.pcolormesh(t, f[m], sub, shading="auto", cmap="turbo", vmin=vmin, vmax=vmax)
    plt.xlabel("t (s)"); plt.ylabel("Hz")
    plt.tight_layout(); plt.savefig(out+name+".png"); plt.close()
    print(name, round(vmin,1), round(vmax,1))
