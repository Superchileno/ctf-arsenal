#!/usr/bin/env python3
"""Prueba entradas concretas y muestra la respuesta cruda (hex+ascii)."""
import socket
import sys

HOST, PORT = "<host>", 28807

CANDIDATES = [
    b"", b"\n", b"0\n", b"1\n", b"flag", b"flag\n", b"getflag", b"getflag\n",
    b"sigcall", b"sigcall\n", b"admin", b"admin\n", b"sh", b"sh\n",
    b"/bin/sh", b"/bin/sh\n", b"cat /flag.txt", b"cat /flag.txt\n",
    b"%s", b"%s\n", b"%n", b"%n\n", b"help", b"help\n", b"password",
    b"pass", b"letmein", b"token", b"env", b"ls", b"id", b"whoami",
]


def talk(payload, timeout=2.0):
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(timeout)
    banner = s.recv(4096)
    s.sendall(payload)
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
    for p in CANDIDATES:
        b, out = talk(p)
        if out.strip(b"\n"):
            print(f"input={p!r:24} banner={b!r} -> OUT={out!r}")
        else:
            print(f"input={p!r:24} -> (sin salida) {out!r}")
