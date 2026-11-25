#!/usr/bin/env python3
"""
Desafío «Centinela» — reconstrucción del incidente C2 a partir de eventos.log (CEF).

Cada línea es un evento CEF de UniFi. Los del incidente tienen
`UNIFIthreat=OUTBOUND.C2.Beacon` y llevan fragmentos del mensaje en
`cs1Label=IncidentFragment cs1=<base64>` + `cn1Label=FragmentIndex cn1=<n>`.

Salida: host, MAC (últimos 4), IP destino, número de intentos bloqueados y mensaje.
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

LOG = Path("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/centinela/eventos.log")


def campos(linea: str) -> dict:
    d = {}
    for m in re.finditer(r"(\w+)=([^=]*?)(?=\s+\w+=|$)", linea):
        d[m.group(1)] = m.group(2).strip()
    return d


eventos = [campos(l) for l in LOG.read_text(errors="replace").splitlines() if l.startswith("CEF:")]

print(f"eventos totales: {len(eventos)}")
print("tipos:", Counter(e.get("UNIFIthreat", e.get("UNIFIcategory", "?")) for e in eventos))

c2 = [e for e in eventos if e.get("UNIFIthreat") == "OUTBOUND.C2.Beacon"]
print(f"\nOUTBOUND.C2.Beacon: {len(c2)}")

# agrupar por (host origen, ip destino)
grupos = defaultdict(list)
for e in c2:
    grupos[(e.get("UNIFIsrcClientHostname"), e.get("src"), e.get("dst"), e.get("dpt"),
            e.get("UNIFIsrcClientMac"))].append(e)

for clave, fs in sorted(grupos.items(), key=lambda kv: -len(kv[1])):
    host, src, dst, dpt, mac = clave
    print(f"\n{host} ({src}) MAC {mac} -> {dst}:{dpt}  eventos={len(fs)}")
    print("  estados:", Counter(f.get("UNIFIthreat") for f in fs))
    print("  resultados:", Counter(f.get("msg", "")[:60] for f in fs))

# tomamos el grupo más grande (el incidente)
clave, fs = max(grupos.items(), key=lambda kv: len(kv[1]))
host, src, dst, dpt, mac = clave
fs.sort(key=lambda f: int(f.get("cn1", 0) or 0))

fragmentos = [(int(f["cn1"]), f["cs1"]) for f in fs if "cs1" in f]
print(f"\nfragmentos: {len(fragmentos)} -> índices {[i for i, _ in fragmentos]}")

import base64
b64 = "".join(x for _, x in fragmentos)
mensaje = base64.b64decode(b64 + "=" * (-len(b64) % 4)).decode(errors="replace")
print("mensaje:", mensaje)
print("\nflag esperada:")
mac4 = mac.replace(":", "")[-4:]
print(f"  TRAMACTF{{{host.lower().replace('-', '_')}_{mac4}_{dst.replace('.', '_')}_{len(fs)}_{mensaje}}}")
