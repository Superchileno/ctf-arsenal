import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.image as mpimg

png = mpimg.imread("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/spec_full.png")
g = png[..., :3].mean(axis=2)

y0, y1 = 845, 945          # banda del texto
def x_of(t): return int(14 + t/7.256*2112)

ramp = " .:-=+*#%@"

def render(t0, t1, sx=2, sy=2):
    x0, x1 = x_of(t0), x_of(t1)
    sub = g[y0:y1, x0:x1].copy()
    # quitar la componente de peine: mediana por fila
    sub = sub - np.median(sub, axis=1, keepdims=True)
    sub = np.clip(sub, 0, None)
    # normalizar por columna (quita modulacion temporal)
    cm = sub.max(axis=0, keepdims=True) + 1e-6
    sub = sub / cm
    # downsample por max-pooling (preserva trazos)
    H, W = sub.shape
    nh, nw = H//sy, W//sx
    sub = sub[:nh*sy, :nw*sx].reshape(nh, sy, nw, sx).max(axis=(1, 3))
    idx = np.clip((sub*(len(ramp)-1)*1.6), 0, len(ramp)-1).astype(int)
    lines = []
    for r in range(nh-1, -1, -1):
        lines.append("".join(ramp[i] for i in idx[r]))
    return "\n".join(lines)

for name, (t0, t1) in {"P1": (0.45, 1.90), "P2": (1.90, 3.40), "P3": (3.40, 4.90)}.items():
    print(f"\n===== {name}: {t0}-{t1}s =====")
    print(render(t0, t1))
