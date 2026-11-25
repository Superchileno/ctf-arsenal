from PIL import Image
import numpy as np
A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
mask = np.all(A == [255,254,232], axis=2)
rows = list(range(240, 283, 3))
G = mask[np.ix_(rows, list(range(40, 680)))].astype(int)  # 15 x 640
print(G.shape)
pat = {}
for c in range(G.shape[1]):
    col = ''.join(str(v) for v in G[:, c])
    pat.setdefault(col, []).append(c)
print('distinct column patterns', len(pat))
for k, v in sorted(pat.items(), key=lambda kv: -len(kv[1]))[:20]:
    print(k, len(v), v[:8])
# contiguity check
noncontig = 0
for c in range(G.shape[1]):
    col = G[:, c]
    idx = np.nonzero(col)[0]
    if len(idx) and (idx[-1]-idx[0]+1 != len(idx)):
        noncontig += 1
print('non-contiguous columns', noncontig)
# heights
h = G.sum(axis=0)
print('heights hist', np.bincount(h))
print('first idx hist', np.bincount([np.nonzero(G[:,c])[0][0] if G[:,c].any() else -1 for c in range(640)])[:16])
