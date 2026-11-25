#!/usr/bin/env python3
"""
PagoAustral — «El bono fantasma»

mi_sesion.txt : 128 bytes (usuario=demo;rol=cliente;...)
mi_token.txt  : 128 bytes en hex  (256 caracteres)
token_gerencia: 128 bytes en hex

Hipótesis: el token va cifrado con la sesión como clave (XOR byte a byte).
Se prueban varias combinaciones y se muestra lo que sea imprimible.
"""
from pathlib import Path

W = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/austral/work")
sesion = W.joinpath("mi_sesion.txt").read_bytes()
t1 = bytes.fromhex(W.joinpath("mi_token.txt").read_text().strip())
t2 = bytes.fromhex(W.joinpath("token_gerencia.txt").read_text().strip())

print(f"sesion: {len(sesion)} bytes")
print(f"token1: {len(t1)} bytes   token2: {len(t2)} bytes")
print()

def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def mostrar(nombre: str, datos: bytes) -> None:
    imprimible = sum(32 <= b < 127 for b in datos)
    print(f"--- {nombre} (imprimibles {imprimible}/{len(datos)})")
    print("   hex :", datos.hex())
    print("   ascii:", "".join(chr(b) if 32 <= b < 127 else "." for b in datos))

mostrar("token1 XOR sesion", xor(t1, sesion))
mostrar("token2 XOR sesion", xor(t2, sesion))
mostrar("token1 XOR token2", xor(t1, t2))
