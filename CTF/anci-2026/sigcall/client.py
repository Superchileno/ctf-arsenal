#!/usr/bin/env python3
"""Cliente simple para el reto Sigcall (<host>:28807)."""
import socket
import sys
import time

HOST, PORT = "<host>", 28807


def recv_all(s, timeout=3.0):
    s.settimeout(timeout)
    buf = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
        except socket.timeout:
            break
    return buf


def main():
    payload = sys.stdin.buffer.read() if not sys.stdin.isatty() else b""
    s = socket.create_connection((HOST, PORT), timeout=10)
    banner = recv_all(s)
    sys.stdout.write(banner.decode("utf-8", "replace"))
    if payload:
        s.sendall(payload)
        time.sleep(0.5)
        sys.stdout.write(recv_all(s, 5).decode("utf-8", "replace"))
    s.close()


if __name__ == "__main__":
    main()
