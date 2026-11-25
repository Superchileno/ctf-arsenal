import base64, collections, math, re

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
k = b'2026-03-14'
dec = bytes(c ^ k[i % 10] for i, c in enumerate(ct)).decode('latin1')

# quadgram model (mixed)
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

# letter-only stream with position map
pos = [i for i, ch in enumerate(dec) if ch.isalpha()]
letters = [dec[i].lower() for i in pos]
N = len(letters)

def rebuild(shifts):
    out = list(dec)
    for j, i in enumerate(pos):
        sh = shifts[j]
        if sh == 0:
            continue
        base = ord(dec[i])
        lower = dec[i].islower()
        c = chr((ord(letters[j]) - 97 - sh) % 26 + 97)
        out[i] = c if lower else c.upper()
    return ''.join(out)

freq = collections.Counter()
for p in ('corpus.txt', 'corpus_es.txt'):
    t = open(p, encoding='utf-8', errors='ignore').read().lower()
    for ch in t:
        if ch.isalpha():
            freq[ch] += 1
totf = sum(freq.values())
fb = {c: freq.get(c, 0) / totf for c in 'abcdefghijklmnopqrstuvwxyz'}

def lf(c):
    return math.log(max(fb.get(c, 0.0), 1e-6))

results = []
for L in range(2, 61):
    shifts = [0] * N
    for r in range(L):
        idx = list(range(r, N, L))
        best, bs = None, -1e18
        for sh in range(26):
            sc = sum(lf(chr((ord(letters[j]) - 97 - sh) % 26 + 97)) for j in idx)
            if sc > bs:
                bs, best = sc, sh
        for j in idx:
            shifts[j] = best
    text = rebuild(shifts)
    t2 = text.lower()
    sc2 = sum(qlog.get(t2[i:i+4], FLOOR) for i in range(len(t2) - 3))
    results.append((sc2, L, text))

results.sort(reverse=True, key=lambda x: x[0])
for sc2, L, text in results[:5]:
    print('L=%d score=%.0f' % (L, sc2))
    print(text)
    print('-' * 72)
