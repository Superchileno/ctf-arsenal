#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRAMA CTF 2026 -- Desafio: Documento Intervenido (MC-0421)
Recupera el payload oculto dentro de un DOCX.

Cadena de ocultamiento:
  1. documento .docx (OOXML = ZIP)
  2. customXml/item1.xml  ->  <cache encoding="base64">  (ZIP en base64)
  3. registro_0421.dat    ->  payload=<hex>
  4. hex  ->  texto de la flag

Uso:
    python3 extraer_intervenido.py [documento_intervenido_0421.docx]
"""
import base64
import io
import re
import sys
import zipfile
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "documento_intervenido_0421.docx"
CACHE_RE = re.compile(rb'<cache encoding="base64">([^<]+)</cache>')
PAYLOAD_RE = re.compile(rb"payload\s*=\s*([0-9A-Fa-f]+)")
FLAG_RE = re.compile(r"TRAMA(?:CTF)?\{[^}]+\}")


def main() -> int:
    docx = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not docx.is_file():
        print(f"[!] No existe: {docx}", file=sys.stderr)
        return 1

    print(f"[1] DOCX: {docx.name} ({docx.stat().st_size} B)")

    with zipfile.ZipFile(docx) as z:
        nombres = z.namelist()
        print(f"[2] partes OOXML: {len(nombres)}")
        if "customXml/item1.xml" not in nombres:
            print("[!] No hay customXml/item1.xml", file=sys.stderr)
            return 1
        item = z.read("customXml/item1.xml")

    m = CACHE_RE.search(item)
    if not m:
        print("[!] No se encontro <cache encoding=\"base64\">", file=sys.stderr)
        return 1
    interno = base64.b64decode(m.group(1))
    print(f"[3] cache base64 -> ZIP interno ({len(interno)} B)")

    with zipfile.ZipFile(io.BytesIO(interno)) as z2:
        print(f"    entradas: {z2.namelist()}")
        dat = z2.read(z2.namelist()[0])

    texto = dat.decode("utf-8", "replace")
    print("[4] registro_0421.dat:")
    for linea in texto.splitlines():
        if not linea.lower().startswith("payload="):
            print(f"    {linea}")
        else:
            print(f"    payload=<{len(linea) - 8} hex chars>")

    mp = PAYLOAD_RE.search(dat)
    if not mp:
        print("[!] No se encontro payload= en el .dat", file=sys.stderr)
        return 1
    secreto = bytes.fromhex(mp.group(1).decode()).decode("utf-8", "replace")
    print(f"[5] payload hex -> {secreto!r}")

    mf = FLAG_RE.search(secreto)
    if not mf:
        print("[!] La cadena decodificada no contiene una flag", file=sys.stderr)
        return 1

    print(f"\nFLAG: {mf.group(0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
