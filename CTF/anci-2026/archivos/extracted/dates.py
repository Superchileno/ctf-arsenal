import base64, re, math, itertools

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
txt = open('corpus.txt', encoding='utf-8').read()
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

def score(p):
    return sum(lp(b) for b in p) / len(p)

dates = ['2026-03-14', '2026-10-14', '14-03-2026', '14-10-2026', '2026/03/14',
         '2026/10/14', '20260314', '20261014', '14032026', '14102026',
         '2026-3-14', '2026-03-14T00:00', '2026-03-14 00:00:00', '03/14/2026',
         '10/14/2026', '2026-03-14T00:00:00Z']

prefixes = ['', 'inkroute', 'inkroute-', 'inkroute:', 'KEY REMNANT', 'signal',
            'inkroute field office', 'Inkroute', 'key', 'otp', 'soft-otp']
suffixes = ['', 'inkroute', '-inkroute', 'inkroute field office']

cands = set()
for d in dates:
    for p in prefixes:
        for s in suffixes:
            cands.add((p + d + s).encode())
            cands.add((p + ' ' + d + ' ' + s).encode())

best = []
for k in cands:
    if not k:
        continue
    p = bytes(c ^ k[i % len(k)] for i, c in enumerate(ct))
    best.append((score(p), k, p))
best.sort(reverse=True)
for sc, k, p in best[:5]:
    print(round(sc, 3), k)
    print(p.decode('latin1'))
    print('-' * 70)

print('\n=== date decode repr ===')
k = b'2026-03-14'
p = bytes(c ^ k[i % len(k)] for i, c in enumerate(ct))
print(repr(p))
print('\nct tail:      ', ct[-24:].hex())
print('pad tail:     ', bytes(k[i % 10] for i in range(len(ct)))[-24:].hex())
print('pt tail:      ', p[-24:].hex())
