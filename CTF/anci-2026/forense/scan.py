import re
d=open("ANCI/forense/extracted/unalloc.raw","rb").read()
print("size",len(d))
for kw in [b"flag{",b"frostbook",b"COLD",b"LEDGER",b"ledger"]:
    idxs=[m.start() for m in re.finditer(re.escape(kw),d)]
    print(kw, len(idxs), idxs[:20])
for m in re.finditer(rb"flag\{[^}]{0,100}\}", d):
    print("FLAG at",m.start(),m.group().decode(errors="replace"))
