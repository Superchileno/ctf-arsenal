#!/usr/bin/env python3
"""
Desafío 06 - El baño VIP (El_Bano_VIP_Jugador)
La máquina de tickets imprime "rayas y puntos" (aparente Morse) pero en realidad
emite un flujo binario:

  - cada token tiene 5 caracteres: '-----' (sin punto) o '.----' (con un punto)
  - 8 tokens por línea = 8 bits = 1 byte, MSB primero
  - 72 líneas = 72 bytes -> texto ASCII en Base64
  - Base64 -> flag

Convención verificada: '.' = 1, '-' = 0.  (La convención opuesta da 72 x 0xFF.)
"""
import base64
import re

RUTA = "work/ticket_0347.txt"


def bits_desde_ticket(ruta: str) -> str:
    bits = []
    for linea in open(ruta, encoding="utf-8"):
        tokens = linea.split()
        if not tokens:
            continue
        if len(tokens) != 8:
            raise SystemExit(f"línea con {len(tokens)} tokens (se esperaban 8): {linea!r}")
        bits.extend("1" if "." in t else "0" for t in tokens)
    return "".join(bits)


def main() -> None:
    bits = bits_desde_ticket(RUTA)
    print(f"[i] {len(bits)} bits = {len(bits)//8} bytes")
    datos = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
    print(f"[i] ASCII: {datos.decode('ascii')}")
    plano = base64.b64decode(datos)
    print(f"[i] Base64 decodificado: {plano.decode()}")
    m = re.search(rb"TRAMACTF\{[^}]*\}", plano)
    print(f"[+] FLAG: {m.group(0).decode()}" if m else "[-] no se encontró flag")


if __name__ == "__main__":
    main()
