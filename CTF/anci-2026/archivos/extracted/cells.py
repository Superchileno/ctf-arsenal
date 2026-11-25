from PIL import Image
import numpy as np, base64

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)
CRIB = b'flag{'

A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
mask = np.all(A == [255, 254, 232], axis=2)
dotrows = [r for r in range(A.shape[0]) if mask[r].any()]
G = mask[np.ix_(dotrows, list(range(0, 720)))].astype(np.uint8)   # 15 x 720
print('grid', G.shape)

results = []
hits = 0

for col0, col1 in ((0, 720), (40, 680)):
    GG = mask[np.ix_(dotrows, list(range(col0, col1)))].astype(np.uint8)
    for roff in range(3):
        rows = list(range(roff, 15, 3))
        for coff in range(3):
            cols = list(range(coff, GG.shape[1], 3))
            S = GG[np.ix_(rows, cols)]           # 5 x nc
            for msb_first in (True, False):
                R = S if msb_first else S[::-1]
                for inv in (0, 1):
                    H = 1 - R if inv else R
                    vals = H.T.dot(1 << np.arange(len(rows) - 1, -1, -1)).astype(np.int64)
                    for base_off in (0x20, 0x30, 0, 0x40):
                        for start in range(0, max(1, len(vals) - n) + 1):
                            v = vals[start:start + n]
                            if len(v) < n:
                                continue
                            pad = (v + base_off) & 0xFF
                            p = bytes(int(a) ^ int(b) for a, b in zip(ct, pad))
                            if CRIB in p:
                                hits += 1
                                print('HIT c%d-%d roff%d coff%d msb%s inv%d base%s start%d'
                                      % (col0, col1, roff, coff, msb_first, inv, hex(base_off), start))
                                print(p)
                            pr = sum(32 <= c < 127 or c == 10 for c in p) / n
                            if pr > 0.93:
                                results.append((pr, col0, col1, roff, coff, msb_first, inv, base_off, start, p))

results.sort(reverse=True, key=lambda x: x[0])
for r in results[:6]:
    print(round(r[0], 3), r[1:9])
    print(r[9][:120])
print('hits', hits, 'cands', len(results))
