#!/usr/bin/env python3
"""Pirata 2 — «El tesoro existe, la boleta no» (DG-004).

Un .docx es un ZIP: el cuerpo está en word/document.xml, pero las cabeceras y
pies viven en word/header1.xml y word/footer1.xml. Aquí el texto relevante está
en runs con color FFFFFF (blanco sobre blanco), invisible en la lectura normal.

Uso: python3 extraer_texto_oculto.py [work/acta_henry_every.docx]
"""
import pathlib
import re
import sys
import zipfile

DOCX = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "work/acta_henry_every.docx")
PARTES = ["word/header1.xml", "word/footer1.xml", "word/document.xml"]

RUN_RE = re.compile(r"<w:r\b.*?</w:r>", re.S)
TEXTO_RE = re.compile(r"<w:t[^>]*>([^<]*)</w:t>")
COLOR_RE = re.compile(r'<w:color[^>]*w:val="([0-9A-Fa-f]{6})"')


def runs_ocultos(xml: str):
    """Devuelve (texto, color) de cada run, marcando los de color blanco."""
    for run in RUN_RE.findall(xml):
        texto = "".join(TEXTO_RE.findall(run))
        if not texto.strip():
            continue
        m = COLOR_RE.search(run)
        color = m.group(1).upper() if m else None
        yield texto, color


def main():
    z = zipfile.ZipFile(DOCX)
    print("partes:", ", ".join(z.namelist()))

    for parte in PARTES:
        if parte not in z.namelist():
            continue
        xml = z.read(parte).decode("utf-8", errors="replace")
        print(f"\n== {parte} ==")
        for texto, color in runs_ocultos(xml):
            marca = "  <-- OCULTO (blanco)" if color == "FFFFFF" else ""
            print(f"  [{color or 'herencia'}] {texto}{marca}")

    # Extracción directa de la flag y del dato de navegación
    for parte in PARTES:
        if parte not in z.namelist():
            continue
        xml = z.read(parte).decode("utf-8", errors="replace")
        for texto, color in runs_ocultos(xml):
            if color != "FFFFFF":
                continue
            if re.fullmatch(r"TRAMACTF\{[^}]+\}", texto.strip()):
                print(f"\nFLAG ({parte}): {texto.strip()}")
            elif re.fullmatch(r"\d+\.\d+", texto.strip()):
                print(f"DATO DE NAVEGACIÓN ({parte}): {texto.strip()}")


if __name__ == "__main__":
    main()
