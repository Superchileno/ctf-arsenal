#!/usr/bin/env python3
"""
Pirata 1 — barrido de bits (LSB / LSB-first / 2 bits / diferencias).
Busca texto legible o el patrón TRAMACTF en muchas combinaciones.
"""
import re
import wave
from pathlib import Path

import numpy as np

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
with wave.open(str(W / "senal_malapata.wav")) as w:
    x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.int32)

def a_bytes(bits: np.ndarray, lsb_first: bool) -> bytes:
    n = len(bits) - len(bits) % 8
    b = bits[:n].reshape(-1, 8)
    if lsb_first:
        b = b[:, ::-1]
    pesos = (1 << np.arange(7, -1, -1)).astype(np.uint32)
    return (b.astype(np.uint32) * pesos).sum(axis=1).astype(np.uint8).tobytes()

fuentes = {
    "sample>>0": (x >> 0) & 1,
    "sample>>1": (x >> 1) & 1,
    "sample>>2": (x >> 2) & 1,
    "sample>>3": (x >> 3) & 1,
    "abs>1": (np.abs(x) >> 1) & 1,
    "diff>>1": (np.abs(np.diff(x)) >> 1) & 1,
    "signo+bit1": ((x < 0).astype(np.int32) ^ ((np.abs(x) >> 1) & 1)),
}

mejores = []
for nombre, bits in fuentes.items():
    for lsb_first in (False, True):
        for off in range(8):
            b = a_bytes(bits[off:], lsb_first)
            if b"TRAMACTF" in b:
                print(f"*** FLAG en {nombre} lsb_first={lsb_first} off={off}")
            ratio = sum(32 <= c < 127 for c in b[:20000]) / 20000
            if ratio > 0.85 and len(set(b[:500])) > 25:
                mejores.append((ratio, nombre, lsb_first, off, b[:120]))
mejores.sort(reverse=True)
for r, n, lf, off, muestra in mejores[:6]:
    print(f"{r:.2%} {n} lsb_first={lf} off={off}: {muestra!r}")

# --- 2 bits por muestra (base4 -> ASCII) --------------------------------
for fuente, arr in (("bit0-1", (x & 3)), ("bit1-2", ((x >> 1) & 3))):
    v = arr.astype(np.uint8)
    for inicio in range(4):
        # 4 símbolos por byte? probamos empaquetar 4 valores de 2 bits
        n = (len(v) - inicio) // 4 * 4
        q = v[inicio:inicio+n].reshape(-1, 4)
        by = (q[:, 0] << 6 | q[:, 1] << 4 | q[:, 2] << 2 | q[:, 3]).astype(np.uint8).tobytes()
        ratio = sum(32 <= c < 127 for c in by[:20000]) / 20000
        if ratio > 0.8:
            print(f"2bits {fuente} inicio={inicio}: {ratio:.1%} {by[:100]!r}")

print("fin")
