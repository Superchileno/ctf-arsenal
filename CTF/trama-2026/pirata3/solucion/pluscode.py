#!/usr/bin/env python3
"""
Pirata 3 — unión de los dos fragmentos y cálculo del Plus Code GLOBAL (Open Location Code, 10).

Fragmentos:
  DG-003 (Pirata 1, LSB del WAV): "19.914434,"
  DG-004 (Pirata 2, pie del DOCX): "38.776970"

Se prueban las dos asignaciones lat/lon posibles y se muestran ambos Plus Codes.
"""
import itertools

ALFABETO = "23456789CFGHJMPQRVWX"     # 20 símbolos del Open Location Code
PARES = 5                              # 10 caracteres = 5 pares


def plus_code(lat: float, lon: float, largo: int = 10) -> str:
    lat = min(max(lat, -90.0), 90.0 - 1e-9) + 90.0
    lon = (lon + 180.0) % 360.0
    codigo = []
    lat_res, lon_res = 180.0, 360.0
    for _ in range(PARES):
        lat_res /= 20.0
        lon_res /= 20.0
        codigo.append(ALFABETO[int(lat / lat_res)])
        codigo.append(ALFABETO[int(lon / lon_res)])
        lat -= int(lat / lat_res) * lat_res
        lon -= int(lon / lon_res) * lon_res
    codigo = "".join(codigo)
    return codigo[:8] + "+" + codigo[8:largo]


frag_dg003 = 19.914434
frag_dg004 = 38.776970

print("Opción A (orden de expedientes, lat,lon):")
a = plus_code(frag_dg003, frag_dg004)
print(f"  lat={frag_dg003} lon={frag_dg004}  ->  {a}")

print("\nOpción B (invertido: lat=DG-004, lon=DG-003):")
b = plus_code(frag_dg004, frag_dg003)
print(f"  lat={frag_dg004} lon={frag_dg003}  ->  {b}")

print("\nflag A: TRAMACTF{El_B0t1n_D3_M4l4p4t4_3st4_3n_" + a + "}")
print("flag B: TRAMACTF{El_B0t1n_D3_M4l4p4t4_3st4_3n_" + b + "}")
