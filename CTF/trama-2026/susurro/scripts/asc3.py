import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.image as mpimg
from scipy.ndimage import median_filter

png = mpimg.imread("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/spec_full.png")
g = png[..., :3].mean(axis=2)
H, W = g.shape

# localizar area de trazado: columnas/lineas de ejes
# asumimos eje y lineal entre primera y ultima fila con contenido
colmax = g.max(axis=0)
print("H,W", H, W)

def render(y0, y1, x0, x1, nrows, ncols, gamma=1.0, ramp=" .:-=+*#%@"):
    sub = g[y0:y1, x0:x1]
    ri = np.linspace(0, sub.shape[0]-1, nrows).astype(int)
    ci = np.linspace(0, sub.shape[1]-1, ncols).astype(int)
    Z = sub[np.ix_(ri, ci)].copy()
    # quitar estructura horizontal (peine) restando mediana por fila
    Z = Z - np.median(Z, axis=1, keepdims=True)
    Z = np.clip(Z, 0, None)
    if Z.max() > 0:
        Z = Z / Z.max()
    Z = Z ** gamma
    idx = (Z*(len(ramp)-1)).astype(int)
    return "\n".join("".join(ramp[i] for i in row) for row in idx)

# frec: y=1040 -> 0 Hz, y=30 -> 22050 (aprox, ajustar si hace falta)
def y_of(f): return int(1040 - f/22050*(1040-30))
print("y(4000)=", y_of(4000), "y(2400)=", y_of(2400))
y0, y1 = y_of(4300), y_of(2400)
print("banda filas", y0, y1)

for name, (t0, t1) in {"A_0.5-2.6s": (0.5, 2.6), "B_2.6-4.8s": (2.6, 4.8)}.items():
    x0 = int(t0/7.256*2144); x1 = int(t1/7.256*2144)
    print(f"\n=== {name}  (x {x0}-{x1}) ===")
    print(render(y0, y1, x0, x1, 46, 120, gamma=0.6))
