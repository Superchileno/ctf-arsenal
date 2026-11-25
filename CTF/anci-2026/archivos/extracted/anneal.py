import base64, re, math, random, collections

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)

# ---- modelo de cuatrigramas ----
corpus = open('corpus.txt', encoding='utf-8').read().lower()
corpus = re.sub(r'[^a-z .,;:\'\-0-9\n]', ' ', corpus)
corpus = re.sub(r'[ \t]+', ' ', corpus)
s = '   ' + corpus + '   '
q = collections.Counter()
for i in range(len(s) - 3):
    q[s[i:i+4]] += 1
tot = float(sum(q.values()))
qlog = {g: math.log(v / tot) for g, v in q.items()}
FLOOR = math.log(0.02 / tot)

def gscore(t):
    v = qlog.get(t, FLOOR)
    return v

def score_full(text):
    t = text.lower()
    return sum(gscore(t[i:i+4]) for i in range(len(t) - 3))

def anneal(L, iters=60000, seed=1):
    rng = random.Random(seed)
    key = [rng.randrange(0x20, 0x40) for _ in range(L)]
    pt = [ct[i] ^ key[i % L] for i in range(n)]
    text = ''.join(chr(c) for c in pt)
    cur = score_full(text)

    best = cur
    bestkey = key[:]
    T0, T1 = 3.0, 0.05
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
                    a = chr(pt[w])
                    b = chr(pt[w + 1])
                    c = chr(pt[w + 2])
                    d = chr(pt[w + 3])
                    before = qlog.get((a + b + c + d).lower(), FLOOR)
                    # replace char at i
                    chars = [a, b, c, d]
                    chars[i - w] = chr(ct[i] ^ new)
                    after = qlog.get(''.join(chars).lower(), FLOOR)
                    delta += after - before
            i += L
        if delta > 0 or rng.random() < math.exp(delta / max(T, 1e-6)):
            for i in range(r, n, L):
                pt[i] = ct[i] ^ new
            key[r] = new
            cur += delta
            if cur > best:
                best = cur
                bestkey = key[:]
    return best, bestkey

def decrypt(key):
    return bytes(c ^ key[i % len(key)] for i, c in enumerate(ct))

results = []
for L in range(4, 41):
    for sd in (1, 2, 3):
        sc, k = anneal(L, iters=25000, seed=sd)
        results.append((sc, L, bytes(k), decrypt(k)))

results.sort(reverse=True, key=lambda x: x[0])
for sc, L, k, p in results[:6]:
    print('L=%d score=%.0f key=%r' % (L, sc, k))
    print(p)
    print('-' * 72)
