import base64, random, hashlib, itertools

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)

base_seeds = [2026, 314, 20260314, 14032026, 140326, 2026031, 1337, 42, 0,
              '2026-03-14', '20260314', 'inkroute', 'KEY REMNANT', 'key remnant',
              'arc-07', 'soft-otp', 'bypass-me', 'signal', 'remnant', '2026/03/14',
              '14032026', 'Inkroute', 'MAIL', 'stamp', 'postcard', 'field office']

def printable(p):
    return sum(32 <= c < 127 or c in (10, 13) for c in p) / n

def check(tag, pad):
    if pad is None or len(pad) < n:
        return None
    p = bytes(a ^ b for a, b in zip(ct, pad))
    if printable(p) > 0.98:
        return (tag, printable(p), p)
    return None

hits = []

for s in base_seeds:
    # python random variants
    for mode in ('randrange', 'getrandbits', 'randbytes', 'randint', 'choice'):
        try:
            r = random.Random(s)
            if mode == 'randrange':
                pad = bytes(r.randrange(256) for _ in range(n))
            elif mode == 'getrandbits':
                pad = bytes(r.getrandbits(8) for _ in range(n))
            elif mode == 'randbytes':
                pad = r.randbytes(n)
            elif mode == 'randint':
                pad = bytes(r.randint(0, 255) for _ in range(n))
            else:
                pad = bytes(r.choice(range(256)) for _ in range(n))
        except Exception as e:
            continue
        h = check(f'random({s!r},{mode})', pad)
        if h: hits.append(h)

    # hash based keystream
    key = str(s).encode()
    for algo in ('md5', 'sha1', 'sha256', 'sha512'):
        if algo == 'md5':
            pad = hashlib.md5(key).digest()
        elif algo == 'sha1':
            pad = hashlib.sha1(key).digest()
        elif algo == 'sha256':
            pad = hashlib.sha256(key).digest()
        else:
            pad = hashlib.sha512(key).digest()
        pad = (pad * (n // len(pad) + 1))[:n]
        h = check(f'{algo}({s!r})', pad)
        if h: hits.append(h)
        # counter mode
        stream = b''
        i = 0
        while len(stream) < n:
            hh = hashlib.new(algo)
            hh.update(key + str(i).encode())
            stream += hh.digest()
            i += 1
        h = check(f'{algo}ctr({s!r})', stream[:n])
        if h: hits.append(h)

for h in hits:
    print(h[0], round(h[1], 3))
    print(h[2])
    print('---')
print('total hits', len(hits))
