from PIL import Image
import numpy as np
A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
mask = np.all(A == [255,254,232], axis=2)
rows = list(range(240, 283, 3))
G = mask[np.ix_(rows, list(range(40, 680)))].astype(int)
for r in G:
    print(''.join('#' if v else '.' for v in r))
