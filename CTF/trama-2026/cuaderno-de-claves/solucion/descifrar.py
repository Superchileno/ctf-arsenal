#!/usr/bin/env python3
"""Desafío 04 - El Cuaderno de Claves: descifrado inverso del cifrador de El Viejo."""
import sys


def _r(b, n):
    return ((b << n) | (b >> (8 - n))) & 255


def _s(b):
    return ((b & 15) << 4) | ((b >> 4) & 15)


def encrypt(p: bytes, k: bytes) -> bytes:
    o = bytearray()
    for i, byte in enumerate(p):
        x = byte ^ k[i % len(k)]
        x = _r(x, (i % 7) + 1)
        x = _s(x)
        o.append(x)
    return bytes(o)


def decrypt(c: bytes, k: bytes) -> bytes:
    o = bytearray()
    for i, byte in enumerate(c):
        x = _s(byte)                    # swap de nibbles es su propia inversa
        x = _r(x, 8 - ((i % 7) + 1))    # rotar a la derecha = rotar izquierda 8-n
        x = x ^ k[i % len(k)]
        o.append(x)
    return bytes(o)


if __name__ == "__main__":
    clave = sys.argv[1] if len(sys.argv) > 1 else "CE2RCA"
    cifrado = bytes.fromhex(open(sys.argv[2] if len(sys.argv) > 2 else "bitacora.cifrada").read().strip())
    plano = decrypt(cifrado, clave.encode())
    print(f"[+] clave: {clave} | {len(plano)} bytes")
    print("-" * 60)
    print(plano.decode("utf-8", "replace"))
