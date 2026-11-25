#!/usr/bin/env python3
"""
PagoAustral — «El bono fantasma»

Idea: `mi_token.txt` es el cifrado de `mi_sesion.txt` (ambos de 128 bytes).
Es decir, tenemos un par conocido (texto plano, cifrado), lo que permite
recuperar el keystream y aplicarlo a `token_gerencia.txt`.

    keystream = C_mio XOR P_mio
    P_gerencia = C_gerencia XOR keystream
"""
from pathlib import Path

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/austral/work")
p1 = W.joinpath("mi_sesion.txt").read_bytes()
c1 = bytes.fromhex(W.joinpath("mi_token.txt").read_text().strip())
c2 = bytes.fromhex(W.joinpath("token_gerencia.txt").read_text().strip())

print("P1 (sesión):", p1.decode(errors="replace"))
keystream = bytes(a ^ b for a, b in zip(c1, p1))
p2 = bytes(a ^ b for a, b in zip(c2, keystream))

print("\nkeystream hex:", keystream.hex())
print("\nP2 (gerencia):")
print(p2.decode(errors="replace"))
print("\nP2 hex:", p2.hex())
