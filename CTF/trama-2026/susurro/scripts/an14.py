import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

png = mpimg.imread("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/spec_full.png")
g = png[..., :3].mean(axis=2)
out = "/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/"

# 1) recorte 1:1 de la banda baja completa (y 700-1060) -> mismo aspecto que el original
sub = g[700:1060, 0:2144]
plt.figure(figsize=(21.44, 3.6), dpi=100)
plt.imshow(sub, aspect="auto", cmap="inferno", interpolation="nearest")
plt.axis("off"); plt.tight_layout(pad=0)
plt.savefig(out+"band_1to1.png")
plt.close()

# 2) solo texto: y 820-1000, x 100-1500, escala 1:1
sub2 = g[820:1000, 100:1500]
plt.figure(figsize=(14, 1.8), dpi=100)
plt.imshow(sub2, aspect="auto", cmap="inferno", interpolation="nearest")
plt.axis("off"); plt.tight_layout(pad=0)
plt.savefig(out+"text_1to1.png")
plt.close()
print(sub.shape, sub2.shape)
