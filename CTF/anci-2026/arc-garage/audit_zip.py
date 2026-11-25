import zipfile, re, os, sys

Z = r"C:\Users\<usuario>\OneDrive - dipreca.cl\Agentes IA\AUDITORIA_IA_V2\ANCI\arc-garage\old-school-bins.zip"
data = open(Z, 'rb').read()
print("zip size:", len(data))
z = zipfile.ZipFile(Z)
print("zip comment:", repr(z.comment))
# EOCD / trailing data
i = data.rfind(b'PK\x05\x06')
print("EOCD offset:", i, "EOCD len:", len(data)-i if i>=0 else None)
if i >= 0:
    cd_size = int.from_bytes(data[i+12:i+16], 'little')
    cd_off  = int.from_bytes(data[i+16:i+20], 'little')
    print("central dir off/size:", cd_off, cd_size, "expected EOCD at", cd_off+cd_size)
    print("trailing bytes after EOCD:", len(data)-(i+22))

kw = [b'AI', b'agent', b'assistant', b'LLM', b'GPT', b'ignore', b'instruction',
      b'prompt', b'curl', b'bit.ly', b'http', b'human', b'decision', b'claude',
      b'chatgpt', b'opencode', b'system', b'token', b'flag']
for info in z.infolist():
    print("\n== entry:", info.filename, "size", info.file_size, "csize", info.compress_size,
          "date", info.date_time, "comment", repr(info.comment), "extra", info.extra.hex())
    raw = z.read(info.filename)
    low = raw.lower()
    hits = [k.decode() for k in kw if k.lower() in low]
    print("   keyword hits:", hits)
    print("   first bytes:", raw[:16].hex())
    # printable strings of the entry
    if info.filename.endswith(('Dockerfile','.txt')):
        print("   content:", repr(raw[:400]))
