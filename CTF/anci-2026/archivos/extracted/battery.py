from PIL import Image
import numpy as np, base64, itertools

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)
CRIB = b'flag{'

A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
mask = np.all(A == [255, 254, 232], axis=2)

rows = [r for r in range(A.shape[0]) if mask[r].any()]
G = mask[np.ix_(rows, list(range(0, 720)))].astype(np.uint8)   # 15 x 720
G_in = mask[np.ix_(rows, list(range(40, 680)))].astype(np.uint8)  # 15 x 640

def runs(row):
    out = []
    c = 0
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
    out = []
    c = 0
    for v in row:
        if not v:
            c += 1
        else:
            if c:
                out.append(c)
            c = 0
    return out

found = []
probes = 0

def try_pad(vals, tag):
    global probes
    vals = np.asarray(vals, dtype=np.int64)
    if len(vals) < n:
        return
    for off in range(0, min(len(vals) - n, 200) + 1):
        v = vals[off:off + n]
        for name, pad in [
            ('v', v),
            ('v&0x3f', v & 0x3f),
            ('0x20|v&0x1f', 0x20 | (v & 0x1f)),
            ('0x20+v%32', 0x20 + (v % 32)),
            ('0x30+v%10', 0x30 + (v % 10)),
            ('0x20+v%64', 0x20 + (v % 64)),
            ('0x20+v%95', 0x20 + (v % 95)),
            ('0x20+(v*7)%32', 0x20 + (v * 7) % 32),
            ('cum%256', np.cumsum(v) % 256),
            ('cum%32', 0x20 + (np.cumsum(v) % 32)),
        ]:
            probes += 1
            p = bytes(int(a) ^ int(b) for a, b in zip(ct, pad))
            if CRIB in p:
                found.append((tag, name, off, p))
                print('HIT', tag, name, off)
                print(p)

for r in range(G.shape[0]):
    try_pad(runs(G[r]), 'runs_row%d' % r)
    try_pad(gaps(G[r]), 'gaps_row%d' % r)
for c in range(0, 720):
    col = G[:, c]
    try_pad(runs(col), 'runs_col%d' % c)
try_pad(G.sum(axis=0), 'colsum_full')
try_pad(G_in.sum(axis=0), 'colsum_inner')
try_pad(G.sum(axis=1), 'rowsum')
ff = [list(G_in[:, c]).index(1) if G_in[:, c].any() else 15 for c in range(G_in.shape[1])]
ll = [14 - list(G_in[:, c][::-1]).index(1) if G_in[:, c].any() else 15 for c in range(G_in.shape[1])]
try_pad(ff, 'firstdot')
try_pad(ll, 'lastdot')
try_pad([a - b for a, b in zip(ll, ff)], 'span')

print('probes', probes, 'hits', len(found))
