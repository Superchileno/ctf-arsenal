import base64, itertools, string, re
ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
n=len(ct)
P=bytes(a^b for a,b in zip(ct,(b'2026-03-14'*(n//10+1))[:n])).decode('latin1')

def vig_dec(s, key):
    out=[]; ki=0
    for ch in s:
        if ch.isalpha():
            k=ord(key[ki%len(key)].lower())-97 if key[ki%len(key)].isalpha() else int(key[ki%len(key)])
            base=ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch)-base-k)%26+base)); ki+=1
        else:
            out.append(ch)
    return ''.join(out)

keys=['keyremnantsignal','KEYREMNANTSIGNAL','key remnant signal','KEY REMNANT SIGNAL','keyremnant',
      'inkroute','mailstamp','inkroutemailstamp','inkroute mail stamp','fieldoffice','inkroutefieldoffice',
      '2026-03-14','20260314','2026','314','signal','remnant','softotp','soft-otp','otp','postcard',
      'sealedpostcardbody','inkroutesealedpostcardbody','keyremnant2026-03-14','2026-03-14signalkeyremnant']
for k in keys:
    for kk in (k, k.upper(), k.lower()):
        d=vig_dec(P,kk)
        if b'flag{' in d.encode() or 'flag{' in d:
            print('FLAGVIG',repr(kk),d)
        pr=sum(32<=ord(c)<127 or c=='\n' for c in d)/len(d)
        if pr>0.99:
            print(round(pr,3),repr(kk),d[:110].replace('\n','|'))
