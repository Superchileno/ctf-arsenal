import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

src = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/spec_full.png"
img = mpimg.imread(src)
print("shape", img.shape)

# recortes: (y0,y1,x0,x1)
crops = {
    "c_left":  (740, 960, 140, 700),
    "c_right": (740, 960, 700, 1320),
}
for name, (y0, y1, x0, x1) in crops.items():
    sub = img[y0:y1, x0:x1]
    plt.figure(figsize=(18, 6), dpi=130)
    plt.imshow(sub, aspect="auto", interpolation="nearest")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(f"/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/out/{name}.png")
    plt.close()
    print(name, sub.shape)
