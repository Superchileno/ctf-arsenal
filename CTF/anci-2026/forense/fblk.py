import re,binascii
d=open("ANCI/forense/extracted/unalloc.raw","rb").read()
off=d.find(b"FBLK")
while off!=-1:
    ver=int.from_bytes(d[off+4:off+8],"little")
    ln=int.from_bytes(d[off+8:off+12],"little")
    js=d[off+12:off+12+ln]
    print("=== FBLK at",hex(off),"v",ver,"len",ln)
    print(js.decode("utf-8","replace"))
    import json
    try:
        o=json.loads(js)
        hx=o.get("token_xor_hex")
        if hx and hx!="deadbeef":
            key=(o.get("xor_hint") or "FBLK").encode()
            raw=bytes.fromhex(hx) if len(hx)%2==0 else None
            print("hexlen",len(hx),"raw",raw)
            if raw:
                out=bytes(b^key[i%len(key)] for i,b in enumerate(raw))
                print("DECODED:",out.decode("utf-8","replace"))
    except Exception as e: print("json err",e)
    off=d.find(b"FBLK",off+4)
