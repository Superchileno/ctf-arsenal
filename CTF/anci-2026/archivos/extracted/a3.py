from PIL import Image
import numpy as np, collections
A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
mask = np.all(A == [255,254,232], axis=2)
ys, xs = np.nonzero(mask)
print('bbox rows', ys.min(), ys.max(), 'cols', xs.min(), xs.max(), 'n', len(ys))
rc = collections.Counter(ys.tolist())
print('rows with dots:', len(rc))
for r in sorted(rc): print(r, rc[r])
cc = collections.Counter(xs.tolist())
print('cols with dots:', len(cc), 'min/max count', min(cc.values()), max(cc.values()))
print(sorted(cc.items())[:20])
# gaps in columns
xs_sorted = sorted(cc)
gaps = collections.Counter(b-a for a,b in zip(xs_sorted, xs_sorted[1:]))
print('col gaps', gaps.most_common(10))
rs = sorted(rc)
print('row gaps', collections.Counter(b-a for a,b in zip(rs, rs[1:])).most_common(10))
