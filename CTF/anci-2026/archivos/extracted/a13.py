import base64, collections, math
ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
n=len(ct)
k=b'2026-03-14'
pad=(k*(n//len(k)+1))[:n]
p=bytes(a^b for a,b in zip(ct,pad))
print(repr(p))
print()
print(p.decode('latin1'))
print()
s=p.decode('latin1')
letters=[c for c in s if c.isalpha()]
c=collections.Counter(letters)
print(len(letters), c.most_common())
N=len(letters)
ic=sum(v*(v-1) for v in c.values())/(N*(N-1))
print('IC', round(ic,4))
# word pattern
import re
words=re.findall(r"[A-Za-z]+", s)
print([(w,''.join(str(sorted(w).index(x)) for x in w)) for w in words[:20]])
