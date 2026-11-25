#!/usr/bin/env python3
"""Resolución de «Memoria» (Archivo de los Ausentes, Expediente 02).

Cadena:
  1. registro_memoria.jpg es un JPEG con un ZIP anexado tras el EOI (FFD9).
  2. El ZIP contiene respaldo_0317.png, que es un código QR.
  3. El QR contiene ASCII en binario (grupos de 8 bits).
  4. El texto se envuelve con el formato oficial TRAMACTF{...}.

Uso: python3 resolver_memoria.py [work/registro_memoria.jpg]
Requiere `zbarimg` (zbar-tools) o, en su defecto, OpenCV con QRCodeDetector.
"""
import io
import pathlib
import shutil
import subprocess
import sys
import zipfile

JPG = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "work/registro_memoria.jpg")
OUT = pathlib.Path("work")


def leer_qr(png: pathlib.Path) -> str:
    if shutil.which("zbarimg"):
        out = subprocess.run(
            ["zbarimg", "-q", "--raw", str(png)], capture_output=True, check=True
        )
        return out.stdout.decode().strip()
    import cv2  # fallback

    img = cv2.imread(str(png))
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    return data.strip()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = JPG.read_bytes()

    off = data.find(b"PK\x03\x04")
    if off < 0:
        raise SystemExit("no hay ZIP anexado al JPEG")
    print(f"[1] ZIP anexado tras el EOI en {off:#x} ({len(data) - off} B)")
    z = zipfile.ZipFile(io.BytesIO(data[off:]))
    print("    entradas:", z.namelist())

    png = OUT / "respaldo_0317.png"
    png.write_bytes(z.read("respaldo_0317.png"))
    print(f"[2] imagen interna: {png.name}")

    qr = leer_qr(png)
    print(f"[3] QR: {qr}")
    texto = "".join(chr(int(g, 2)) for g in qr.split())
    flag = "TRAMACTF{" + texto + "}"
    (OUT / "flag.txt").write_text(flag + "\n", encoding="ascii")
    print(f"[4] {flag}")


if __name__ == "__main__":
    main()
