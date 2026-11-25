import base64, re, math, collections

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)

corpus = open('corpus.txt', encoding='utf-8').read()
corpus = re.sub(r'[^A-Za-z0-9 \n\.,;:\'\-\(\)!?"]', ' ', corpus)
corpus = re.sub(r'[ \t]+', ' ', corpus).lower()
s = '  ' + corpus + '  '

q = collections.Counter()
for i in range(len(s) - 3):
    q[s[i:i+4]] += 1
tot = sum(q.values())
qlog = {g: math.log(v / tot) for g, v in q.items()}
QFLOOR = math.log(0.05 / tot)

ALLOWED = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,;:\'"-(){}_/!?\n')

def lm(ch):
    return 0.0 if ch in ALLOWED else -25.0

def beam(pad_alphabet, width=1500, topk=5):
    beams = [('', 0.0)]
    for i in range(n):
        cands = []
        c = ct[i]
        opts = [(c ^ p) for p in pad_alphabet]
        for text, sc in beams:
            ctx = text[-3:].lower()
            for code in opts:
                ch = chr(code)
                if ch in ALLOWED:
                    sc2 = sc + qlog.get(ctx + ch, QFLOOR) + lm(ch)
                elif code in (10, 13):
                    ch = '\n'
                    sc2 = sc + qlog.get(ctx + ch, QFLOOR) - 2
                else:
                    continue
                cands.append((text + ch, sc2))
        if not cands:
            return []
        cands.sort(key=lambda x: -x[1])
        beams = cands[:width]
    beams.sort(key=lambda x: -x[1])
    return beams[:topk]

for label, alpha in [('pad 0x20-0x2f (16)', list(range(0x20, 0x30))),
                     ('pad 0x20-0x3f (32)', list(range(0x20, 0x40)))]:
    print('=' * 30, label)
    res = beam(alpha)
    for text, sc in res:
        print('score %.1f' % sc)
        print(text)
        print('-' * 60)
