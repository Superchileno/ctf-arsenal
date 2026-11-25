#!/usr/bin/env python3
"""Resuelve «El Cielo Falsificado» (ruta_espectral).

El binario solo acepta un vector de 36 bytes que satisface, para cada i en 0..35,
una condición ofuscada (rotaciones, tablas y magia de división del compilador).
Como (7*i) mod 36 recorre los 36 índices sin repetir, cada byte del vector se
puede resolver de forma independiente probando los 256 valores.

Tablas en .rodata (offset de fichero == vaddr porque .rodata está en 0x2000):
  0x2140  T3  36 B  (comparación final, inalcanzable: el checksum siempre falla)
  0x2180  TB  32 B  (tabla de mezcla)
  0x21a0  TA  36 B  (tabla de mezcla)
La clave "CANAL47" se construye en la pila con dos dword inmediatos.

Uso: python resolver_vector.py [ruta_al_binario]
"""
import pathlib
import sys

BIN = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "ruta_espectral")
data = BIN.read_bytes()

T3 = data[0x2140:0x2140 + 36]
TB = data[0x2180:0x2180 + 32]
TA = data[0x21A0:0x21A0 + 36]
KEY = b"CANAL47"

M = (1 << 64) - 1
M1 = 0xE38E38E38E38E38F  # división por 36 (índice de entrada)
M2 = 0x2492492492492493  # división por 7  (índice de clave)
M3 = 0xAAAAAAAAAAAAAAAB  # rotación 1
M4 = 0xCCCCCCCCCCCCCCCD  # rotación 2


def mulhi(a, b):
    return ((a * b) >> 64) & M


def rol8(v, n):
    n &= 7
    return (((v << n) | (v >> (8 - n))) & 0xFF) if n else v & 0xFF


def idx_in(i):
    hi = mulhi(7 * i, M1) >> 5
    return (7 * i - 36 * hi) % 36


def idx_key(i):
    hi = mulhi(i, M2)
    rdx = (hi + ((i - hi) >> 1)) >> 2
    return (i - 7 * rdx) % 7


def rot1(i):
    hi = mulhi(i, M3)
    rdx = (hi & ~1) + (hi >> 1)
    return (i - rdx + 1) & 7


def rot2(i):
    hi = mulhi(i, M4)
    rdx = (hi & ~3) + (hi >> 2)
    return (i - rdx + 1) & 7


def cond(i, b):
    s = (b ^ KEY[idx_key(i)])
    s = (s + i) & 0xFF
    s = rol8(s, rot1(i))
    s ^= ((0x41 + 0x13 * i) ^ TA[i]) & 0xFF
    s ^= rol8(TB[(7 + 5 * i) & 31] ^ TB[(3 + 9 * i) & 31] ^ ((0x3D * i) & 0xFF), rot2(i))
    s ^= 0xA7
    return s


def checksum_tb():
    """r9b = 0x52 XOR rol(TB[j], j%7+1); el éxito exige 0x24 (siempre falla)."""
    chk = 0x52
    for j in range(32):
        chk ^= rol8(TB[j], (j % 7) + 1)
    return chk


def main():
    vector = bytearray(36)
    for i in range(36):
        sols = [b for b in range(256) if cond(i, b) == 0]
        if len(sols) != 1:
            raise SystemExit(f"i={i}: soluciones ambiguas {sols}")
        vector[idx_in(i)] = sols[0]

    print("vector hex :", vector.hex())
    print("vector     :", bytes(vector).decode())
    print("checksum TB:", hex(checksum_tb()), "(esperado 0x24; si difiere, la comparación con T3 no se ejecuta)")
    print("T3 (36 B)  :", T3.hex())


if __name__ == "__main__":
    main()
