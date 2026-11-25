#!/usr/bin/env python3
"""Sonda interactiva: envia lineas y reporta lo que devuelve el servidor."""
import socket
import sys
import time

HOST, PORT = "<host>", 28807


def run(lines, wait=1.0, read_timeout=2.0):
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(read_timeout)
    out = []
    for line in lines:
        try:
            out.append(s.recv(4096))
        except socket.timeout:
            pass
        s.sendall(line if isinstance(line, bytes) else line.encode() + b"\n")
        time.sleep(wait)
        try:
            out.append(s.recv(8192))
        except socket.timeout:
            out.append(b"<timeout>")
    time.sleep(wait)
    try:
        while True:
            d = s.recv(8192)
            if not d:
                out.append(b"<EOF>")
                break
            out.append(d)
    except socket.timeout:
        out.append(b"<timeout>")
    s.close()
    return b"".join(out)


if __name__ == "__main__":
    lines = sys.argv[1:] or ["hello"]
    print(run(lines).decode("utf-8", "replace"))
