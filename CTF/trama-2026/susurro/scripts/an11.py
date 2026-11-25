import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

png = mpimg.imread("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/spec_full.png")
g = png[..., :3].mean(axis=2)

y0, y1 = 830, 990       # banda del texto
# tiempos: el eje x va de col 14 (t=0) a 2126 (t=7.256)
def x_of(t): return int(14 + t/7.256*(2126-14))

for name, (t0, t1) in {"A": (0.45, 1.75), "B": (1.75, 3.1), "C": (3.1, 4.85)}.items():
    x0, x1 = x_of(t0), x_of(t1)
    sub = g[y0:y1, x0:x1].copy()
    sub = sub - np.median(sub, axis=1, keepdims=True)
    sub = np.clip(sub, 0, None)
    sub = sub / (sub.max() + 1e-9)
    plt.figure(figsize=(16, 4.2), dpi=120)
    plt.imshow(sub, aspect="auto", cmap="magma", interpolation="nearest", vmin=0, vmax=0.6)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(f"/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/txt_{name}.png")
    plt.close()
    print(name, sub.shape)
