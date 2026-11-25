#!/usr/bin/env python3
"""Sonda de comportamiento del servicio Sigcall.

Uso:
    python probe2.py idle                # solo banner, mide si mantiene la conexion
    python probe2.py send <texto>        # envia texto (sin newline) y mide respuesta
    python probe2.py line <texto>        # envia texto + \n
    python probe2.py raw <hex>           # envia bytes en hexadecimal
    python probe2.py big <n> [char]      # envia n bytes repetidos
"""
import socket
import sys
import time

HOST, PORT = "<host>", 28807


def exchange(payload=None, idle_wait=3.0, read_timeout=2.0):
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(read_timeout)
    t0 = time.time()

    def read(tag):
        data = b""
        while True:
            try:
                chunk = s.recv(65536)
            except socket.timeout:
                return data, "timeout"
            if not chunk:
                return data, "EOF"
            data += chunk
            # pequena pausa para agrupar
            time.sleep(0.05)

    banner, st = read("banner")
    print(f"[{time.time()-t0:6.2f}s] banner ({len(banner)} b, {st}): {banner[:200]!r}")
    if payload is None:
        time.sleep(idle_wait)
        data, st = read("idle")
        print(f"[{time.time()-t0:6.2f}s] idle   ({len(data)} b, {st}): {data[:400]!r}")
    else:
        s.sendall(payload)
        print(f"[{time.time()-t0:6.2f}s] enviado {len(payload)} b")
        for i in range(3):
            data, st = read("resp")
            print(f"[{time.time()-t0:6.2f}s] resp{i}  ({len(data)} b, {st}): {data[:400]!r}")
            if st == "EOF":
                break
            time.sleep(0.3)
    s.close()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "idle"
    if cmd == "idle":
        exchange(None)
    elif cmd == "send":
        exchange(sys.argv[2].encode())
    elif cmd == "line":
        exchange(sys.argv[2].encode() + b"\n")
    elif cmd == "raw":
        exchange(bytes.fromhex(sys.argv[2]))
    elif cmd == "big":
        n = int(sys.argv[2])
        ch = (sys.argv[3] if len(sys.argv) > 3 else "A")[:1].encode()
        exchange(ch * n)
    else:
        print(__doc__)
