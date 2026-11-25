import base64, os, urllib.request, math, re

cache = 'corpus.txt'
if not os.path.exists(cache):
    u = "https://www.gutenberg.org/files/1342/1342-0.txt"
    req = urllib.request.Request(u, headers={'User-Agent': 'ctf/1.0'})
    txt = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'ignore')
    open(cache, 'w', encoding='utf-8').write(txt)
else:
    txt = open(cache, encoding='utf-8').read()

# normalize to typical postcard alphabet
txt = re.sub(r'[^a-zA-Z0-9 \n\.,;:\'\-\(\)/]', ' ', txt)
txt = re.sub(r'[ \t]+', ' ', txt).lower()

freq = {}
for ch in txt:
    freq[ch] = freq.get(ch, 0) + 1
tot = sum(freq.values())
logp = {ord(k): math.log(v / tot) for k, v in freq.items()}
floor = math.log(0.5 / tot)
print('corpus chars', tot, 'alphabet', len(logp))

def lp(b):
    if b in logp:
        return logp[b]
    if 32 <= b < 127:
        return floor
    return -14

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)

results = []
for L in range(2, 121):
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
    sc = sum(lp(b) for b in p)
    # chi-square-ish normalization not needed; compare per-char average
    results.append((sc / n, L, bytes(key), p))

results.sort(reverse=True)
for sc, L, k, p in results[:8]:
    print('L=%d avg=%.3f key=%s' % (L, sc, k))
    print(p.decode('latin1'))
    print('-' * 70)
