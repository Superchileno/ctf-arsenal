import base64, itertools, collections, math, re

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)

ALLOWED = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,;:\'"!?-_(){}[]/@#\n')
CRIB = b'flag{'

# model (mixed es/en)
s = ''
for p in ('corpus.txt', 'corpus_es.txt'):
    t = open(p, encoding='utf-8', errors='ignore').read().lower()
    t = re.sub(r'[^a-záéíóúñü .,;:\'\-0-9\n]', ' ', t)
    t = re.sub(r'[ \t\r]+', ' ', t)
    s += t + ' '
s = '   ' + s + '   '
q = collections.Counter(s[i:i+4] for i in range(len(s) - 3))
tot = float(sum(q.values()))
qlog = {g: math.log(v / tot) for g, v in q.items()}
FLOOR = math.log(0.02 / tot)

def sc(p):
    t = p.decode('latin1').lower()
    return sum(qlog.get(t[i:i+4], FLOOR) for i in range(len(t) - 3))

best = []
for L in range(2, 81):
    cand = []
    ok = True
    for r in range(L):
        opts = []
        for p in range(0x20, 0x40):
            if all(chr(ct[i] ^ p) in ALLOWED for i in range(r, n, L)):
                opts.append(p)
        if not opts:
            ok = False
            break
        cand.append(opts)
    if not ok:
        continue
    total = 1
    for o in cand:
        total *= len(o)
    if total > 400000:
        print('L=%d combos=%d (skip)' % (L, total))
        continue
    for combo in itertools.product(*cand):
        p = bytes(c ^ combo[i % L] for i, c in enumerate(ct))
        s2 = sc(p)
        best.append((s2, L, bytes(combo), p))
    print('L=%d combos=%d done' % (L, total))

best.sort(reverse=True, key=lambda x: x[0])
for s2, L, k, p in best[:6]:
    print('L=%d score=%.0f key=%r' % (L, s2, k))
    print(p.decode('latin1'))
    print('-' * 72)
