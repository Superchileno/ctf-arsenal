import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import zoom
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/"
bursts = [(0.569,0.818),(0.851,1.063),(1.087,1.362),(1.458,1.534),
          (1.939,2.160),(2.184,2.459),(2.474,2.714),(2.746,2.986),
          (3.028,3.240),(3.300,3.530),(3.563,3.793),(3.844,4.065),
          (4.116,4.337),(4.388,4.609)]

def glyph(t0,t1,lo,hi,W=70,H=140):
    a,b = int(t0*rate), int(t1*rate)
    seg = x[a:b]
    n = min(1024, len(seg))
    f,t,S = signal.spectrogram(seg, fs=rate, nperseg=n, noverlap=n-16, window="hann", scaling="spectrum")
    m = (f>=lo)&(f<=hi)
    Z = 10*np.log10(S[m]+1e-20)
    Z = Z - np.median(Z, axis=0, keepdims=True)
    Z = np.clip(Z,0,None); Z = Z/(Z.max()+1e-9)
    z = zoom(Z, (H/Z.shape[0], W/Z.shape[1]), order=1)
    return z[::-1]

def panel(fname, lo, hi):
    G=[]; 
    for i,(t0,t1) in enumerate(bursts):
        G.append(glyph(t0,t1,lo,hi))
        G.append(np.ones((140,4))*0.4)
        if i==3: G.append(np.ones((140,10))*0.25)
    S=np.concatenate(G,axis=1)
    plt.figure(figsize=(28,7), dpi=100)
    plt.imshow(S, cmap="inferno", aspect="auto", interpolation="bicubic", vmin=0.1, vmax=0.8)
    plt.title(f"banda {lo}-{hi} Hz")
    plt.xticks([]); plt.yticks([])
    plt.tight_layout(); plt.savefig(out+fname); plt.close()
    print(fname, S.shape)

panel("strip_low.png", 2100, 3000)
