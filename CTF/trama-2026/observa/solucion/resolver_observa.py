#!/usr/bin/env python3
"""«Observa» — Expediente 01.

Cadena:
  1. Observa.zip está cifrado (ZipCrypto). La contraseña es `jhonny`
     (crackeada con rockyou; ver CONTEXTO.md).
  2. El DOCX interno (`por_aqui.docx`) tiene **los 4 primeros bytes dañados**
     (`50 15 78 04` en vez de `PK\\x03\\x04`), por eso "no se abre".
  3. Reparada la firma, el texto visible está en blanco (`w:color FFFFFF`):
     «La bandera es TRAMACTF{...}».

Uso: python3 resolver_observa.py [ruta_Observa.zip] [password]
"""
import io
import pathlib
import re
import sys
import zipfile

ZIP = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "../Observa.zip")
PWD = (sys.argv[2] if len(sys.argv) > 2 else "jhonny").encode()
OUT = pathlib.Path("work")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(ZIP)
    print("[1] entradas:", z.namelist())

    docx = bytearray(z.read("por_aqui.docx", pwd=PWD))
    (OUT / "por_aqui.docx").write_bytes(docx)
    print("[2] DOCX descifrado:", len(docx), "B; cabecera", docx[:8].hex())

    if docx[:4] != b"PK\x03\x04":
        print("    cabecera dañada -> reparando a PK\\x03\\x04")
        docx[0:4] = b"PK\x03\x04"
    (OUT / "por_aqui_reparado.docx").write_bytes(docx)

    doc = zipfile.ZipFile(io.BytesIO(bytes(docx)))
    xml = doc.read("word/document.xml").decode("utf-8", errors="replace")

    ocultos = []
    for run in re.findall(r"<w:r\b.*?</w:r>", xml, re.S):
        texto = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", run))
        color = re.search(r'<w:color[^>]*w:val="([0-9A-Fa-f]{6})"', run)
        if texto.strip() and color and color.group(1).upper() in ("FFFFFF",):
            ocultos.append(texto)

    print("[3] runs en blanco:", ocultos)
    for t in ocultos:
        m = re.search(r"TRAMACTF\{[^}]+\}", t)
        if m:
            print("[4] FLAG:", m.group(0))
            (OUT / "flag.txt").write_text(m.group(0) + "\n", encoding="ascii")
            return
    raise SystemExit("no se encontró la flag en runs blancos")


if __name__ == "__main__":
    main()
