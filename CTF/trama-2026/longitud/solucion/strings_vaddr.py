import struct, sys

p = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/longitud/longitud_heredada"
data = open(p, "rb").read()

# parse program headers para mapear vaddr -> offset
e_phoff = struct.unpack_from("<Q", data, 0x20)[0]
e_phentsize = struct.unpack_from("<H", data, 0x36)[0]
e_phnum = struct.unpack_from("<H", data, 0x38)[0]
segs = []
for i in range(e_phnum):
    off = e_phoff + i*e_phentsize
    p_type, p_flags = struct.unpack_from("<II", data, off)
    p_offset, p_vaddr, p_paddr, p_filesz = struct.unpack_from("<QQQQ", data, off+8)
    if p_type == 1:
        segs.append((p_vaddr, p_offset, p_filesz))

def read_vaddr(addr, n=64):
    for va, off, sz in segs:
        if va <= addr < va+sz:
            fo = off + (addr-va)
            return data[fo:fo+n].split(b"\x00")[0]
    return b"<?>"

for a in [0x47c010,0x47c01a,0x47c02d,0x47c038,0x47c04c,0x47c068,0x47c07d,
          0x47c091,0x47c099,0x47c0b7,0x47c0d3,0x47c130,0x47de61]:
    print(hex(a), read_vaddr(a, 80))
