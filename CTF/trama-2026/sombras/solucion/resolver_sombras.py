#!/usr/bin/env python3
"""Resolución de «La Hermandad de las Sombras» (fiesta-sombras-2026).

1) Descarga las imágenes del README del repo CondeCyberDracula/fiesta-sombras-2026.
2) Carvea el ZIP anexado tras el EOI del JPEG (firma PK\\x03\\x04).
3) Lee secreto.txt y aplica César -3 (validando el prefijo TRAMACTF{).

Uso: python resolver_sombras.py [directorio_de_trabajo]
"""
import io
import pathlib
import sys
import urllib.request
import zipfile

REPO = "CondeCyberDracula/fiesta-sombras-2026"
README = f"https://raw.githubusercontent.com/{REPO}/main/README.md"
IMG_PISTA = "https://github.com/user-attachments/assets/7889da77-03f1-4d85-8cd7-a04a5984ade8"


def caesar(text: str, shift: int) -> str:
    out = []
    for c in text:
        if c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            out.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            out.append(c)
    return "".join(out)


def main():
    work = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "work")
    work.mkdir(parents=True, exist_ok=True)

    print("[1] README:", README)
    urllib.request.urlretrieve(README, work / "README.md")

    print("[2] descargando imagen con la pista…")
    urllib.request.urlretrieve(IMG_PISTA, work / "Pista_Invitacion.png")
    data = (work / "Pista_Invitacion.png").read_bytes()

    off = data.find(b"PK\x03\x04")
    if off < 0:
        raise SystemExit("no se encontró ZIP anexado")
    print(f"    ZIP anexado en el offset {off:#x} ({off})")
    (work / "secreto.zip").write_bytes(data[off:])

    z = zipfile.ZipFile(io.BytesIO(data[off:]))
    cifrado = z.read("secreto.txt").decode()
    (work / "secreto.txt").write_text(cifrado + "\n", encoding="ascii")
    print("[3] secreto.txt:", cifrado.strip())

    for k in range(26):
        claro = caesar(cifrado, -k)
        if "TRAMACTF{" in claro:
            print(f"[4] César -{k}: {claro.strip()}")
            pathlib.Path("flag.txt").write_text(claro.strip() + "\n", encoding="ascii")
            return
    raise SystemExit("no se encontró desplazamiento válido")


if __name__ == "__main__":
    main()
