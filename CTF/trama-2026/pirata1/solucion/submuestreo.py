#!/usr/bin/env python3
"""
Pirata 1 — búsqueda de bits con submuestreo: ¿el mensaje va en el LSB de 1 de cada N muestras?
También prueba a leer la PCM como bytes de 8 bits (si fuera un WAV de 8 bits mal etiquetado).
"""
import re
import wave
from pathlib import Path

import numpy as np

W = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata1/work")
with wave.open(str(W / "senal_malapata.wav")) as w:
    x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.int32)

def empaquetar(bits: np.ndarray) -> bytes:
    n = len(bits) // 8 * 8
    b = bits[:n].reshape(-1, 8)
    pesos = (1 << np.arange(7, -1, -1)).astype(np.uint32)
    return (b.astype(np.uint32) * pesos).sum(axis=1).astype(np.uint8).tobytes()

def puntuar(b: bytes) -> float:
    m = min(len(b), 20000)
    return sum(32 <= c < 127 for c in b[:m]) / max(m, 1)

hallazgos = []
for N in list(range(2, 33)) + [40, 50, 64, 100, 128]:
    for bit in (0, 1):
        bits = ((x[::N] >> bit) & 1).astype(np.uint8)
        for lsb_first in (False, True):
            b = empaquetar(bits[::-1] if lsb_first else bits)
            if b"TRAMACTF" in b:
                print(f"*** FLAG: N={N} bit={bit} rev={lsb_first}")
            p = puntuar(b)
            if p > 0.9:
                hallazgos.append((p, N, bit, lsb_first, b[:80]))
hallazgos.sort(reverse=True)
for p, N, bit, rev, m in hallazgos[:5]:
    print(f"{p:.2%} N={N} bit={bit} rev={rev}: {m!r}")

# --- ¿PCM cruda como bytes de 8 bits? -----------------------------------
b = x.astype("<i2").tobytes()
bajo = b[0::2]
print("\nbytes pares (byte bajo) imprimibles:", f"{puntuar(bajo):.1%}",
      "| TRAMACTF:", bajo.find(b"TRAMACTF"))
print("primeros bytes pares:", bajo[:60])

# --- ¿texto al revés? ---------------------------------------------------
if b"FTACAMART" in bajo:
    print("texto invertido encontrado")
