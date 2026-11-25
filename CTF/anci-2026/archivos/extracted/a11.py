import base64, math, string
ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
n=len(ct)
freq = {
 ' ':0.182,'e':0.102,'t':0.075,'a':0.065,'o':0.061,'i':0.057,'n':0.057,'s':0.053,'h':0.049,'r':0.049,
 'd':0.034,'l':0.033,'u':0.023,'c':0.022,'m':0.020,'f':0.018,'w':0.017,'g':0.016,'p':0.015,'y':0.014,
 'b':0.012,'v':0.008,'k':0.006,'x':0.002,'j':0.002,'q':0.001,'z':0.001,
 'E':0.010,'T':0.010,'A':0.008,'S':0.006,'I':0.005,'O':0.005,'N':0.005,'R':0.005,'H':0.004,'L':0.003,
 'D':0.003,'C':0.003,'U':0.003,'M':0.003,'P':0.002,'F':0.002,'G':0.002,'W':0.002,'Y':0.002,'B':0.002,
 ',':0.010,'.':0.010,'-':0.003,'\n':0.010,"'":0.002,'{':0.0005,'}':0.0005,'_':0.001,'0':0.001,'1':0.001,
 '2':0.001,'3':0.001,'4':0.001,'5':0.001,'6':0.001,'7':0.001,'8':0.001,'9':0.001,'!':0.001,'?':0.001,
 ':':0.001,';':0.001,'(' :0.001,')':0.001,'/':0.001,'=':0.001,'"':0.001,'$':0.001,'&':0.001,'%':0.001,
 '@':0.0002,'#':0.0002,'*':0.0002,'+':0.0002,'<':0.0002,'>':0.0002,'[':0.0002,']':0.0002,'|':0.0002
}
def lp(c):
    ch=chr(c)
    if ch in freq: return math.log(freq[ch])
    return math.log(1e-5)
best=[]
for L in range(1,65):
    key=[]
    total=0
    for j in range(L):
        cols=[ct[i] for i in range(j,n,L)]
        bestk=None;bestsc=-1e9
        for k in range(64):
            sc=sum(lp(c^k) for c in cols)
            if sc>bestsc: bestsc=sc;bestk=k
        key.append(bestk); total+=bestsc
    p=bytes(ct[i]^key[i%L] for i in range(n))
    pr=sum(32<=c<127 or c==10 for c in p)/n
    best.append((total/n,pr,L,bytes(key),p))
best.sort(reverse=True)
for sc,pr,L,key,p in best[:8]:
    print(round(sc,3),round(pr,3),'L=',L,'key=',key)
    print(p[:120])
    print()
