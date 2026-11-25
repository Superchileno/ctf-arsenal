#!/usr/bin/env python3
"""Correlación temporal: qué flujo ocurrió en la ventana del incidente (01:46-01:49)."""
import csv
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/fantasma/work")
patron = re.compile(r'^(\S+) - - \[([^\]]+)\].*"GET /telemetry/sync\?rid=([^&"]+)&p=([^ "]+)')
info = {}
for l in W.joinpath("access.log").read_text(errors="replace").splitlines():
    m = patron.search(l)
    if m:
        ip, fecha, rid, p = m.groups()
        info[rid] = (ip, datetime.strptime(fecha, "%d/%b/%Y:%H:%M:%S %z"), p)

filas = list(csv.DictReader(W.joinpath("proxy_trace.csv").open()))
flujos = defaultdict(list)
for f in filas:
    rid = f["request_id"]
    if rid in info:
        flujos[f["flow"]].append((int(f["seq"]), f["terminal"], f["proxy_result"],
                                  info[rid][1], info[rid][0]))

for flow, fs in sorted(flujos.items()):
    fs.sort()
    horas = [x[3] for x in fs]
    ips = sorted({x[4] for x in fs})
    print(f"{flow} [{fs[0][1]}]: {min(horas).time()} .. {max(horas).time()}  IPs={ips}")
    for seq, term, res, hora, ip in fs:
        print(f"   seq {seq:2d}  {hora.time()}  {res:7s} {ip}")
