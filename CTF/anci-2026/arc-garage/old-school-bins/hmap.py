import gdb, struct

class Heap:
    def __init__(self):
        self.inferior = gdb.selected_inferior()
    def u8(self,a): return struct.unpack('<B', self.read(a,1))[0]
    def u16(self,a): return struct.unpack('<H', self.read(a,2))[0]
    def u32(self,a): return struct.unpack('<I', self.read(a,4))[0]
    def u64(self,a): return struct.unpack('<Q', self.read(a,8))[0]
    def read(self,a,n):
        try: return self.inferior.read_memory(a,n).tobytes()
        except Exception: return b'\x00'*n
    def chunk(self,p):
        if p==0: return None
        off = self.u16(p-2); idx = self.u8(p-3)&31
        chk = self.u8(p-4)
        base = p - 16*off - 16
        meta = self.u64(base)
        # meta fields
        mem = self.u64(meta+16)
        avail = self.u32(meta+24); freed=self.u32(meta+28)
        bits = self.u64(meta+32)
        last_idx = bits & 31
        freeable = (bits>>5)&1
        sc = (bits>>6)&0x3f
        maplen = (bits>>12)&((1<<52)-1)
        return dict(p=p,off=off,idx=idx,chk=chk,base=base,meta=meta,mem=mem,
                    avail=avail,freed=freed,last_idx=last_idx,freeable=freeable,
                    sc=sc,maplen=maplen)

gdb.execute('set pagination off')
gdb.execute('set confirm off')
gdb.execute('break idx_cmp_qsort')
gdb.execute('run < /tmp/poc.txt')
H=Heap()
garage = int(gdb.parse_and_eval('(unsigned long)&garage'))
count  = int(gdb.parse_and_eval('(int)car_count'))
print("count", count)
seen={}
for i in range(count):
    c = H.u64(garage+8*i)
    if not c: continue
    ch = H.chunk(c)
    print("car %2d struct=%#x off=%d idx=%d base=%#x sc=%d last=%d map=%d avail=%#x freed=%#x" % (
        i,c,ch['off'],ch['idx'],ch['base'],ch['sc'],ch['last_idx'],ch['maplen'],ch['avail'],ch['freed']))
    for name,fo in (('model',0),('team',8),('driver',16),('engine',24)):
        s=H.u64(c+fo)
        if s:
            sh=H.chunk(s)
            print("      %-6s %#x off=%d idx=%d base=%#x sc=%d last=%d map=%d" % (
                name,s,sh['off'],sh['idx'],sh['base'],sh['sc'],sh['last_idx'],sh['maplen']))
