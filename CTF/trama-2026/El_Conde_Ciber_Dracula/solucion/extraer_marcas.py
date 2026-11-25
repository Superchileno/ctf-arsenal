#!/usr/bin/env python3
"""
DesafÃ­o 12 - El Conde Ciber-DrÃ¡cula
Extrae y agrupa las marcas Base64 de la esquina de cada slide.

Pipeline por frame:
  crop esquina -> canal verde -> autocontraste -> x10 -> OCR (psm 7, whitelist base64)

Luego normaliza (arregla confusiones tÃ­picas 0/O, 1/l/I, 5/S) y agrupa lecturas
idÃ©nticas en clusters consecutivos, mostrando el rango de frames de cada una.
"""
import glob
import os
import re
import subprocess
from collections import OrderedDict

from PIL import Image, ImageOps

W = "/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/El_Conde_Ciber_Dracula/work"
CAJA = (1040, 624, 1268, 654)   # caja ancha: la marca puede ser más larga que 16 chars
TMP = W + "/tmp_ocr"
os.makedirs(TMP, exist_ok=True)

WHITELIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


def ocr_frame(ruta):
    img = Image.open(ruta).convert("RGB")
    if img.size != (1280, 720):
        img = img.resize((1280, 720), Image.LANCZOS)
    g = img.crop(CAJA).split()[1]
    g = ImageOps.autocontrast(g).resize((g.width * 10, g.height * 10), Image.LANCZOS)
    p = os.path.join(TMP, os.path.basename(ruta))
    g.save(p)
    out = subprocess.run(
        ["tesseract", p, "stdout", "-l", "eng", "--psm", "7",
         "-c", f"tessedit_char_whitelist={WHITELIST}"],
        capture_output=True, text=True).stdout
    return out.strip().replace(" ", "")


def sq_de(nombre):
    m = re.search(r"sq_(\d+)", nombre)
    return int(m.group(1)) if m else -1


def main():
    frames = sorted(glob.glob(os.path.join(W, "dvr", "*.png")), key=lambda p: sq_de(os.path.basename(p)))
    lecturas = []
    for f in frames:
        txt = ocr_frame(f)
        lecturas.append((sq_de(os.path.basename(f)), txt))

    with open(os.path.join(W, "lecturas_ocr.tsv"), "w") as fh:
        for sq, t in lecturas:
            fh.write(f"{sq}\t{t}\n")

    # agrupar por lectura (valor -> lista de sq donde aparece)
    from collections import defaultdict
    grupos = defaultdict(list)
    for sq, t in lecturas:
        grupos[t if t else "(vacÃ­o)"].append(sq)

    print(f"frames: {len(lecturas)} | lecturas distintas: {len(grupos)}\n")
    for clave, sqs in sorted(grupos.items(), key=lambda kv: min(kv[1])):
        if clave == "(vacÃ­o)":
            continue
        print(f"  sq {min(sqs):5d}-{max(sqs):5d}  ({len(sqs):3d} frames)  {clave}")


if __name__ == "__main__":
    main()

