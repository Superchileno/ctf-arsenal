from PIL import Image
import numpy as np
A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
mask = np.all(A == [255,254,232], axis=2)
rows = list(range(240, 283, 3))
G = mask[np.ix_(rows, list(range(40, 680)))].astype(int)
h = G.sum(axis=0)
s = ''.join('0123456789ABCDEF'[v] for v in h)
for i in range(0, 640, 128):
    print(i, s[i:i+128])
# per-column first nonzero row and last
print()
for i in range(0, 640, 128):
    print('first', i, ''.join('0123456789ABCDE'[int(np.nonzero(G[:,c])[0][0])] for c in range(i, i+128)))
print()
for i in range(0, 640, 128):
    print('last ', i, ''.join('0123456789ABCDE'[int(np.nonzero(G[:,c])[0][-1])] for c in range(i, i+128)))
