import base64, re, math

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)
CRIB = b'flag{'

txt = open('corpus.txt', encoding='utf-8').read()
txt = re.sub(r'[^A-Za-z0-9 \n\'\"\.,;:\-\(\)\[\]{}/_!?%$#@&=+*]', ' ', txt)
txt = re.sub(r'[ \t]+', ' ', txt)
freq = {}
for ch in txt:
    freq[ch] = freq.get(ch, 0) + 1
tot = sum(freq.values())
logp = {ord(k): math.log(v / tot) for k, v in freq.items()}
floor = math.log(0.3 / tot)
def sc(p):
    return sum((logp.get(b, floor if 32 <= b < 127 else -15.0) for b in p)) / len(p)

keys = [b'2026-03-14', b'14-03-2026', b'20260314', b'14032026', b'Inkroute',
        b'inkroute', b'KEY REMNANT', b'SIGNAL', b'inkroute field office',
        b'Inkroute sealed postcard body', b'2026/03/14', b'soft-otp']

def mod26(c, k, sign):
    ch = chr(c)
    if not ch.isalpha():
        return c
    base = ord('a') if ch.islower() else ord('A')
    v = c - base
    kv = (k - ord('a')) % 26 if 97 <= k <= 122 else k % 26
    if sign > 0:
        v = (v + kv) % 26
    else:
        v = (v - kv) % 26
    return base + v

best = []
for key in keys:
    for sign in (1, -1):
        # mod 26 on letters
        p = bytes(mod26(c, key[i % len(key)], sign) for i, c in enumerate(ct))
        best.append((sc(p), 'mod26%s %r' % ('+' if sign > 0 else '-', key), p))
        # mod 95 printable
        def mod95(c, k, sign):
            if 32 <= c < 127:
                v = c - 32
                kv = (k - 32) % 95
                v = (v + sign * kv) % 95
                return 32 + v
            return c
        p = bytes(mod95(c, key[i % len(key)], sign) for i, c in enumerate(ct))
        best.append((sc(p), 'mod95%s %r' % ('+' if sign > 0 else '-', key), p))
        # mod 128
        p = bytes(((c + sign * key[i % len(key)]) % 128) for i, c in enumerate(ct))
        best.append((sc(p), 'mod128%s %r' % ('+' if sign > 0 else '-', key), p))
        p = bytes(((c - sign * key[i % len(key)]) % 128) for i, c in enumerate(ct))
        best.append((sc(p), 'mod128b %r' % (key,), p))

best.sort(reverse=True, key=lambda x: x[0])
for s, tag, p in best[:6]:
    print('%.3f' % s, tag)
    print(p)
    print('-' * 70)
