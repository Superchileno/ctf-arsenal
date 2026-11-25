import base64, itertools, collections, math, re

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)
CRIB = b'flag{'

# quadgram model
corpus = open('corpus.txt', encoding='utf-8').read().lower()
corpus = re.sub(r'[^a-z .,;:\'\-0-9\n]', ' ', corpus)
s = '   ' + corpus + '   '
q = collections.Counter(s[i:i+4] for i in range(len(s) - 3))
tot = float(sum(q.values()))
qlog = {g: math.log(v / tot) for g, v in q.items()}
FLOOR = math.log(0.02 / tot)

def sc(p):
    t = p.decode('latin1').lower()
    return sum(qlog.get(t[i:i+4], FLOOR) for i in range(len(t) - 3))

hits = []
bests = []
for L in (1, 2, 3):
    for key in itertools.product(range(256), repeat=L):
        p = bytes(c ^ key[i % L] for i, c in enumerate(ct))
        if CRIB in p:
            hits.append((L, key, p))
            print('HIT L=%d key=%r' % (L, key))
            print(p)
    print('L=%d done' % L)
print('hits', len(hits))
