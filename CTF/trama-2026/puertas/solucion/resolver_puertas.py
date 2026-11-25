#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRAMA CTF 2026 - Las Veinte Puertas
Reconstruye la ronda nocturna valida y lee el mensaje del registro.

Reglas (protocolo_de_ronda.txt):
  * Entrada: puerta 01.
  * La ronda valida recorre 7 puertas contando la inicial.
  * Cada puerta tiene dos salidas: IZQ y DER (paso_izq / paso_der).
  * sello_siguiente = (3 * sello_actual + 7) mod 17
  * Solo una salida lleva a una puerta cuyo sello coincida con el esperado.
  * La ronda termina en la puerta con estado SALIDA.
  * Cada puerta visitada aporta una banda de 5 simbolos.
  * Las bandas se colocan como COLUMNAS en orden de visita y se leen por FILAS.
"""
from __future__ import annotations

import csv
import io
import sys
import zipfile
from pathlib import Path

ZIP = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "Veinte_Puertas.zip"
INICIO = 1
LARGO = 7
MOD = 17


def cargar(zpath: Path) -> dict[int, dict]:
    with zipfile.ZipFile(zpath) as z:
        raw = z.read("registro_de_puertas.csv").decode("utf-8")
    puertas = {}
    for fila in csv.DictReader(io.StringIO(raw)):
        n = int(fila["puerta"])
        puertas[n] = {
            "sello": int(fila["sello"]),
            "izq": int(fila["paso_izq"]),
            "der": int(fila["paso_der"]),
            "banda": fila["banda"],
            "estado": fila["estado"].strip(),
        }
    return puertas


def siguiente_sello(s: int) -> int:
    return (3 * s + 7) % MOD


def main() -> int:
    puertas = cargar(ZIP)
    print(f"[*] {len(puertas)} puertas cargadas")

    actual = INICIO
    recorrido = [actual]
    for paso in range(1, LARGO):
        esperado = siguiente_sello(puertas[actual]["sello"])
        opciones = {"IZQ": puertas[actual]["izq"], "DER": puertas[actual]["der"]}
        validas = [lado for lado, dest in opciones.items() if puertas[dest]["sello"] == esperado]
        if len(validas) != 1:
            print(f"[!] paso {paso+1}: {len(validas)} salidas validas desde puerta {actual} "
                  f"(esperado sello {esperado}, opciones {opciones})")
            return 1
        lado = validas[0]
        destino = opciones[lado]
        print(f"    puerta {actual:02d} (sello {puertas[actual]['sello']:2d}) "
              f"-> esperado {esperado:2d} -> {lado} -> puerta {destino:02d}")
        actual = destino
        recorrido.append(actual)

    print(f"[*] recorrido: {' -> '.join(f'{p:02d}' for p in recorrido)} ({len(recorrido)} puertas)")
    estado = puertas[actual]["estado"]
    print(f"[*] estado final: {estado}")
    if estado != "SALIDA":
        print("[!] la ronda no termina en SALIDA")
        return 1

    bandas = [puertas[p]["banda"] for p in recorrido]
    print("\n    columnas (orden de visita):")
    for p, b in zip(recorrido, bandas):
        print(f"      {p:02d}: {b}")
    if any(len(b) != 5 for b in bandas):
        print("[!] alguna banda no tiene 5 simbolos")
        return 1

    mensaje = "".join(b[i] for i in range(5) for b in bandas)
    print(f"\nFLAG: {mensaje}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
