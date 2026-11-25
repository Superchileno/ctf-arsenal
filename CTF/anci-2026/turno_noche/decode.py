d=open("ANCI/turno_noche/night_shift","rb").read()
import re
out=[]
# find all 15-byte-ish instruction groups: 10 00 xx 00 10 01 yy 00 22 00 01 12 00 idx 01
for m in re.finditer(rb"\x10\x00(.)\x00\x10\x01(.)\x00\x22\x00\x01\x12\x00(.)\x01", d, re.S):
    x,y,idx=m.group(1)[0],m.group(2)[0],m.group(3)[0]
    out.append((idx,x,y,x^y,chr(x^y) if 32<=x^y<127 else "."))
out.sort()
print(len(out))
for t in out: print(t)
print("FLAG:", "".join(t[4] for t in out))
