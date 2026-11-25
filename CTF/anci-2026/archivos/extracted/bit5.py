from PIL import Image
import numpy as np, base64, itertools

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)
CRIB = b'flag{'
A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
mask = np.all(A == [255, 254, 232], axis=2)
rows = [r for r in range(A.shape[0]) if mask[r].any()]

best = []
hits = 0
probes = 0

def bits_variants():
    for c0, c1 in ((0, 720), (40, 680)):
        G = mask[np.ix_(rows, list(range(c0, c1)))].astype(np.uint8)
        for inv in (0, 1):
            H = 1 - G if inv else G
            for order in ('row', 'col'):
                base = H.reshape(-1) if order == 'row' else H.T.reshape(-1)
                for rev in (0, 1):
                    B = base[::-1] if rev else base
                    yield '%s_inv%d_%s_rev%d' % (c1 - c0, inv, order, rev), B

for tag, B in bits_variants():
    L = len(B)
    for gw in (5, 6, 7):
        for start in range(0, 40):
            cnt = (L - start) // gw
            if cnt < n:
                continue
            vals = np.zeros(cnt, dtype=np.int64)
            seg = B[start:start + cnt * gw].reshape(cnt, gw)
            w = (1 << np.arange(gw - 1, -1, -1))
            vals = seg.dot(w)
            for base_off in (0x20, 0x30, 0, 0x40):
                pad = (vals[:n] + base_off)
                pad = np.where(pad < 256, pad, pad % 256).astype(np.uint8)
                probes += 1
                p = bytes(int(a) ^ int(b) for a, b in zip(ct, pad))
                pr = sum(32 <= c < 127 or c == 10 for c in p) / n
                if CRIB in p:
                    hits += 1
                    print('HIT', tag, 'gw', gw, 'start', start, 'base', hex(base_off))
                    print(p)
                elif pr > 0.9:
                    best.append((pr, tag, gw, start, base_off, p))

best.sort(reverse=True, key=lambda x: x[0])
for b in best[:5]:
    print(round(b[0], 3), b[1:5])
    print(b[5][:100])
print('probes', probes, 'hits', hits, 'printable-candidates', len(best))
