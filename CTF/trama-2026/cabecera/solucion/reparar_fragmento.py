#!/usr/bin/env python3
"""CABECERA PERDIDA // ÚLTIMA TRANSMISIÓN (nodo VF-0317).

El fragmento `fragmento_0317.bin` es un PNG de 1600×900 al que le falta el
primer byte de la firma: empieza por `00 50 4E 47 0D 0A 1A 0A` en lugar de
`89 50 4E 47 0D 0A 1A 0A`. El motor de recuperación lo clasificó como ilegible.

El script:
  1. Restaura el byte 0x89.
  2. Valida la estructura de chunks y los CRC de cada uno.
  3. Decodifica el volcado hexadecimal que la imagen muestra en el panel
     PAYLOAD // BLOQUE 03 (transcrito del PNG; ver CONTEXTO.md).

Uso: python3 reparar_fragmento.py [fragmento_0317.bin] [salida.png]
"""
import pathlib
import re
import struct
import sys
import zlib

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "../fragmento_0317.bin")
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "cabecera_restaurada.png")

# Volcado visible en la imagen (panel PAYLOAD // BLOQUE 03, offsets 0000..0028)
PAYLOAD_HEX = (
    "54 52 41 4D 41 43 54 46 7B 4C "
    "34 5F 53 33 4E 34 4C 5F 52 30 "
    "54 34 5F 43 30 4E 53 33 52 56 "
    "34 5F 53 55 5F 31 44 33 4E 54 "
    "31 44 34 44 5F 30 33 31 37 7D"
)


def reparar():
    data = bytearray(SRC.read_bytes())
    print("firma original :", data[:8].hex())
    if data[:8] == bytes.fromhex("89504e470d0a1a0a"):
        print("ya tenía la firma correcta")
    elif data[1:8] == bytes.fromhex("504e470d0a1a0a"):
        data[0] = 0x89
        print("firma reparada :", data[:8].hex())
    else:
        raise SystemExit("el daño no es solo el primer byte")
    OUT.write_bytes(data)
    print(f"guardado en {OUT} ({len(data)} B)")


def validar():
    b = OUT.read_bytes()
    assert b[:8] == bytes.fromhex("89504e470d0a1a0a")
    pos = 8
    ok = True
    while pos + 12 <= len(b):
        ln = struct.unpack(">I", b[pos:pos + 4])[0]
        typ = b[pos + 4:pos + 8]
        data = b[pos + 8:pos + 8 + ln]
        crc = struct.unpack(">I", b[pos + 8 + ln:pos + 12 + ln])[0]
        calc = zlib.crc32(typ + data) & 0xFFFFFFFF
        print(f"  {typ.decode(errors='replace'):4} len={ln:<6} crc={'OK' if crc == calc else 'MAL'}")
        ok &= crc == calc
        pos += 12 + ln
        if typ == b"IEND":
            break
    print("  datos tras IEND:", len(b) - pos, "| integridad:", ok)
    return ok


def main():
    reparar()
    if not validar():
        raise SystemExit("CRC inválido")
    claro = bytes.fromhex(PAYLOAD_HEX).decode("ascii")
    print("\npayload decodificado:", claro)
    m = re.search(r"TRAMACTF\{[^}]+\}", claro)
    print("FLAG:", m.group(0))


if __name__ == "__main__":
    main()
