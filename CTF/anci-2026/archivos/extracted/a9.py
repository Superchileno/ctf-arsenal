from PIL import Image
import numpy as np, base64, string

ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
n = len(ct)
A = np.array(Image.open('stamp_scan.png').convert('RGB')).astype(int)
mask = np.all(A == [255,254,232], axis=2)
rows = list(range(240, 283, 3))
G = mask[np.ix_(rows, list(range(40, 680)))].astype(np.uint8)
print(G.shape)

b64a = set((string.ascii_uppercase+string.ascii_lowercase+string.digits+'+/=').encode())

def report(tag, p):
    pr = sum(32 <= c < 127 or c in (10,13,9) for c in p)/len(p)
    if b'flag{' in p or b'FLAG{' in p:
        print('!!!FLAG', tag, p)
    if set(p) <= b64a:
        print('B64', tag, p)
    if pr > 0.97:
        print('PRINT', round(pr,3), tag, p[:80])

variants = []
for inv in (0,1):
    H = 1-G if inv else G
    for order in ('row','col'):
        B = H.reshape(-1) if order=='row' else H.T.reshape(-1)
        for rev in (0,1):
            variants.append((f'inv{inv}_{order}_rev{rev}', B[::-1] if rev else B))

for tag,B in variants:
    L=len(B)
    for w in (6,7,8):
        for off in range(w):
            cnt=(L-off)//w
            if cnt < n: continue
            seg=B[off:off+cnt*w].reshape(cnt,w).astype(np.int64)
            for msb in (1,0):
                wts = (1<<np.arange(w-1,-1,-1)) if msb else (1<<np.arange(w))
                vals = seg.dot(wts)
                for start in range(0, cnt-n+1, 1):
                    key = vals[start:start+n] & 0xFF
                    p = bytes(int(a)^int(b) for a,b in zip(ct,key))
                    report(f'{tag} w{w} off{off} msb{msb} start{start}', p)
print('done')
