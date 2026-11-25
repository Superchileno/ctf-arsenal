import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.image as mpimg

png = mpimg.imread("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/spec_full.png")
g = png[..., :3].mean(axis=2)
H, W = g.shape
colmean = g.mean(axis=0)
nz = np.where(colmean > 0.02)[0]
print("area trazado: cols", nz.min(), nz.max(), " de", W)
rowmean = g.mean(axis=1)
nzr = np.where(rowmean > 0.02)[0]
print("area trazado: filas", nzr.min(), nzr.max(), " de", H)

# mapear filas -> frecuencia usando nzr
y0p, y1p = nzr.min(), nzr.max()
def freq(y): return 22050*(y1p - y)/(y1p - y0p)

a = g[:, 200:1350].mean(axis=1)   # zona del texto
b = g[:, 1900:2050].mean(axis=1)  # zona silencio (si existe)
d = a - b
top = np.argsort(d)[::-1][:60]
print("filas texto (y, freq):", [(int(i), round(freq(i))) for i in sorted(top.tolist())])
