#!/usr/bin/env python3
"""
Desafío 07 - Magma (postal de cinco lucas)
La "postal" es una textura de magma repetida en mosaico horizontal (periodo 164 px).
El mensaje no está en la superficie ni en los metadatos: está en las DIFERENCIAS
entre mosaicos, es decir, en lo que se "sale" del patrón repetido.

Pasos:
  1. detectar el periodo horizontal por autocorrelación (min |img - img desplazada|)
  2. restar la imagen desplazada una vez el periodo  -> mask de diferencias
  3. el texto aparece en dos bandas de filas; se recortan y amplían
  4. leer las líneas en orden y concatenarlas sin espacios

Uso: python3 revelar_magma.py [ruta_png]
"""
import sys

import numpy as np
from PIL import Image

BASE = "/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/Magma"
RUTA = sys.argv[1] if len(sys.argv) > 1 else BASE + "/work/placa_magma.png"


def detectar_periodo(gris, dmax=600):
    """Periodo horizontal d que minimiza la diferencia media con su desplazamiento."""
    score = [(np.abs(gris[:, :-d] - gris[:, d:]).mean(), d) for d in range(1, dmax)]
    return min(score)[1]


def main():
    a = np.array(Image.open(RUTA).convert("RGB")).astype(np.int16)
    H, W, _ = a.shape
    print(f"[i] imagen {W}x{H}")

    d = detectar_periodo(a.mean(axis=2))
    print(f"[i] periodo del mosaico: {d} px -> {W / d:.1f} repeticiones horizontales")

    dif = np.abs(a[:, d:, :] - a[:, :-d, :]).sum(axis=2)
    mask = (dif > 0).astype(np.uint8) * 255
    print(f"[i] píxeles fuera del patrón: {int((dif > 0).sum())}")
    Image.fromarray(mask).save(BASE + "/work/diff_mask.png")

    # bandas de texto: filas con muchas diferencias
    filas = np.where((dif > 0).sum(axis=1) > 50)[0]
    bandas = []
    inicio = anterior = filas[0]
    for f in filas[1:]:
        if f - anterior > 20:
            bandas.append((inicio, anterior))
            inicio = f
        anterior = f
    bandas.append((inicio, anterior))
    print(f"[i] bandas de texto detectadas: {bandas}")

    for i, (y0, y1) in enumerate(bandas, 1):
        # recortar la banda y ampliar x2 para lectura cómoda
        sub = mask[max(0, y0 - 10):y1 + 10, :]
        cols = np.where(sub.sum(axis=0) > 0)[0]
        sub = sub[:, max(0, cols.min() - 10):cols.max() + 10]
        img = Image.fromarray(sub).resize((sub.shape[1] * 2, sub.shape[0] * 2), Image.LANCZOS)
        img.save(BASE + f"/work/linea{i}.png")
        print(f"[+] línea {i}: filas {y0}-{y1} -> work/linea{i}.png")


if __name__ == "__main__":
    main()
