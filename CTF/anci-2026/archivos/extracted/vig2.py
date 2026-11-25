import base64, os, urllib.request, math, re, json

cache = 'corpus.txt'
txt = open(cache, encoding='utf-8').read() if os.path.exists(cache) else ''

# preserve case, keep a realistic text alphabet
txt = re.sub(r'[^A-Za-z0-9 \n\'\"\.,;:\-\(\)\[\]{}/_!?%$#@&=+*]', ' ', txt)
txt = re.sub(r'[ \t]+', ' ', txt)

freq = {}
for ch in txt:
    freq[ch] = freq.get(ch, 0) + 1
tot = sum(freq.values())
logp = {ord(k): math.log(v / tot) for k, v in freq.items()}
floor = math.log(0.3 / tot)

def lp(b):
    return logp[b] if b in logp else (floor if 32 <= b < 127 else -15.0)

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)

res = []
for L in range(2, 65):
    key = []
    for r in range(L):
        idxs = range(r, n, L)
        best_k, best_s = 0, -1e18
        for k in range(256):
            s = 0.0
            for i in idxs:
                s += lp(ct[i] ^ k)
            if s > best_s:
                best_s, best_k = s, k
        key.append(best_k)
    p = bytes(c ^ key[i % L] for i, c in enumerate(ct))
    res.append((sum(lp(b) for b in p) / n, L, bytes(key), p))

res.sort(reverse=True)
for sc, L, k, p in res[:6]:
    print('L=%2d avg=%.3f key=%r' % (L, sc, k))
    print(p.decode('latin1'))
    print('-' * 72)
