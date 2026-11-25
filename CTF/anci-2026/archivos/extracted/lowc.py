from PIL import Image
import numpy as np, collections

A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
H, W, _ = A.shape
bg = np.array([245, 238, 220])

d = np.abs(A - bg).sum(axis=2)
print('shape', A.shape)
print('dist of diff:', collections.Counter(np.clip(d, 0, 40).tolist()).most_common(20))

# map of "slightly off background" pixels
for lo, hi in [(1, 5), (6, 15), (16, 40)]:
    m = (d >= lo) & (d <= hi)
    ys, xs = np.nonzero(m)
    print('range', lo, hi, 'count', m.sum(), 'bbox', (ys.min(), ys.max(), xs.min(), xs.max()) if m.sum() else None)

# visualize the low-contrast layer
m = (d >= 1) & (d <= 12)
out = np.where(m, 0, 255).astype(np.uint8)
Image.fromarray(out).save('lowcontrast.png')
print('saved')
