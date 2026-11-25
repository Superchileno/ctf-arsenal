import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.image as mpimg

png = mpimg.imread("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/spec_full.png")
print("shape", png.shape, "dtype", png.dtype)
print("min max mean", png[..., :3].min(), png[..., :3].max(), png[..., :3].mean())
print("canal alpha rango", png[..., 3].min(), png[..., 3].max()) if png.shape[2] == 4 else print("sin alpha")
g = png[..., :3].mean(axis=2)
print("g min max mean", g.min(), g.max(), g.mean())
print("histograma:", np.histogram(g, bins=10)[0].tolist())
colmean = g.mean(axis=0)
print("colmean rango", colmean.min(), colmean.max())
print("colmean muestra", np.round(colmean[::200], 2).tolist())
