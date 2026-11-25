import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.image as mpimg

img = mpimg.imread("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out/spec_full.png")
print("shape", img.shape)
g = img[..., :3].mean(axis=2)
print("rows", g.shape[0], "cols", g.shape[1])

# perfil de varianza por fila para localizar bandas con "texto"
rv = g.std(axis=1)
top = np.argsort(rv)[::-1][:25]
print("filas con mayor varianza:", sorted(top.tolist()))

# ASCII del PNG completo, 200x80
def render(y0, y1, x0, x1, nrows, ncols, gamma=1.0):
    sub = g[y0:y1, x0:x1]
    ri = np.linspace(0, sub.shape[0]-1, nrows).astype(int)
    ci = np.linspace(0, sub.shape[1]-1, ncols).astype(int)
    Z = sub[np.ix_(ri, ci)]
    Z = (Z - Z.min())/(Z.max()-Z.min()+1e-9)
    Z = Z**gamma
    chars = " .:-=+*#%@"
    idx = (Z*(len(chars)-1)).astype(int)
    return "\n".join("".join(chars[i] for i in row) for row in idx)

print("\n=== PNG completo (80x200) ===")
print(render(0, g.shape[0], 0, g.shape[1], 80, 200))
