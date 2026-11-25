import base64

raw = open('postcard.txt').read().splitlines()[-1].strip()
ct = base64.b64decode(raw)

# Capa 1: XOR con la fecha de la estampa (2026-03-14)
k1 = b'2026-03-14'
s1 = bytes(a ^ b for a, b in zip(ct, (k1 * (len(ct) // len(k1) + 2))[:len(ct)]))
print('[capa1] len =', len(ct), '| imprimibles =', sum(32 <= c < 127 or c == 10 for c in s1), '/', len(ct))

# Capa 2: Vigenere con la clave SIGNAL ("KEY REMNANT SIGNAL")
def vig(s, key):
    out, ki = [], 0
    for ch in s.decode('latin1'):
        if ch.isalpha():
            k = ord(key[ki % len(key)].lower()) - 97
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base - k) % 26 + base)); ki += 1
        else:
            out.append(ch)
    return ''.join(out)

texto = vig(s1, 'SIGNAL')
print('\n' + texto)
print('FLAG:', texto.split('token:')[1].split()[0])
