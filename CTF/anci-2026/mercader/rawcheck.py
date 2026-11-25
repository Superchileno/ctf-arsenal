import zlib, struct

def raw_entries(path):
    d=open(path,'rb').read()
    i=0
    out=[]
    while True:
        sig=d.find(b'PK\x03\x04', i)
        if sig<0: break
        (ver, flag, method, t, dt, crc, csz, usz, nlen, elen)=struct.unpack('<HHHHHIIIHH', d[sig+4:sig+30])
        name=d[sig+30:sig+30+nlen]
        off=sig+30+nlen+elen
        out.append((name, flag, method, csz, usz, crc, off))
        i=off+max(csz,0)
    return out, d

for f in ['oro','plata','plomo']:
    p=r'ANCI\mercader\extract\%s.zip'%f
    ents,d=raw_entries(p)
    print('==',f)
    for (name,flag,method,csz,usz,crc,off) in ents:
        raw=d[off:off+csz]
        print(' ',name,'flag',flag,'method',method,'csz',csz,'usz',usz,'crc',hex(crc))
        for skip in (0,12):
            try:
                o=zlib.decompressobj(-15)
                res=o.decompress(raw[skip:])+o.flush()
                print('    skip',skip,'-> OK len',len(res),res[:16].hex(), 'eof',o.eof)
            except Exception as e:
                print('    skip',skip,'-> fail',e)
