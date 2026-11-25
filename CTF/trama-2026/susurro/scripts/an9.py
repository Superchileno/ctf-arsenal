import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.image as mpimg

png = mpimg.imread("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/spec_full.png")
g = png[..., :3].mean(axis=2)
H, W = g.shape

# x: 0..7.256s -> columnas del PNG con margenes. Estimamos area de trazado
# columna con contenido: buscar donde hay señal
colmean = g.mean(axis=0)
nz = np.where(colmean > 5)[0]
print("cols con contenido:", nz.min(), nz.max(), "W=", W)
rowmean = g.mean(axis=1)
nzr = np.where(rowmean > 5)[0]
print("filas con contenido:", nzr.min(), nzr.max(), "H=", H)

# perfil: intensidad en zona texto (x 150..1400) menos zona silencio (x 1500..1900)
a = g[:, 150:1400].mean(axis=1)
b = g[:, 1500:1900].mean(axis=1)
d = a - b
order = np.argsort(d)[::-1][:40]
print("filas mas brillantes (texto) :", sorted(order.tolist()))
print("valores:", [round(d[i],1) for i in sorted(order.tolist())])
