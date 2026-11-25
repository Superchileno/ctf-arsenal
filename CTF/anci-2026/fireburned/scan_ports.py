#!/usr/bin/env python3
"""Escanea puertos de challenges2 y clasifica servicios HTTP/banner."""
import concurrent.futures as cf
import socket
import sys

HOST = "<host>"


def probe(port, timeout=1.2):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((HOST, port))
    except Exception:
        return None
    try:
        s.sendall(b"GET / HTTP/1.0\r\nHost: x\r\n\r\n")
        s.settimeout(1.5)
        data = b""
        try:
            while len(data) < 800:
                c = s.recv(800 - len(data))
                if not c:
                    break
                data += c
        except Exception:
            pass
    finally:
        s.close()
    return data


if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 28700
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 29000
    with cf.ThreadPoolExecutor(max_workers=120) as ex:
        futs = {ex.submit(probe, p): p for p in range(start, end)}
        for f in cf.as_completed(futs):
            p = futs[f]
            try:
                d = f.result()
            except Exception:
                continue
            if d is None:
                continue
            first = d.split(b"\r\n", 1)[0][:80]
            title = b""
            if b"<title>" in d:
                title = d.split(b"<title>", 1)[1].split(b"</title>", 1)[0][:60]
            print(f"{p}: {first!r} title={title!r}", flush=True)
