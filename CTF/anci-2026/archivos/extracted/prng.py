import base64, random, itertools, string

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)
CRIB = b'flag{'
ctb = ct

def check(p):
    return CRIB in p

def gen_pad(seed, mode):
    r = random.Random(seed)
    if mode == 0:
        return bytes(r.randrange(0x20, 0x40) for _ in range(n))
    if mode == 1:
        return bytes(0x20 + r.randrange(32) for _ in range(n))
    if mode == 2:
        return bytes(r.choice(range(0x20, 0x40)) for _ in range(n))
    if mode == 3:
        return bytes(r.randrange(256) for _ in range(n))
    if mode == 4:
        return r.randbytes(n)
    if mode == 5:
        return bytes(r.getrandbits(8) for _ in range(n))
    if mode == 6:
        return bytes(0x20 + r.getrandbits(5) for _ in range(n))
    try:
        return bytes(r.choice(string.printable.encode()) for _ in range(n))
    except Exception:
        return bytes(n)

def quick_ok(pad):
    # fast filter: first 6 plaintext chars must be "text like"
    for i in range(6):
        c = ct[i] ^ pad[i]
        if not (97 <= c <= 122 or c in (32, 10, 13, 44, 46, 39, 58, 59)):
            return False
    return True

date_ints = [2026, 314, 20260314, 14032026, 2026031, 260314, 26314, 3142026,
             2026 * 10000 + 314, 314 + 2026 * 10000, 2026 * 12 + 3 * 31 + 14]
strings = ['2026-03-14', '2026/03/14', '20260314', '14-03-2026', '14032026',
           'Inkroute', 'inkroute', 'KEY REMNANT', 'SIGNAL', 'soft-otp', 'otp',
           'Inkroute mail stamp', 'inkroute field office', 'postcard', 'stamp',
           'mara', '2026-03-14T00:00:00']

hits = 0
tested = 0
for seed in list(range(0, 60001)) + date_ints + strings:
    for mode in range(8):
        tested += 1
        pad = gen_pad(seed, mode)
        if len(pad) < n:
            continue
        if not quick_ok(pad):
            continue
        p = bytes(a ^ b for a, b in zip(ctb, pad))
        if check(p):
            hits += 1
            print('HIT seed=%r mode=%d' % (seed, mode))
            print(p)

print('tested', tested, 'hits', hits)
