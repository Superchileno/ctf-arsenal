import base64, collections, math, re
ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
n=len(ct)
P=bytes(a^b for a,b in zip(ct,(b'2026-03-14'*(n//10+1))[:n])).decode('latin1')

EN=[0.08167,0.01492,0.02782,0.04253,0.12702,0.02228,0.02015,0.06094,0.06966,0.00153,0.00772,0.04025,0.02406,
    0.06749,0.07507,0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,0.02360,0.00150,0.01974,0.00074]

def letters(s):
    return [i for i,ch in enumerate(s) if ch.isalpha()]

idxs=letters(P)
vals=[ord(P[i].lower())-97 for i in idxs]

def chi2(v):
    c=collections.Counter(v); L=len(v)
    s=0
    for a in range(26):
        exp=EN[a]*L
        obs=c.get(a,0)
        s+=(obs-exp)**2/max(exp,1e-9)
    return s

def decrypt(key):
    out=[]; ki=0
    for ch in P:
        if ch.isalpha():
            k=key[ki%len(key)]
            base=ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch)-base-k)%26+base)); ki+=1
        else: out.append(ch)
    return ''.join(out)

COMMON=('the of and to in that is was he for it with as his on be at by i this had not are but from or have an they which one you were her all she there would their we him been has when who will more no if out so said what up its about into than them can only other new some could time these two may then do first any my now such like our over man me even most made after also did many before must through back years where much your way well down should because each just those people mr how too little state good very make world still own see men work long get here between both life being under never day same another know while last might us great old year off come since against go came right used take three states himself few house use during without again place around however home small found thought went say part once general high upon school every does got united left number course war until always away something fact water though less public put think almost hand enough far took head yet government system better set told nothing night end why called eyes find going look asked later knew point next program business give order present national keep big want girl room')
words=set(COMMON.split())

def score(t):
    ws=re.findall(r'[A-Za-z]+', t.lower())
    return sum(1 for w in ws if w in words)

res=[]
for L in range(1,41):
    key=[]
    for j in range(L):
        v=vals[j::L]
        best=None
        for k in range(26):
            c=chi2([(x-k)%26 for x in v])
            if best is None or c<best[0]: best=(c,k)
        key.append(best[1])
    d=decrypt(key)
    res.append((score(d),L,bytes(k+65 for k in key),d))
res.sort(reverse=True)
for sc,L,key,d in res[:10]:
    print('score',sc,'L',L,'key',key.decode())
    print(d)
    print()
