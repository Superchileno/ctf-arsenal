import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage import zoom
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = x.astype(np.float64)
out = "/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/"

bursts = [(0.569,0.818),(0.851,1.063),(1.087,1.362),(1.458,1.534),
          (1.939,2.160),(2.184,2.459),(2.474,2.714),(2.746,2.986),
          (3.028,3.240),(3.300,3.530),(3.563,3.793),(3.844,4.065),
          (4.116,4.337),(4.388,4.609)]

G = []
for (t0,t1) in bursts:
    a, b = int(t0*rate), int(t1*rate)
    seg = x[a:b]
    nperseg = min(512, len(seg))
    f, t, S = signal.spectrogram(seg, fs=rate, nperseg=nperseg, noverlap=nperseg-32, window="hann", scaling="spectrum")
    m = (f >= 2000) & (f <= 4400)
    Z = 10*np.log10(S[m]+1e-20)
    # normalizar por columna
    Z = Z - np.median(Z, axis=0, keepdims=True)
    Z = np.clip(Z, 0, None)
    Z = Z/(Z.max()+1e-9)
    # redimensionar a 60x120
    z = zoom(Z, (120/Z.shape[0], 60/Z.shape[1]), order=1)
    z = z[::-1]           # frecuencia descendente hacia abajo? invertir para que agudo arriba
    G.append(z)

sep = np.ones((120, 3))*0.5
strip = []
for i,g in enumerate(G):
    strip.append(g)
    if i in (3,):
        strip.append(np.ones((120,8))*0.35)   # separacion tras KEY:
    else:
        strip.append(sep)
S = np.concatenate(strip, axis=1)
print("strip", S.shape)
plt.figure(figsize=(26, 6), dpi=90)
plt.imshow(S, cmap="inferno", aspect="auto", interpolation="nearest", vmin=0.15, vmax=0.85)
plt.title("14 bursts (cada bloque = 1 caracter). 1-3: K E Y   4: dos puntos   5-14: palabra")
plt.xticks([]); plt.yticks([])
plt.tight_layout(); plt.savefig(out+"strip.png"); plt.close()
print("ok")
