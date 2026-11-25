from PIL import Image
import numpy as np, base64

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)
CRIB = b'flag{'

A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
mask = np.all(A == [255, 254, 232], axis=2)
dotrows = [r for r in range(A.shape[0]) if mask[r].any()]
G = mask[np.ix_(dotrows, list(range(0, 720)))].astype(np.uint8)

def runs(row):
    out, c = [], 0
    for v in row:
        if v:
            c += 1
        else:
            if c:
                out.append(c)
            c = 0
    if c:
        out.append(c)
    return out

def gaps(row):
    out, c = [], 0
    for v in row:
        if not v:
            c += 1
        else:
            if c:
                out.append(c)
            c = 0
    return out

hits = 0
probes = 0

def try_vals(vals, tag):
    global hits, probes
    v = np.asarray(vals, dtype=np.int64)
    if len(v) < n:
        return
    for off in range(0, min(len(v) - n, 200) + 1):
        s = v[off:off + n]
        for name, pad in [
            ('0x20+v%16', 0x20 + (s % 16)),
            ('0x20+v%32', 0x20 + (s % 32)),
            ('0x20+(v-1)%16', 0x20 + ((s - 1) % 16)),
            ('0x20+cum%16', 0x20 + (np.cumsum(s) % 16)),
            ('v', s),
            ('0x20+v*5%16', 0x20 + (s * 5) % 16),
        ]:
            probes += 1
            p = bytes(int(a) ^ int(b) & 0xFF for a, b in zip(ct, pad))
            if CRIB in p:
                hits += 1
                print('HIT', tag, name, off)
                print(p)

for r in range(15):
    try_vals(runs(G[r]), 'runs_row%d' % r)
    try_vals(gaps(G[r]), 'gaps_row%d' % r)
for c in range(0, 720, 1):
    col = G[:, c]
    try_vals(runs(col), 'runs_col%d' % c)
try_vals(G.sum(axis=0), 'colsum')
try_vals(G.sum(axis=1), 'rowsum')
print('probes', probes, 'hits', hits)
