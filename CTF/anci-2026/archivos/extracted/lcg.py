import base64, itertools

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)
CRIB = b'flag{'
found = 0

def test(pad, tag):
    global found
    p = bytes(c ^ k for c, k in zip(ct, pad))
    if CRIB in p:
        found += 1
        print('HIT', tag)
        print(p)

# affine pads mod various bases
for m, off in ((256, 0), (128, 0), (95, 32), (64, 32), (32, 32), (16, 32), (10, 48)):
    for a in range(m):
        for b in range(m):
            pad = [((a * i + b) % m) + off for i in range(n)]
            if max(pad) > 255:
                continue
            test(pad, 'affine m=%d off=%d a=%d b=%d' % (m, off, a, b))
print('affine done', found)

# LCG pads
for m in (256, 128, 95, 32):
    for a in range(0, m, max(1, m // 32)):
        for c0 in range(0, m, max(1, m // 32)):
            for seed in (0, 1, 14, 42, 2026 % m, 314 % m):
                v = seed % m
                pad = []
                for i in range(n):
                    pad.append(v + (32 if m <= 95 else 0))
                    v = (a * v + c0) % m
                if max(pad) > 255:
                    continue
                test(pad, 'lcg m=%d a=%d c=%d s=%d' % (m, a, c0, seed))
print('lcg done', found)
