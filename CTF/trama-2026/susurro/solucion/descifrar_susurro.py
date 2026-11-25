#!/usr/bin/env python3
"""El Susurro del Conde — TRAMA CTF 2026.

Capas:
  1) El espectrograma (2,4-4,1 kHz) dibuja  KEY: SweetBlood  -> llave visual.
  2) El bit 0 de cada muestra PCM contiene, al inicio, una cadena Base64:
         ByUkKDUBOHZLNyNECRAaKQVeVzsWGVYJKw8JREJULg==
     que decodifica a 31 bytes. Al hacer XOR con la llave leet "SweetBl00d"
     (no "SweetBlood") aparece la flag.

Uso:  python3 descifrar_susurro.py [--wav ChismeAudio.wav]
"""

import argparse
import base64
import re
import struct
import wave
from pathlib import Path

KEY = b"SweetBl00d"
B64 = re.compile(rb"[A-Za-z0-9+/]{16,}={0,2}")


def extraer_lsb(ruta):
    with wave.open(str(ruta), "rb") as w:
        if w.getsampwidth() != 2 or w.getnchannels() != 1:
            raise SystemExit("Se espera WAV PCM 16-bit mono")
        n = w.getnframes()
        datos = w.readframes(n)
    muestras = struct.unpack("<%dh" % n, datos)
    bits = [(m & 1) for m in muestras]
    # empaquetar MSB-first
    salida = bytearray()
    for i in range(0, len(bits) - 7, 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bits[i + j]
        salida.append(b)
    return bytes(salida)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wav", default=str(Path(__file__).resolve().parents[1] / "ChismeAudio.wav"))
    args = ap.parse_args()

    flujo = extraer_lsb(args.wav)
    print(f"[1] LSB empaquetado: {len(flujo)} bytes; inicio: {flujo[:48]!r}")

    m = B64.search(flujo[:256])
    if not m:
        raise SystemExit("No se encontro el blob Base64 en el LSB")
    blob = m.group(0)
    print(f"[2] Blob Base64 ({len(blob)} chars): {blob.decode()}")

    ct = base64.b64decode(blob)
    print(f"[3] Ciphertext ({len(ct)} B): {ct.hex()}")

    pt = bytes(c ^ KEY[i % len(KEY)] for i, c in enumerate(ct))
    print(f"[4] XOR con {KEY.decode()!r}: {pt.decode(errors='replace')}")

    if not pt.startswith(b"TRAMACTF{"):
        raise SystemExit("La flag no empieza por TRAMACTF{; revisar la llave")
    print("\nFLAG:", pt.decode())


if __name__ == "__main__":
    main()
