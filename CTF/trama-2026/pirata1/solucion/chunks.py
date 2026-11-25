#!/usr/bin/env python3
"""Parsea la estructura RIFF del WAV y muestra todos los chunks."""
import struct
from pathlib import Path

P = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work/senal_malapata.wav")
d = P.read_bytes()
print(f"tamaño: {len(d)}")
assert d[:4] == b"RIFF"
print("RIFF size:", struct.unpack("<I", d[4:8])[0], "formato:", d[8:12])

pos = 12
while pos + 8 <= len(d):
    cid = d[pos:pos+4]
    size = struct.unpack("<I", d[pos+4:pos+8])[0]
    cuerpo = d[pos+8:pos+8+size]
    print(f"chunk {cid!r} size={size} pos={pos}")
    if cid != b"data":
        # mostrar subchunks si es LIST
        if cid == b"LIST":
            sub = cuerpo[4:]
            p2 = 0
            while p2 + 8 <= len(sub):
                sid = sub[p2:p2+4]
                ssz = struct.unpack("<I", sub[p2+4:p2+8])[0]
                print(f"    {sid!r} {ssz} {sub[p2+8:p2+8+ssz]!r}")
                p2 += 8 + ssz + (ssz & 1)
        else:
            print("   ", cuerpo[:200])
    pos += 8 + size + (size & 1)
print("fin en", pos, "sobrante:", len(d) - pos)
