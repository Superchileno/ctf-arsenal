d=open("ANCI/forense/extracted/unalloc.raw","rb").read()
def dump(off,n=512):
    chunk=d[off:off+n]
    for i in range(0,len(chunk),16):
        b=chunk[i:i+16]
        print(f"{off+i:08x}  {b.hex(' '):<47}  {''.join(chr(c) if 32<=c<127 else '.' for c in b)}")
for off in [983040, 3727360]:
    print("=== offset",off,"===")
    dump(off, 768)
    print()
