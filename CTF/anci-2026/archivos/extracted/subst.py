import base64, re, math, random, string

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)

# ---- layer 1: XOR con la fecha ----
k = b'2026-03-14'
pad = bytes(k[i % 10] for i in range(n))
dec = bytes(c ^ pad[i] for i, c in enumerate(ct)).decode('latin1')

print('=== capa 1 (XOR fecha) ===')
print(dec)
print()

# ---- modelo de cuatrigramas ----
corpus = open('corpus.txt', encoding='utf-8').read().lower()
corpus = re.sub(r'[^a-z ]+', ' ', corpus)
corpus = re.sub(r' +', ' ', corpus)

qc = {}
for i in range(len(corpus) - 4):
    g = corpus[i:i+4]
    qc[g] = qc.get(g, 0) + 1
tot = sum(qc.values())
floor = math.log(0.01 / tot)
qlog = {g: math.log(v / tot) for g, v in qc.items()}
print('cuatrigramas distintos:', len(qlog))

# texto objetivo: solo letras y espacios (conservando longitudes)
target = ''.join(ch.lower() if ch.isalpha() else (' ' if ch in ' \n' else '|') for ch in dec)
work = target.replace('|', ' ')

def qscore(s):
    s = ' ' + s + ' '
    sc = 0.0
    for i in range(len(s) - 3):
        sc += qlog.get(s[i:i+4], floor)
    return sc

letters = string.ascii_lowercase
best = None
bestscore = -1e18

for attempt in range(40):
    perm = list(letters)
    random.shuffle(perm)
    mapping = dict(zip(letters, perm))
    cur = ''.join(mapping.get(c, c) for c in work)
    curs = qscore(cur)
    improved = True
    while improved:
        improved = False
        for a in letters:
            for b in letters:
                if a == b:
                    continue
                # swap the plaintext assignments of a and b
                inv = {v: k_ for k_, v in mapping.items()}
                pa, pb = mapping[a], mapping[b]
                if pa == pb:
                    continue
                mapping[a], mapping[b] = pb, pa
                cand = ''.join(mapping.get(c, c) for c in work)
                s = qscore(cand)
                if s > curs:
                    curs = s
                    improved = True
                else:
                    mapping[a], mapping[b] = pa, pb
    if curs > bestscore:
        bestscore = curs
        best = dict(mapping)

plain = ''.join(best.get(c, c) for c in work)
print('\n=== mejor descifrado (score %.0f) ===' % bestscore)
print(plain)
print()
print('mapeo cifrado->claro:')
print(' '.join('%s=%s' % (a, b) for a, b in sorted(best.items())))
