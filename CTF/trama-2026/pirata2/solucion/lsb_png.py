#!/usr/bin/env python3
"""
Pirata 2 — segunda oportunidad: el banner del DOCX puede llevar el mismo
contenedor `DGLD` + zlib que el WAV de Pirata 1 (el LSB no se veía como texto).
Prueba todos los planos de bits/canales y offsets.
"""
import struct
import zlib
from pathlib import Path

import numpy as np
from PIL import Image

PNG = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/docx/word/media/image1.png")
img = Image.open(PNG)
modos = [("RGB", img.convert("RGB")), ("RGBA", img.convert("RGBA")), ("L", img.convert("L"))]

for nombre_modo, im in modos:
    arr = np.array(im)
    canales = arr.reshape(-1, arr.shape[2]) if arr.ndim == 3 else arr.reshape(-1, 1)
    for c in range(canales.shape[1]):
        col = canales[:, c]
        for bit in range(4):
            bits = ((col >> bit) & 1).astype(np.uint8)
            for invertir in (False, True):
                b0 = bits[::-1] if invertir else bits
                n = len(b0) // 8 * 8
                datos = (b0[:n].reshape(-1, 8) * (1 << np.arange(7, -1, -1))).sum(axis=1).astype(np.uint8).tobytes()
                if b"DGLD" in datos or datos[:4] == b"PK\x03\x04" or datos[:2] == b"\x78\x9c" or datos[:2] == b"\x78\xda":
                    print(f"*** {nombre_modo} canal {c} bit {bit} inv={invertir}: {datos[:16]!r}")
                    print("   ", datos[:120])
                # probar zlib a distintos offsets
                for off in range(8):
                    try:
                        d = zlib.decompress(datos[off:off+4000])
                        if b"TRAMACTF" in d or b"DGLD" in d:
                            print(f"*** zlib en {nombre_modo} c{c} bit{bit} inv={invertir} off={off}: {d[:200]!r}")
                    except Exception:
                        pass
print("fin")
