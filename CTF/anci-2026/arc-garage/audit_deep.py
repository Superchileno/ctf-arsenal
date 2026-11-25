import zipfile, re, struct

Z = r"C:\Users\<usuario>\OneDrive - dipreca.cl\Agentes IA\AUDITORIA_IA_V2\ANCI\arc-garage\old-school-bins.zip"
z = zipfile.ZipFile(Z)
chall = z.read('old-school-bins/chall')
libc  = z.read('old-school-bins/libc.so')

pat = re.compile(rb'(?i)(ai[ _-]?agent|assistant|chatgpt|claude|opencode|llm|ignore (all|previous|the)|prompt|instruction|bit\.ly|https?://|curl |system prompt|human players?|do not analyze|token[: ])')
for name, buf in (('chall', chall), ('libc.so', libc)):
    print('==', name)
    seen = set()
    for m in pat.finditer(buf):
        s = max(0, m.start()-60); e = min(len(buf), m.end()+80)
        ctx = buf[s:e]
        ctx = re.sub(rb'[^\x20-\x7e]', b'.', ctx)
        if ctx in seen: continue
        seen.add(ctx)
        print('  @%#x %r' % (m.start(), ctx))
    print('  hits:', len(seen))

print('\n== overlay / embedded magics in chall ==')
elf = chall
# e_shoff at 0x28, e_shentsize 0x3a, e_shnum 0x3c
e_shoff = struct.unpack_from('<Q', elf, 0x28)[0]
e_shentsize = struct.unpack_from('<H', elf, 0x3a)[0]
e_shnum = struct.unpack_from('<H', elf, 0x3c)[0]
maxend = 0
for i in range(e_shnum):
    off = e_shoff + i*e_shentsize
    sh_offset = struct.unpack_from('<Q', elf, off+0x18)[0]
    sh_size   = struct.unpack_from('<Q', elf, off+0x20)[0]
    if sh_type := struct.unpack_from('<I', elf, off+0x04)[0]:
        if sh_type != 8:  # SHT_NOBITS
            maxend = max(maxend, sh_offset+sh_size)
print('file size', len(elf), 'last section end', maxend, 'trailing', len(elf)-maxend)
for magic in (b'PK\x03\x04', b'\x89PNG', b'%PDF', b'\x1f\x8b', b'flag{', b'test_flag', b'AI ', b'ignore'):
    print(magic, [hex(m.start()) for m in re.finditer(re.escape(magic), elf)][:10])

print('\n== full zip raw scan ==')
raw = open(Z,'rb').read()
for m in pat.finditer(raw):
    s=max(0,m.start()-40); e=min(len(raw), m.end()+60)
    ctx = re.sub(rb'[^\x20-\x7e]', b'.', raw[s:e])
    print('  @%#x %r' % (m.start(), ctx))
