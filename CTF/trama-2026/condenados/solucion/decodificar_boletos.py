#!/usr/bin/env python3
"""El reto «La Lotería de los Condenados».

Cada boleto es Base64 de un texto XOR con la clave repetida `nodo_trama_2026`
(la "marca de archivo" que el exsecretario usaba en todas las copias).
Solo uno de los diez mensajes decodifica a la flag; el resto son señuelos.

Uso: python decodificar_boletos.py [ruta_a_la_urna.txt]
"""
import base64
import pathlib
import re
import sys

URNA = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "work/la_urna.txt")
KEY = b"nodo_trama_2026"


def xor(data: bytes, key: bytes) -> bytes:
    return bytes(c ^ key[i % len(key)] for i, c in enumerate(data))


def main():
    texto = URNA.read_text(encoding="utf-8")
    mensajes = re.findall(r"Mensaje:\s*«([^»]+)»", texto)
    for n, msg in enumerate(mensajes, 1):
        claro = xor(base64.b64decode(msg), KEY).decode(errors="replace")
        marca = "  <-- FLAG" if "TRAMACTF{" in claro else ""
        print(f"Boleto {n:02d}: {claro}{marca}")


if __name__ == "__main__":
    main()
