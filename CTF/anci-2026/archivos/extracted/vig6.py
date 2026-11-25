import base64, collections, math, re, random

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
k = b'2026-03-14'
dec = bytes(c ^ k[i % 10] for i, c in enumerate(ct)).decode('latin1')

s = ''
for p in ('corpus.txt',):
    t = open(p, encoding='utf-8', errors='ignore').read().lower()
    t = re.sub(r'[^a-z .,;:\'\-0-9\n]', ' ', t)
    t = re.sub(r'[ \t\r]+', ' ', t)
    s += t + ' '
s = '   ' + s + '   '
q = collections.Counter(s[i:i+4] for i in range(len(s) - 3))
tot = float(sum(q.values()))
qlog = {g: math.log(v / tot) for g, v in q.items()}
FLOOR = math.log(0.02 / tot)

pos = [i for i, ch in enumerate(dec) if ch.isalpha()]
letters = [dec[i].lower() for i in pos]
N = len(letters)

def render(shifts):
    out = list(dec)
    for j, i in enumerate(pos):
        c = chr((ord(letters[j]) - 97 - shifts[j % 6]) % 26 + 97)
        out[i] = c if dec[i].islower() else c.upper()
    return ''.join(out)

def score(shifts):
    t = render(shifts).lower()
    return sum(qlog.get(t[i:i+4], FLOOR) for i in range(len(t) - 3))

best = None
bestsc = -1e18
starts = [[0] * 6, [5, 13, 0, 19, 4, 17], [18, 4, 2, 20, 17, 8]]
rng = random.Random(7)
for _ in range(60):
    starts.append([rng.randrange(26) for _ in range(6)])

for st in starts:
    sh = st[:]
    cur = score(sh)
    improved = True
    while improved:
        improved = False
        for r in range(6):
            for v in range(26):
                if v == sh[r]:
                    continue
                old = sh[r]
                sh[r] = v
                s2 = score(sh)
                if s2 > cur:
                    cur = s2
                    improved = True
                else:
                    sh[r] = old
    if cur > bestsc:
        bestsc = cur
        best = sh[:]

print('best shifts:', best, 'score %.0f' % bestsc)
print()
print(render(best))
print()
# also show the key as letters
print('keyword:', ''.join(chr(97 + (26 - b) % 26) for b in best))
