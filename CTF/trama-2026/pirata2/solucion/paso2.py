#!/usr/bin/env python3
"""
Pirata 2 — segunda pasada: el texto blanco de la cabecera resultó ser un señuelo.
Busca lo que queda «fuera de la vista»:
  * datos anexados después del EOCD del ZIP;
  * partes OOXML no evidentes (settings, webSettings, app.xml, theme...);
  * texto oculto por estilo/vanish;
  * cadenas base64 o hex largas;
  * metadatos y comentarios.
"""
import re
import zipfile
from pathlib import Path

DOCX = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/pirata2/work/acta_henry_every.docx")
datos = DOCX.read_bytes()
print(f"tamaño docx: {len(datos)}")

# --- 1. datos después del EOCD --------------------------------------------
i = datos.rfind(b"PK\x05\x06")
if i >= 0:
    eocd_len = 22 + int.from_bytes(datos[i+20:i+22], "little")
    cola = datos[i+eocd_len:]
    print(f"EOCD en {i}, fin del zip en {i+eocd_len}, cola: {len(cola)} bytes")
    if cola:
        print("  cola (repr):", cola[:200])

# --- 2. revisar cada parte -------------------------------------------------
with zipfile.ZipFile(DOCX) as z:
    print("\npartes:")
    for info in z.infolist():
        print(f"  {info.filename:40s} {info.file_size:7d} comp={info.compress_size:6d} "
              f"crc={info.CRC:08x}")
    print()
    for info in z.infolist():
        if not info.filename.endswith((".xml", ".rels")):
            continue
        x = z.read(info.filename).decode("utf-8", "replace")
        hallazgos = []
        if re.search(r"w:vanish", x):
            hallazgos.append("vanish")
        if re.search(r'w:color w:val="FFFFFF"', x):
            hallazgos.append("color blanco")
        if re.search(r'w:sz w:val="(1|2|4)"', x):
            hallazgos.append("tamaño diminuto")
        if re.search(r"<!--", x):
            hallazgos.append("comentario XML")
        if re.search(r"(?i)(flag|tramactf|plus|coord|lat|lon|rumbo)", x):
            hallazgos.append("palabra clave")
        for m in re.finditer(r"[A-Za-z0-9+/]{24,}={0,2}", x):
            s = m.group(0)
            if len(s) % 4 == 0 and re.search(r"[A-Z]", s) and re.search(r"[a-z]", s):
                hallazgos.append(f"posible b64: {s[:60]}")
        if hallazgos:
            print(f"{info.filename}: {hallazgos}")

# --- 3. texto visible de document.xml con colores usados -------------------
with zipfile.ZipFile(DOCX) as z:
    x = z.read("word/document.xml").decode("utf-8", "replace")
print("\ncolores en document.xml:", sorted(set(re.findall(r'w:color w:val="([0-9A-Fa-f]{6})"', x))))
print("tamaños:", sorted(set(re.findall(r'<w:sz w:val="(\d+)"', x)), key=int))
print("rStyle:", sorted(set(re.findall(r'<w:rStyle w:val="([^"]+)"', x))))
print("\napp.xml:")
print(z.read("docProps/app.xml").decode("utf-8", "replace")[:800] if False else "")
