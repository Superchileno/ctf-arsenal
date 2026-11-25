import numpy as np, hashlib
from scipy.io import wavfile

rate, x = wavfile.read("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/ChismeAudio.wav")
x = np.asarray(x).astype(np.int32)

regions = {"intro": (0, int(0.569*rate)), "cuerpo": (int(0.569*rate), int(4.609*rate)),
           "cola": (int(4.609*rate), len(x))}

def bits_from(arr, bit, msb=True):
    b = ((arr >> bit) & 1).astype(np.uint8)
    return b

def to_bytes(b, msb=True):
    n = len(b)//8*8
    b = b[:n].reshape(-1,8)
    if msb:
        w = (b << np.arange(7,-1,-1)).sum(axis=1)
    else:
        w = (b << np.arange(0,8)).sum(axis=1)
    return bytes(w.astype(np.uint8))

def printable(bs):
    return sum(1 for c in bs if 32 <= c < 127)/max(1,len(bs))

key = b"SweetBlood"
ks = hashlib.sha256(key).digest()
def xor_rep(bs, k):
    return bytes(c ^ k[i % len(k)] for i, c in enumerate(bs))

found = False
for rname,(a,b) in regions.items():
    for bit in range(4):
        bits = bits_from(x[a:b], bit)
        for msb in (True, False):
            data = to_bytes(bits, msb)
            for label, d in (("raw", data), ("xor", xor_rep(data, ks))):
                p = printable(d[:400])
                hit = any(t in d for t in (b"TRAMA", b"PK\x03\x04", b"flag", b"FLAG", b"{TRAMA"))
                if hit or p > 0.85:
                    print(f"*** {rname} bit{bit} msb={msb} {label}: printable={p:.2f} hit={hit}")
                    print("   ", d[:120])
                    found = True
print("hallazgos:", found)

# entropia de la secuencia de LSB por region (para detectar datos)
for rname,(a,b) in regions.items():
    for bit in range(3):
        bts = ((x[a:b] >> bit) & 1)
        p1 = bts.mean()
        trans = np.abs(np.diff(bts)).sum()/len(bts)
        print(f"{rname} bit{bit}: p1={p1:.4f} trans={trans:.4f}")
