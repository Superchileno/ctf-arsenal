import base64, itertools
ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
n=len(ct)
def test(k, tag):
    pad=(k*(n//len(k)+1))[:n]
    p=bytes(a^b for a,b in zip(ct,pad))
    pr=sum(32<=c<127 or c==10 for c in p)/n
    return pr,p
cands = ['2026-03-14','2026-03-14T00:00:00','20260314','14-03-2026','14/03/2026','2026/03/14',
         '2026-03-14 00:00:00','2026-3-14','260314','March 14, 2026','2026-03-14T00:00:00Z',
         'KEY REMNANT','KEY REMNANT SIGNAL','Inkroute','inkroute field office','Inkroute mail stamp',
         'soft-otp','inkroute','Inkroute sealed postcard body','postcard','sealed postcard','stamp_scan',
         'Inkroute field office','DATE 2026-03-14','2026','0314','314','mara']
for c in cands:
    for k in (c.encode(), c.lower().encode(), c.upper().encode()):
        pr,p=test(k,'')
        if pr>0.9:
            print(round(pr,3),repr(k),p[:100])
