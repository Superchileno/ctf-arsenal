#!/usr/bin/env python3
"""
Desafío 12 - El Conde Ciber-Drácula
Busca fragmentos Base64 en los frames OCR del stream (charla "El lado oscuro de la IA").

Uso:
  python3 buscar_fragmentos.py [directorio_ocr]

Heurística: tokens con pinta de Base64 (>= 12 chars, con mayúsculas/dígitos y
opcionalmente + / =), que no sean palabras en español.
"""
import glob
import os
import re
import sys

OCR = sys.argv[1] if len(sys.argv) > 1 else "ocr"

# palabras/etiquetas de la interfaz que NO son base64
RUIDO = {
    "clasifican", "preliminar", "clasificatoria", "actualizado", "equipos", "puntos",
    "cierre", "quedan", "horas", "posicion", "cambia", "ultima", "senal", "panorama",
    "trama", "vector", "fantasma", "numeros", "nodotrama", "youtube", "directo",
}

CANDIDATO = re.compile(r"\b[A-Za-z0-9+/]{10,}={0,2}\b")

def puntaje(tok: str) -> int:
    """Prioriza tokens con mezcla de mayúsculas, dígitos y símbolos base64."""
    s = 0
    if any(c.isupper() for c in tok):
        s += 2
    if any(c.isdigit() for c in tok):
        s += 2
    if any(c in "+/=" for c in tok):
        s += 3
    if len(tok) % 4 == 0:
        s += 1
    if tok.lower() in RUIDO:
        s -= 10
    return s

hallazgos = {}
for ruta in sorted(glob.glob(os.path.join(OCR, "*.txt"))):
    frame = os.path.basename(ruta)
    for linea in open(ruta, encoding="utf-8", errors="replace"):
        for tok in CANDIDATO.findall(linea):
            s = puntaje(tok)
            if s >= 4:
                hallazgos.setdefault(tok, set()).add(frame)

print(f"[i] frames OCR: {len(glob.glob(os.path.join(OCR, '*.txt')))}")
print(f"[i] candidatos con puntaje alto: {len(hallazgos)}\n")
for tok, frames in sorted(hallazgos.items(), key=lambda kv: -puntaje(kv[0])):
    fl = sorted(frames)
    print(f"  score={puntaje(tok):2d}  len={len(tok):3d}  {tok}")
    print(f"        frames: {fl[:4]}{' ...' if len(fl) > 4 else ''}")
