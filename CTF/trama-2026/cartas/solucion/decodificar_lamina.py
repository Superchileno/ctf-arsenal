#!/usr/bin/env python3
"""
Desafío 05 - Cartas: decodifica las láminas usando el catálogo de glifos.

Cada glifo representa una cifra hexadecimal; dos glifos por byte.
El catálogo auténtico (catalogo_glifos.txt) es el que valida el acta de subasta;
la reimpresión intercambia los valores de ▽ y ▲ (9 <-> 2) y solo sirve para el
folleto PROMO.
"""
import re
import sys

BASE = "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/cartas/work/"


def cargar_catalogo(path):
    mapa = {}
    for linea in open(path, encoding="utf-8"):
        m = re.match(r"^(.) \| ([0-9A-F])$", linea.rstrip("\n"))
        if m:
            mapa[m.group(1)] = m.group(2)
    return mapa


def decodificar(texto, mapa):
    glifos = [c for c in texto if c in mapa]
    hexstr = "".join(mapa[c] for c in glifos)
    if len(hexstr) % 2:
        hexstr = hexstr[:-1]
    return bytes.fromhex(hexstr)


def main():
    autentico = cargar_catalogo(BASE + "catalogo_glifos.txt")
    falso = cargar_catalogo(BASE + "catalogo_reimpresion.txt")
    print(f"[i] catálogo auténtico: {len(autentico)} glifos")
    difs = {k: (autentico[k], falso[k]) for k in autentico if autentico[k] != falso[k]}
    print(f"[i] diferencias glifos.txt vs reimpresion.txt: {difs}")

    for lamina in ("lamina_quintrala.txt", "lamina_promocional.txt"):
        texto = open(BASE + lamina, encoding="utf-8").read()
        print("\n" + "=" * 70)
        print(f"### {lamina}")
        for nombre, mapa in (("AUTÉNTICO", autentico), ("REIMPRESIÓN", falso)):
            try:
                plano = decodificar(texto, mapa)
                txt = plano.decode("utf-8", "replace")
            except ValueError as exc:
                txt = f"<error: {exc}>"
            print(f"--- con catálogo {nombre} ---")
            print(txt)
            if "TRAMA" in txt:
                print(">>> FLAG AQUÍ <<<")


if __name__ == "__main__":
    main()
