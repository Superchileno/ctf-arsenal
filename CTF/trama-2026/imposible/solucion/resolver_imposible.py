#!/usr/bin/env python3
"""Resolución de «El Archivo Imposible» (polyglot PNG+ZIP, 4 niveles).

Cadena:
  1. PNG con un ZIP anexado tras IEND (polyglot png+zip).
  2. nivel1.zip -> nivel2.gz
  3. gunzip -> texto ASCII85
  4. ASCII85 -> nivel3.zip (con flag.txt cifrado)
  5. La contraseña está en el chunk tEXt `clave_nivel4` = pr1sma_oculto
  6. flag.txt -> flag

Uso: python resolver_imposible.py [work/archivo_imposible.png]
"""
import base64
import gzip
import io
import pathlib
import re
import struct
import sys
import zipfile

PNG = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "work/archivo_imposible.png")
OUT = pathlib.Path("work")


def leer_text_chunks(data: bytes) -> dict:
    """Devuelve los tEXt del PNG (keyword -> valor)."""
    out = {}
    pos = 8
    while pos + 12 <= len(data):
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + ln]
        if typ == b"tEXt":
            k, _, v = body.partition(b"\x00")
            out[k.decode(errors="replace")] = v.decode(errors="replace")
        if typ == b"IEND":
            break
        pos += 12 + ln
    return out


def main():
    data = PNG.read_bytes()
    OUT.mkdir(parents=True, exist_ok=True)

    textos = leer_text_chunks(data)
    print("[1] tEXt:", textos)
    clave = textos.get("clave_nivel4", "pr1sma_oculto")

    off = data.find(b"PK\x03\x04")
    if off < 0:
        raise SystemExit("no hay ZIP anexado")
    print(f"[2] ZIP anexado tras IEND en {off:#x}; tamaño {len(data) - off} B")
    nivel1 = zipfile.ZipFile(io.BytesIO(data[off:]))
    print("    entradas:", nivel1.namelist())

    gz = nivel1.read("nivel2.gz")
    (OUT / "nivel2.gz").write_bytes(gz)
    texto85 = gzip.decompress(gz).strip()
    (OUT / "nivel2.out").write_bytes(texto85 + b"\n")
    print(f"[3] nivel2.gz -> {len(texto85)} bytes de texto ASCII85")

    nivel3_data = base64.a85decode(texto85, adobe=False, ignorechars=b" \t\n\r\v")
    (OUT / "nivel3.zip").write_bytes(nivel3_data)
    print(f"[4] ASCII85 -> ZIP de {len(nivel3_data)} B: {nivel3_data[:4]!r}")

    nivel3 = zipfile.ZipFile(io.BytesIO(nivel3_data))
    print("    entradas:", nivel3.namelist())
    flag = nivel3.read("flag.txt", pwd=clave.encode()).decode().strip()
    (OUT / "flag.txt").write_text(flag + "\n", encoding="ascii")
    print(f"[5] contraseña '{clave}' -> {flag}")

    assert re.fullmatch(r"TRAMACTF\{[^}]+\}", flag), "formato de flag inesperado"


if __name__ == "__main__":
    main()
