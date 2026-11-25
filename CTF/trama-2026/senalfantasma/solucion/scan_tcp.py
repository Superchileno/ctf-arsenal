#!/usr/bin/env python3
"""Escaneo TCP connect rápido desde Windows hacia la VM host-only.
Uso: python scan_tcp.py <ip> [puertos|all]
"""
import socket
import sys
import concurrent.futures

ip = sys.argv[1]
spec = sys.argv[2] if len(sys.argv) > 2 else "all"
if spec == "all":
    ports = range(1, 65536)
else:
    ports = [int(p) for p in spec.split(",")]


def probe(p):
    s = socket.socket()
    s.settimeout(0.7)
    try:
        if s.connect_ex((ip, p)) == 0:
            return p
    except OSError:
        return None
    finally:
        s.close()
    return None


open_ports = []
with concurrent.futures.ThreadPoolExecutor(max_workers=400) as ex:
    for r in ex.map(probe, ports, chunksize=64):
        if r:
            open_ports.append(r)
            print(f"[+] {ip}:{r} abierto", flush=True)

print("ABIERTOS:", ",".join(map(str, sorted(open_ports))))
