#!/usr/bin/env python3
"""
Desafío 04 - ataque alternativo SIN la tarjeta QSL.

Idea: el cifrador es, tras deshacer rotación y swap de nibbles, un XOR de clave
repetida.  Con un crib conocido ("Bitacora") se derivan los primeros bytes de la
clave; si la longitud probada L coincide con la real, el texto completo sale
imprimible.  No hace falta adivinar el indicativo.
"""
import sys
from descifrar import _r, _s

crib = b"Bitacora"

def inv_transform(c: bytes) -> bytes:
    return bytes(_r(_s(b), 8 - ((i % 7) + 1)) for i, b in enumerate(c))

def main(path: str) -> None:
    c = bytes.fromhex(open(path).read().strip())
    u = inv_transform(c)                      # u[i] = p[i] ^ k[i % L]
    for L in range(1, 17):
        if len(u) < L:
            break
        k = bytes(u[i] ^ crib[i] for i in range(L))
        p = bytes(u[i] ^ k[i % L] for i in range(len(u)))
        imprimibles = sum(1 for b in p if 32 <= b < 127) / len(p)
        if imprimibles > 0.98:
            print(f"[+] longitud de clave probable: {L}")
            print(f"[+] clave derivada: {k.decode('latin-1')!r}  ({k.hex()})")
            print(f"[+] texto plano ({imprimibles:.0%} imprimible):")
            print("-" * 60)
            print(p.decode("latin-1"))
            return
    print("[-] no se encontró longitud consistente con el crib")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "work/bitacora.cifrada")
