import wave, struct, sys, collections, re

p = "/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav"
raw = open(p, "rb").read()
print("size", len(raw))
print("header first 64:", raw[:64].hex())

# WAV chunk walk
i = 12
while i + 8 <= len(raw):
    cid = raw[i:i+4]
    sz = struct.unpack("<I", raw[i+4:i+8])[0]
    print("chunk", cid, "size", sz, "offset", i)
    i += 8 + sz + (sz & 1)

w = wave.open(p, "rb")
n = w.getnframes()
data = w.readframes(n)
print("frames", n, "rate", w.getframerate())

s = struct.unpack("<%dh" % n, data)
print("min", min(s), "max", max(s))
lsb0 = sum(1 for x in s if x & 1)
print("LSB=1 count", lsb0, "of", n, "ratio", lsb0/n)

# extraer LSB serial (bit = s[i]&1), agrupando en bytes MSB-first y LSB-first
bits = [x & 1 for x in s]
def tobytes(bits, msb=True):
    out = bytearray()
    for k in range(0, len(bits)-7, 8):
        b = 0
        for j in range(8):
            if msb:
                b = (b << 1) | bits[k+j]
            else:
                b |= bits[k+j] << j
        out.append(b)
    return bytes(out)

for name, bits_ in [("lsb", bits), ("neg-lsb", [1-(x&1) for x in s])]:
    for msb in (True, False):
        tb = tobytes(bits_, msb)
        printable = sum(1 for c in tb[:2000] if 32 <= c < 127)
        print(name, "msb" if msb else "lsbf", "printable/2000:", printable, "head:", tb[:32])

# buscar strings tipo bandera en todas las variantes
for name, bits_ in [("lsb", bits)]:
    for msb in (True, False):
        tb = tobytes(bits_, msb)
        for m in re.finditer(rb"TRAMA|PK\x03\x04|flag", tb):
            print("HIT", name, msb, m.start())
