#!/usr/bin/env python3
"""Mira los primeros bytes de cada flujo LSB y prueba descompresión/codificaciones."""
import base64
import bz2
import gzip
import wave
import zlib
from pathlib import Path

import numpy as np

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
with wave.open(str(W / "senal_malapata.wav")) as w:
    x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.int32)

def empaq(bits):
    n = len(bits) // 8 * 8
    b = bits[:n].reshape(-1, 8)
    p = (1 << np.arange(7, -1, -1)).astype(np.uint32)
    return (b.astype(np.uint32) * p).sum(axis=1).astype(np.uint8).tobytes()

for bit in (0, 1, 2, 3):
    bits = ((x >> bit) & 1).astype(np.uint8)
    b = empaq(bits)
    print(f"--- bit {bit}: primeros 64 bytes: {b[:64]!r}")
    for f, nombre in ((zlib.decompress, "zlib"), (gzip.decompress, "gzip"),
                      (bz2.decompress, "bz2")):
        try:
            d = f(b)
            print(f"    {nombre}: {d[:80]!r}")
        except Exception:
            pass
    try:
        d = base64.b64decode(b[:4096], validate=True)
        print(f"    b64: {d[:60]!r}")
    except Exception:
        pass
    if b[:2] == b"PK":
        print("    ¡empieza con PK!")
