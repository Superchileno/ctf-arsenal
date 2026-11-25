#!/usr/bin/env python3
"""
Desafío 03 - Señal desde Blackwood (BW_SOC_3110)
Carvea el archivo ZIP anexado después del chunk IEND de un PNG.

Uso: python3 carve_trailer.py BW_SOC_3110.png
"""
import io
import sys
import zipfile

PNG_END_SIG = b"IEND"


def carve(img_path: str, out_zip: str = "embed.zip") -> bytes:
    data = open(img_path, "rb").read()

    # El chunk IEND son 12 bytes: longitud(4) + "IEND"(4) + CRC(4).
    # data.find(b"IEND") apunta al *tipo*, no al inicio del chunk.
    tipo = data.find(PNG_END_SIG)
    if tipo < 0:
        raise SystemExit("No se encontró el chunk IEND: no es un PNG válido")
    fin_png = tipo + 8            # fin del tipo (4) + CRC (4)
    extra = data[fin_png:]

    print(f"[i] PNG válido hasta el byte {fin_png}")
    print(f"[i] tamaño total {len(data)} -> {len(extra)} bytes anexados tras el IEND")

    firma = extra.find(b"PK\x03\x04")
    if firma < 0:
        raise SystemExit("[-] no hay firma ZIP en el trailer")
    print(f"[i] firma ZIP en offset {firma} del trailer")

    zip_bytes = extra[firma:]
    open(out_zip, "wb").write(zip_bytes)
    print(f"[+] guardado {out_zip} ({len(zip_bytes)} bytes)")

    zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    print("[+] contenido del ZIP:")
    for info in zf.infolist():
        print(f"    - {info.filename} ({info.file_size} bytes)")
        if info.file_size < 4096:
            print(f"      {zf.read(info.filename).decode('utf-8', 'replace')}")
    return zip_bytes


if __name__ == "__main__":
    carve(sys.argv[1] if len(sys.argv) > 1 else "BW_SOC_3110.png")
