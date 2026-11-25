#!/usr/bin/env python3
"""Descifra la 'orden' de pulso_mantenimiento (TEA-like, 32 rondas, clave derivada de ORION-03)."""
import struct

BIN = "/mnt/c/Users/shapl/AppData/Local/Temp/opencode/mantenimiento/pulso_mantenimiento"
data = open(BIN, "rb").read()

# .rodata: vaddr == offset
PTR_A = 0x205a   # "ORIO"
PTR_B = 0x205e   # "N-03"
CIPHER = 0x2120
CLEN = 0x28      # 40 bytes (5 bloques de 8)

def u32(off):
    return struct.unpack_from("<I", data, off)[0]

# --- clave: 4 palabras derivadas en el primer bucle de main ---
key = []
for i in range(4):
    src = PTR_A if (i & 1) == 0 else PTR_B
    w = u32(src)
    k = (w ^ (0x11111111 * i & 0xFFFFFFFF) ^ 0x65F2A4C0) & 0xFFFFFFFF
    key.append(k)
    print(f"key[{i}] = {k:08x}   (desde {data[src:src+4]!r})")

# --- descifrado identico al desensamblado ---
M = 0xFFFFFFFF
DELTA = 0x9E3779B9
MINUS_DELTA = (M + 1 - DELTA) & M     # 0x61c88647

def decrypt(v0, v1):
    s = 0xC6EF3720
    while True:
        e = s + key[(s >> 11) & 3]
        d = ((((v0 << 4) & M) ^ (v0 >> 5)) + v0) & M
        d ^= e
        v1 = (v1 - d) & M
        s = (s + MINUS_DELTA) & M
        e = s + key[s & 3]
        d = ((((v1 << 4) & M) ^ (v1 >> 5)) + v1) & M
        d ^= e
        v0 = (v0 - d) & M
        if s == 0:
            return v0, v1

out = b""
for i in range(0, CLEN, 8):
    c0, c1 = u32(CIPHER + i), u32(CIPHER + i + 4)
    v0, v1 = decrypt(c0, c1)
    out += struct.pack("<II", v0, v1)
print("\nbytes descifrados:", out)
txt = out.split(b"\x00")[0]
print("ORDEN:", txt.decode("latin1"))
open("/mnt/c/Users/shapl/AppData/Local/Temp/opencode/mantenimiento/orden.txt", "wb").write(txt + b"\n")
