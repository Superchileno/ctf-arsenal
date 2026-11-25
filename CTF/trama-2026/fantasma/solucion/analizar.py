#!/usr/bin/env python3
"""Resumen por flujo del proxy_trace y búsqueda de pistas en los logs."""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/fantasma/work")
filas = list(csv.DictReader(W.joinpath("proxy_trace.csv").open()))

por_flujo = defaultdict(list)
for f in filas:
    por_flujo[f["flow"]].append(f)

for flow, fs in sorted(por_flujo.items()):
    term = Counter(f["terminal"] for f in fs)
    res = Counter(f["proxy_result"] for f in fs)
    st = Counter(f["backend_status"] for f in fs)
    seqs = sorted(int(f["seq"]) for f in fs)
    print(f"{flow}: {len(fs):2d} filas | terminales={dict(term)} | proxy={dict(res)} | backend={dict(st)}")
    print(f"      seqs={seqs}")
    print(f"      enc={set(f['content_encoding'] for f in fs)}")

print("\n=== filas REJECT / no-206 ===")
for f in filas:
    if f["proxy_result"] != "OK" or f["backend_status"] != "206":
        print("  ", f)

print("\n=== cualquier TRAMACTF o 'flag' en los logs ===")
for nombre in ("access.log", "proxy_trace.csv", "parte_turno.txt", "LEEME.txt"):
    txt = W.joinpath(nombre).read_text(errors="replace")
    for m in re.finditer(r"(?i)tramactf|\bflag\b|premio|bon(o|ito)", txt):
        ini = max(0, m.start() - 60)
        print(f"  {nombre}: ...{txt[ini:m.end()+60]}...")

print("\n=== rutas únicas en access.log ===")
rutas = Counter()
for l in W.joinpath("access.log").read_text(errors="replace").splitlines():
    m = re.search(r'"([A-Z]+) ([^ ]+) HTTP', l)
    if m:
        rutas[m.group(2).split("?")[0]] += 1
for r, n in rutas.most_common():
    print(f"  {n:3d}  {r}")
