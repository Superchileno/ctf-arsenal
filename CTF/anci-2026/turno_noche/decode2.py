import re
d=open("ANCI/turno_noche/night_shift","rb").read()
pairs=[]
pat=rb"\x10\x01(.)\x00\x22\x00\x01\x10\x02(.)\x00\x30\x00\x02\x42\xd6\x02\x11\x00(.)\x00"
for m in re.finditer(pat,d,re.S):
    a,b,idx=m.group(1)[0],m.group(2)[0],m.group(3)[0]
    pairs.append((idx,a,b,a^b,chr(a^b) if 32<=a^b<127 else "."))
pairs.sort()
print(len(pairs))
for p in pairs: print(p)
print("PASS:", "".join(p[4] for p in pairs))
