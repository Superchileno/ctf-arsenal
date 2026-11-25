import gdb, struct

class Heap:
    def __init__(self): self.inf=gdb.selected_inferior()
    def read(self,a,n):
        try: return self.inf.read_memory(a,n).tobytes()
        except Exception: return b'\x00'*n
    def u8(self,a): return self.read(a,1)[0]
    def u16(self,a): return struct.unpack('<H',self.read(a,2))[0]
    def u32(self,a): return struct.unpack('<I',self.read(a,4))[0]
    def u64(self,a): return struct.unpack('<Q',self.read(a,8))[0]
    def chunk(self,p):
        if not p: return None
        off=self.u16(p-2); idx=self.u8(p-3)&31; chk=self.u8(p-4)
        base=p-16*off-16; meta=self.u64(base)
        mem=self.u64(meta+16); avail=self.u32(meta+24); freed=self.u32(meta+28)
        bits=self.u64(meta+32)
        return dict(p=p,off=off,idx=idx,chk=chk,base=base,meta=meta,mem=mem,
                    avail=avail,freed=freed,last=bits&31,freeable=(bits>>5)&1,
                    sc=(bits>>6)&0x3f,maplen=(bits>>12)&((1<<52)-1))

gdb.execute('set pagination off'); gdb.execute('set confirm off')
gdb.execute('break idx_cmp_qsort'); gdb.execute('run < /tmp/poc.txt')
H=Heap()
garage=int(gdb.parse_and_eval('(unsigned long)&garage')); count=int(gdb.parse_and_eval('(int)car_count'))
print("count",count)
groups={}
for i in range(count):
    c=H.u64(garage+8*i)
    if not c: continue
    for off in (0,8,16,24):
        s=H.u64(c+off)
        if s:
            ch=H.chunk(s)
            if ch: groups[ch['base']]=ch
# print chains for each distinct group
for g,ch in sorted(groups.items()):
    print("\nGROUP %#x sc=%d last=%d map=%d avail=%#x freed=%#x meta=%#x" % (
        g,ch['sc'],ch['last'],ch['maplen'],ch['avail'],ch['freed'],ch['meta']))
    cur=g; depth=0
    while depth<5:
        pch=H.chunk(cur)
        if pch is None: break
        if pch['base']==cur:  # self? shouldn't
            break
        print("   parent %#x  slot_idx=%d off_units=%d off_in_slot=%d  psc=%d pmap=%d plasty=%d" % (
            pch['base'],pch['idx'],pch['off'],pch['off']-pch['sc']*pch['idx'],
            pch['sc'],pch['maplen'],pch['last']))
        if pch['maplen'] or pch['sc']>=48: break
        if pch['base']==cur: break
        cur=pch['base']; depth+=1
        if depth>4: break
