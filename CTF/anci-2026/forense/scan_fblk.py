import json,re
d=open("ANCI/forense/extracted/unalloc.raw","rb").read()
i=0; found=[]
while True:
    off=d.find(b"FBLK",i)
    if off<0: break
    i=off+1
    if off+12>len(d): continue
    ver=int.from_bytes(d[off+4:off+8],"little")
    ln=int.from_bytes(d[off+8:off+12],"little")
    if ver!=1 or ln<=0 or ln>4096: continue
    js=d[off+12:off+12+ln]
    if not (js.startswith(b"{") and js.endswith(b"}")): continue
    try: o=json.loads(js)
    except Exception: continue
    found.append((off,o))
    print(f"OFFSET {off:#x} (cluster {off//4096}, sector {off//512}) kind={o.get('kind')} batch={o.get('batch')} hint={o.get('xor_hint')} token={o.get('token_xor_hex')}")
    if o.get("token_xor_hex") and o["token_xor_hex"]!="deadbeef":
        raw=bytes.fromhex(o["token_xor_hex"]); key=o.get("xor_hint","FBLK").encode()
        dec=bytes(b^key[k%len(key)] for k,b in enumerate(raw))
        print("   ->", dec.decode("utf-8", "backslashreplace"))
print("total",len(found))
print("--- cluster map ---")
for cl in [80,240,910,1500,40,60]:
    print(cl, hex(cl*4096))
