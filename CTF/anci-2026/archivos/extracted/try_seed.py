import base64, random

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())

seeds = [2026, 314, 3142026, 20260314, 14032026, 140326, 0, 7, 42, 1337, 4412,
         2291, '2026-03-14', '2026-03-14'.replace('-', ''), 'inkroute',
         'KEY REMNANT', 'key remnant', 'arc-07', 'soft-otp', 'bypass-me',
         'mara', 'Inkroute', 'inkroute field office', 'signal', 'remnant']

def score(p):
    ok = sum(32 <= c < 127 for c in p)
    try:
        s = p.decode('ascii')
    except Exception:
        return ok / len(p), p
    return ok / len(p), p

for s in seeds:
    r = random.Random(s)
    pad = bytes(r.randrange(256) for _ in range(len(ct)))
    p = bytes(a ^ b for a, b in zip(ct, pad))
    pr, p = score(p)
    if pr > 0.9:
        print(repr(s), round(pr, 3), p[:80])

print('done', len(ct))
