#!/usr/bin/env python3
"""Redireccion TCP 127.0.0.1:<local> -> <host>:<remoto> (sin privilegios de admin)."""
import socket, sys, threading, time

TARGET = "192.168.226.129"
MAP = {8080: 80, 2222: 22, 3306: 3306, 8443: 443}


def pipe(a, b):
    try:
        while True:
            d = a.recv(65536)
            if not d:
                break
            b.sendall(d)
    except Exception:
        pass
    finally:
        for s in (a, b):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            try:
                s.close()
            except Exception:
                pass


def serve(lport, rport):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", lport))
    srv.listen(64)
    while True:
        c, _ = srv.accept()
        try:
            r = socket.create_connection((TARGET, rport), timeout=10)
        except Exception:
            c.close()
            continue
        threading.Thread(target=pipe, args=(c, r), daemon=True).start()
        threading.Thread(target=pipe, args=(r, c), daemon=True).start()


if __name__ == "__main__":
    for lp, rp in MAP.items():
        threading.Thread(target=serve, args=(lp, rp), daemon=True).start()
        print(f"127.0.0.1:{lp} -> {TARGET}:{rp}", flush=True)
    while True:
        time.sleep(3600)
