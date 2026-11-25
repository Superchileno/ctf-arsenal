#!/usr/bin/env python3
"""
Desafío «El Chino se pierde en el Cajón del Maipo: Misión Fotito»
===============================================================

Notas de calibración del archivo `interceptacion.txt`:

  [1] «La ventisca dio vuelta el mensaje entero, de la última marca a la primera»
      -> invertir la cadena completa.
  [2] «Para abrirlo, usa solo la última palabra del destino como llave»
      -> destino = TERMAS DE COLINA  =>  clave = COLINA
  [3] «La llave se repite de principio a fin; solo avanzas al leer letras A-Z»
      -> cifrado de clave repetida; el índice de la clave SOLO avanza con A-Z.
  [4] «Números, espacios, puntos, llaves y guiones bajos no cambian»
      -> los caracteres no alfabéticos se copian tal cual.

Se prueban las dos interpretaciones habituales (XOR y Vigenère) y se muestra la
que produce el formato de flag.

Uso: python3 resolver.py [ruta_al_archivo]
"""
import sys
from pathlib import Path

CIFRADO = ("}0e0t_4pu_e0x_01mi5_0p1hp_t3{QHEAZICH .QITCQST NH VP GQMNLPIS "
           "SBV J SXEVV LWDAU .WECH AAC CCR SBUTIH")
CLAVE = "COLINA"


def invertir(s: str) -> str:
    return s[::-1]


def xor_clave(texto: str, clave: str) -> str:
    """XOR sobre letras A-Z; la clave avanza solo cuando se consume una letra."""
    salida = []
    k = 0
    for c in texto:
        if c.isalpha() and c.isascii():
            x = ord(c.upper()) ^ ord(clave[k % len(clave)])
            letra = chr(x)
            salida.append(letra.upper() if c.isupper() else letra.lower())
            k += 1
        else:
            salida.append(c)
    return "".join(salida)


def vigenere(texto: str, clave: str, signo: int = -1) -> str:
    salida = []
    k = 0
    for c in texto:
        if c.isascii() and c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            d = (ord(c) - base + signo * (ord(clave[k % len(clave)]) - ord("A"))) % 26
            salida.append(chr(base + d))
            k += 1
        else:
            salida.append(c)
    return "".join(salida)


def main() -> None:
    ruta = Path(sys.argv[1] if len(sys.argv) > 1 else "interceptacion.txt")
    if ruta.exists():
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            if "{" in linea and "}" in linea and linea.strip().startswith("}"):
                cifrado = linea.strip()
                break
        else:
            cifrado = CIFRADO
    else:
        cifrado = CIFRADO

    print("cifrado :", cifrado)
    volteado = invertir(cifrado)
    print("volteado:", volteado)
    print()

    candidatos = {
        "XOR + clave COLINA": xor_clave(volteado, CLAVE),
        "Vigenere (-)": vigenere(volteado, CLAVE, -1),
        "Vigenere (+)": vigenere(volteado, CLAVE, +1),
    }
    for nombre, texto in candidatos.items():
        print(f"{nombre:20s}: {texto}")
    print()
    for nombre, texto in candidatos.items():
        if "TRAMACTF" in texto.upper():
            print(f"[+] FLAG ({nombre}): {texto}")


if __name__ == "__main__":
    main()
