import base64

raw = open('postcard.txt').read().split('\n')[2].strip()
ct = base64.b64decode(raw)

# capa 1: XOR con la fecha del sello (periodo 10)
date = b'2026-03-14'
mid = bytes(c ^ date[i % len(date)] for i, c in enumerate(ct))

# capa 2: Vigenere sobre letras, clave SIGNAL (de la etiqueta del sello)
k = 'signal'
i = 0
out = []
for ch in mid.decode('latin1'):
    if ch.isalpha():
        lower = ch.islower()
        v = (ord(ch.lower()) - 97 - (ord(k[i % len(k)]) - 97)) % 26
        c = chr(v + 97)
        out.append(c if lower else c.upper())
        i += 1
    else:
        out.append(ch)

print(''.join(out))
