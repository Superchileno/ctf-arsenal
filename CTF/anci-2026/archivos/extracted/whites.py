from PIL import Image
import numpy as np, collections

A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
H, W, _ = A.shape

# all colors that are "whitish-blue"
sel = (A[:, :, 0] == 255) & (A[:, :, 1] == 255) & (A[:, :, 2] < 255)
ys, xs = np.nonzero(sel)
print('whitish count', sel.sum())
print('bbox y', ys.min(), ys.max(), 'x', xs.min(), xs.max())

vals = collections.Counter(A[ys, xs, 2].tolist())
print('B values:', sorted(vals.items()))

# spatial distribution per B value
for b in sorted(vals)[:20]:
    m = sel & (A[:, :, 2] == b)
    yy, xx = np.nonzero(m)
    print('B=%d n=%d yrange=%s xrange=%s' % (b, m.sum(), (yy.min(), yy.max()), (xx.min(), xx.max())))

# render: whites as black on white
out = np.where(sel, 0, 255).astype(np.uint8)
Image.fromarray(out).save('whites.png')
print('saved whites.png')
