import base64, re, math

ct = base64.b64decode(open('postcard.txt').read().split('\n')[2].strip())
n = len(ct)

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

base = b'2026-03-14'
pad = bytes(base[i % len(base)] for i in range(n))
dec = bytes(c ^ pad[i] for i, c in enumerate(ct))   # == ct ^ date

print('xor-date decode (letters only Caesar test):')
letters = 'abcdefghijklmnopqrstuvwxyz'
res = []
for s in range(26):
    out = []
    for b in dec:
        ch = chr(b)
        if ch.isalpha():
            lower = ch.lower()
            i = letters.index(lower)
            nc = letters[(i - s) % 26]
            out.append(nc if ch.islower() else nc.upper())
        else:
            out.append(ch)
    p = ''.join(out)
    res.append((sum(lp(ord(c)) for c in p) / n, s, p))
res.sort(reverse=True)
for sc, s, p in res[:3]:
    print('rot-%d avg=%.3f' % (s, sc))
    print(p)
    print('-' * 70)

print('\n=== arithmetic ops with date pad ===')
import itertools
def mods(c, k, op, m, off):
    if op == 'sub':
        v = (c - k) % m
    elif op == 'add':
        v = (c + k) % m
    elif op == 'xor':
        v = c ^ k
    return (v + off) % m + (32 if m == 95 else 0)
