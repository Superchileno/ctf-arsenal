import base64, string
ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
print('--- xor 0x20 ---')
print(''.join(chr(c^0x20) for c in ct))
print('--- xor 0x60 ---')
print(''.join(chr(c^0x60) for c in ct))
b64a = set((string.ascii_uppercase+string.ascii_lowercase+string.digits+'+/=').encode())
print('--- single xor keys landing in base64 alphabet ---')
for k in range(256):
    p = bytes(c^k for c in ct)
    if set(p) <= b64a:
        print('xor', hex(k), p)
print('--- single add keys landing in base64 alphabet ---')
for k in range(256):
    p = bytes((c+k)&0xFF for c in ct)
    if set(p) <= b64a:
        print('add', k, p)
print('--- single sub keys ---')
for k in range(256):
    p = bytes((c-k)&0xFF for c in ct)
    if set(p) <= b64a:
        print('sub', k, p)
