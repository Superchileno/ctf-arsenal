import struct, sys, zlib, os, multiprocessing as mp, zipfile, tempfile

CRC_TABLE=[]
for i in range(256):
    c=i
    for _ in range(8):
        c=(c>>1)^0xEDB88320 if c&1 else c>>1
    CRC_TABLE.append(c)

def crc32(data):
    c=0xFFFFFFFF
    for b in data:
        c=CRC_TABLE[(c^b)&0xff]^(c>>8)
    return c^0xFFFFFFFF

def keys(pwd):
    k0,k1,k2=0x12345678,0x23456789,0x34567890
    for b in pwd:
        k0=(k0>>8)^CRC_TABLE[(k0^b)&0xff]
        k1=(k1+(k0&0xff))&0xFFFFFFFF
        k1=(k1*134775813+1)&0xFFFFFFFF
        k2=(k2>>8)^CRC_TABLE[(k2^(k1>>24))&0xff]
    return [k0,k1,k2]

def decrypt(keys, data):
    k0,k1,k2=keys
    out=bytearray(len(data))
    for i,b in enumerate(data):
        t=(k2|2)&0xffff
        y=((t*(t^1))>>8)&0xff
        p=b^y
        out[i]=p
        k0=(k0>>8)^CRC_TABLE[(k0^p)&0xff]
        k1=(k1+(k0&0xff))&0xFFFFFFFF
        k1=(k1*134775813+1)&0xFFFFFFFF
        k2=(k2>>8)^CRC_TABLE[(k2^(k1>>24))&0xff]
    return bytes(out), [k0,k1,k2]

class Target:
    def __init__(self, path, entry=0):
        z=zipfile.ZipFile(path)
        self.i=z.infolist()[entry]
        with open(path,'rb') as f:
            f.seek(self.i.header_offset)
            h=f.read(30)
            n,e=struct.unpack('<HH',h[26:30])
            f.read(n+e)
            self.head=f.read(12)
            self.body=f.read(max(0,self.i.compress_size-12))
        self.check=((self.i._raw_time>>8)&0xff) if (self.i.flag_bits&0x08) else ((self.i.CRC>>24)&0xff)
        self.method=self.i.compress_type
        self.crc=self.i.CRC
        self.usz=self.i.file_size
        self.name=self.i.filename

    def test(self, pwd):
        h,k=decrypt(keys(pwd), self.head)
        if h[11]!=self.check:
            return False
        body,_=decrypt(k, self.body)
        try:
            if self.method==8:
                o=zlib.decompressobj(-15)
                plain=o.decompress(body)+o.flush()
            else:
                plain=body
        except Exception:
            return False
        return len(plain)==self.usz and crc32(plain)==self.crc

    def extract(self, pwd):
        if not self.test(pwd):
            return None
        h,k=decrypt(keys(pwd), self.head)
        body,_=decrypt(k, self.body)
        if self.method==8:
            o=zlib.decompressobj(-15)
            return o.decompress(body)+o.flush()
        return body

G={'path':None,'entry':0}

def _worker(args):
    path, entry, shard = args
    t=Target(path, entry)
    hits=[]
    with open(shard,'rb') as f:
        for line in f:
            pwd=line.rstrip(b'\r\n')
            if not pwd: continue
            if t.test(pwd):
                hits.append(pwd)
                print('FOUND:', pwd.decode('latin1'), flush=True)
    return hits

def shard_file(src, n, d):
    paths=[os.path.join(d,'shard%d.txt'%i) for i in range(n)]
    fs=[open(p,'wb') for p in paths]
    try:
        with open(src,'rb') as f:
            for i,line in enumerate(f):
                fs[i%n].write(line)
    finally:
        for f in fs: f.close()
    return paths

def run(src, path, entry, procs=8):
    G['path']=path; G['entry']=entry
    tmp=tempfile.mkdtemp()
    shards=shard_file(src, procs, tmp)
    hits=[]
    with mp.Pool(procs) as pool:
        for r in pool.imap_unordered(_worker, [(path,entry,s) for s in shards]):
            hits+=r
    return hits

if __name__=='__main__':
    path=sys.argv[1]; entry=int(sys.argv[2]); wl=sys.argv[3]
    print('hits', run(wl, path, entry))
