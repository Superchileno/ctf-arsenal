#!/usr/bin/env python3
"""Envia cada posible numero de senal al servicio y reporta salidas distintas."""
import socket

HOST, PORT = "<host>", 28807


def talk(payload, timeout=2.0):
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(timeout)
    s.recv(4096)
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
    return out


if __name__ == "__main__":
    for n in range(0, 65):
        for p in (str(n).encode(), (str(n) + "\n").encode(),
                  ("SIG" + str(n)).encode()):
            out = talk(p)
            if out.strip(b"\n"):
                print(f"{p!r} -> {out!r}")
    print("fin")
