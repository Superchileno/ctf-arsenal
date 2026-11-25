#!/usr/bin/env python3
"""Busca el umbral de desbordamiento del servicio Sigcall."""
import socket
import sys

HOST, PORT = "<host>", 28807


def try_len(n, ch=b"A"):
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(3)
    banner = s.recv(4096)
    s.sendall(ch * n)
    out = b""
    try:
        while True:
            d = s.recv(4096)
            if not d:
                break
            out += d
    except socket.timeout:
        pass
    s.close()
    return banner, out


if __name__ == "__main__":
    lengths = [int(x) for x in sys.argv[1:]] or [16, 32, 48, 64, 65, 72, 80, 96, 112, 128, 160, 192, 224, 256, 300]
    for n in lengths:
        b, out = try_len(n)
        crashed = b"Segmentation" in out or b"core dumped" in out
        print(f"{n:4d} bytes -> {'CRASH' if crashed else 'ok/exit'}  {out[:120]!r}")
