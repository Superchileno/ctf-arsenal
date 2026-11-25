import base64
ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
def score(b):
    return sum(32 <= c < 127 or c in (10,13,9) for c in b)/len(b)
def rot(b,n):
    n%=8
    return bytes(((c<<n)|(c>>(8-n)))&0xFF if n else c for c in b)
for n in range(8):
    for d in ('l','r'):
        p = rot(ct,n) if d=='l' else rot(ct,8-n)
        print(d,n,round(score(p),3), p[:60])
# nibble swap
p=bytes(((c<<4)|(c>>4))&0xFF for c in ct)
print('nib', score(p), p[:60])
# xor with 0x20, 0x40, 0x60
for k in (0x20,0x40,0x60,0x80,0xff):
    p=bytes(c^k for c in ct)
    print('xor',hex(k), score(p), p[:60])
