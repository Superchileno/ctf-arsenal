d=open("ANCI/net/extracted/capture.pcap","rb").read()
print("size",len(d), d[:24].hex())
for i in range(0,len(d),16):
    b=d[i:i+16]
    print(f"{i:04x}  {b.hex(' '):<47}  {''.join(chr(c) if 32<=c<127 else '.' for c in b)}")
