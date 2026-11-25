#!/usr/bin/env python3
"""
Pirata 1 — el LSB de las muestras lleva un contenedor propio:

    'DGLD' | longitud (4 bytes, big endian) | zlib(deflate) ...

Aquí se extrae y se descomprime.
"""
import struct
import wave
import zlib
from pathlib import Path

import numpy as np

W = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
with wave.open(str(W / "senal_malapata.wav")) as w:
    x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.int32)

bits = ((x >> 0) & 1).astype(np.uint8)
n = len(bits) // 8 * 8
b = (bits[:n].reshape(-1, 8) * (1 << np.arange(7, -1, -1))).sum(axis=1).astype(np.uint8).tobytes()

print("magic:", b[:4], "| longitud declarada:", struct.unpack(">I", b[4:8])[0])
print("cabecera zlib en offset 8:", b[8:10].hex())

largo = struct.unpack(">I", b[4:8])[0]
cuerpo = b[8:8 + largo]
print("cuerpo:", len(cuerpo), "bytes, empieza:", cuerpo[:8].hex())

try:
    datos = zlib.decompress(cuerpo)
    print("\n=== DESCOMPRIMIDO ===")
    print(datos.decode(errors="replace"))
except Exception as e:
    print("zlib falló:", e)
    try:
        d = zlib.decompressobj()
        out = d.decompress(b[8:])
        print("parcial:", out[:2000])
    except Exception as e2:
        print("también falló:", e2)

# volcar el contenedor completo por si acaso
(W / "contenedor_lsb.bin").write_bytes(b)
print("\nvolcado el flujo LSB completo en work/contenedor_lsb.bin")
