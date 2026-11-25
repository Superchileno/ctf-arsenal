import base64, collections, math, string
ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
n=len(ct)
k=b'2026-03-14'
pad=(k*(n//len(k)+1))[:n]
P=bytes(a^b for a,b in zip(ct,pad)).decode('latin1')
print(P)
print('len',len(P))
# letter positions and values
idx=[i for i,ch in enumerate(P) if ch.isalpha()]
vals=[ord(P[i].lower())-97 for i in idx]
N=len(vals)
print('letters',N)
def ic(v):
    c=collections.Counter(v); L=len(v)
    if L<2: return 0
    return sum(x*(x-1) for x in c.values())/(L*(L-1))
print('overall IC', round(ic(vals),4))
scores=[]
for L in range(1,41):
    ics=[ic(vals[i::L]) for i in range(L)]
    scores.append((sum(ics)/L,L,round(min(ics),3),round(max(ics),3)))
scores.sort(reverse=True)
print('best key lengths by avg IC:')
for s in scores[:8]: print(s)
