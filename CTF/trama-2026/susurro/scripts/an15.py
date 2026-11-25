import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

png = mpimg.imread("/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/spec_full.png")
g = png[..., :3].mean(axis=2)
out = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/"

# region del texto en el PNG: y ~ 855..935 (2.4-4.1 kHz), x = 14 + t/7.256*2112
def x_of(t): return int(14 + t/7.256*2112)

regions = {"k1": (0.50, 0.95), "k2": (0.95, 1.40), "k3": (1.85, 2.35), "k4": (2.35, 2.85),
           "k5": (2.85, 3.35), "k6": (3.35, 3.85), "k7": (3.85, 4.35), "k8": (4.35, 4.80)}
for name, (t0, t1) in regions.items():
    sub = g[850:940, x_of(t0):x_of(t1)]
    plt.figure(figsize=(12, 5), dpi=100)
    plt.imshow(sub, aspect="auto", cmap="inferno", interpolation="nearest")
    plt.axis("off"); plt.tight_layout(pad=0)
    plt.savefig(out+f"zoom_{name}.png"); plt.close()
    print(name, sub.shape)
