import base64, re, math, random, collections, sys

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)

def build(corpus_paths):
    s = ''
    for p in corpus_paths:
        t = open(p, encoding='utf-8', errors='ignore').read().lower()
        t = re.sub(r'[^a-záéíóúñü .,;:\'\-0-9\n]', ' ', t)
        t = re.sub(r'[ \t\r]+', ' ', t)
        s += t + ' '
    s = '   ' + s + '   '
    q = collections.Counter(s[i:i+4] for i in range(len(s) - 3))
    tot = float(sum(q.values()))
    return {g: math.log(v / tot) for g, v in q.items()}, math.log(0.02 / tot)

qlog, FLOOR = build(['corpus.txt', 'corpus_es.txt'])
print('model grams', len(qlog))

def score_full(p):
    t = p.decode('latin1').lower()
    return sum(qlog.get(t[i:i+4], FLOOR) for i in range(len(t) - 3))

def anneal(L, iters=40000, seed=1):
    rng = random.Random(seed)
    key = [rng.randrange(0x20, 0x40) for _ in range(L)]
    pt = [ct[i] ^ key[i % L] for i in range(n)]
    cur = score_full(bytes(pt))
    best, bestkey = cur, key[:]
    T0, T1 = 8.0, 0.02
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / iters)
        r = rng.randrange(L)
        old = key[r]
        new = rng.randrange(0x20, 0x40)
        if new == old:
            continue
        delta = 0.0
        i = r
        while i < n:
            for w in range(max(0, i - 3), i + 1):
                if w + 4 <= n:
                    chars = [chr(pt[w]), chr(pt[w+1]), chr(pt[w+2]), chr(pt[w+3])]
                    before = qlog.get(''.join(chars).lower(), FLOOR)
                    chars[i - w] = chr(ct[i] ^ new)
                    after = qlog.get(''.join(chars).lower(), FLOOR)
                    delta += after - before
            i += L
        if delta > 0 or rng.random() < math.exp(min(delta / max(T, 1e-6), 50)):
            for i in range(r, n, L):
                pt[i] = ct[i] ^ new
            key[r] = new
            cur += delta
            if cur > best:
                best, bestkey = cur, key[:]
    return best, bestkey

def dec(key):
    return bytes(c ^ key[i % len(key)] for i, c in enumerate(ct))

results = []
rngL = list(range(4, 41))
for L in rngL:
    for sd in (1, 2):
        sc, k = anneal(L, iters=30000, seed=sd)
        results.append((sc, L, bytes(k), dec(k)))

results.sort(reverse=True, key=lambda x: x[0])
for sc, L, k, p in results[:5]:
    print('L=%d score=%.0f key=%r' % (L, sc, k))
    print(p.decode('latin1'))
    print('-' * 72)
