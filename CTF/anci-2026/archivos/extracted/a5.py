import base64, collections
ct = base64.b64decode(open('postcard.txt').read().splitlines()[-1].strip())
print(sorted(set(ct)))
print(len(set(ct)))
# differences between consecutive
print([ct[i+1]-ct[i] for i in range(30)])
# try: values mod patterns
for m in (2,4,8,16,32,64):
    print('mod',m, collections.Counter(v%m for v in ct).most_common())
# bit plane visual
for b in range(7,-1,-1):
    s=''.join('#' if (v>>b)&1 else '.' for v in ct[:108])
    print(b, s)
