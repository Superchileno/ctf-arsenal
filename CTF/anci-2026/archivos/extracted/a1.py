import base64, collections
s = open('postcard.txt').read().splitlines()[-1].strip()
d = base64.b64decode(s)
print('len', len(d))
print(d.hex())
print(repr(d[:120]))
c = collections.Counter(d)
print('distinct', len(c))
for k, v in c.most_common(15):
    print(hex(k), chr(k) if 32 <= k < 127 else '.', v)
