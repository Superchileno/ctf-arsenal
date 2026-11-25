#!/usr/bin/env python3
"""Frameline FG01 client - solved authorize path.

Protocol observed in capture.pcap:
  C->S  HS_CLIENT  body = client_nonce(8)
  S->C  HS_SERVER  body = server_nonce(8)
  C->S  SESS_OPEN  (empty)
  C->S  AUTHORIZE  body = client_nonce XOR server_nonce XOR "FRAMELIN"
  C->S  OP_PULL    (empty)
  S->C  OP_TOKEN   body = flag
"""
from __future__ import annotations

import secrets
import socket
import struct
import sys

MAGIC = b"FG\x01"
VER = 1
HS_CLIENT = 0x01
HS_SERVER = 0x02
SESS_OPEN = 0x03
AUTHORIZE = 0x04
OP_PULL = 0x05
OP_TOKEN = 0x06
STUB_KEY = b"FRAMELIN"


def pack_frame(frame_type: int, body: bytes = b"") -> bytes:
    length = 1 + len(body)
    return MAGIC + bytes([VER]) + struct.pack(">H", length) + bytes([frame_type]) + body


def recvexact(sock: socket.socket, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("closed")
        buf.extend(chunk)
    return bytes(buf)


def read_frame(sock: socket.socket) -> tuple[int, bytes]:
    header = recvexact(sock, 6)
    if header[:3] != MAGIC or header[3] != VER:
        raise ValueError(f"bad header {header!r}")
    (length,) = struct.unpack(">H", header[4:6])
    payload = recvexact(sock, length)
    return payload[0], payload[1:]


def build_authorize_proof(client_nonce: bytes, server_nonce: bytes) -> bytes:
    return bytes(a ^ b ^ k for a, b, k in zip(client_nonce, server_nonce, STUB_KEY))


def session(host: str, port: int) -> bytes:
    client_nonce = secrets.token_bytes(8)
    with socket.create_connection((host, port), timeout=15.0) as sock:
        sock.sendall(pack_frame(HS_CLIENT, client_nonce))
        ftype, body = read_frame(sock)
        if ftype != HS_SERVER or len(body) != 8:
            raise RuntimeError(f"handshake failed {ftype:#x} {body!r}")
        server_nonce = body
        print(f"[*] cnonce={client_nonce.hex()} snonce={server_nonce.hex()}")
        proof = build_authorize_proof(client_nonce, server_nonce)
        print(f"[*] proof ={proof.hex()}")
        sock.sendall(pack_frame(SESS_OPEN))
        sock.sendall(pack_frame(AUTHORIZE, proof))
        sock.sendall(pack_frame(OP_PULL))
        ftype, body = read_frame(sock)
        if ftype != OP_TOKEN:
            raise RuntimeError(f"expected OP_TOKEN, got {ftype:#x} body={body!r}")
        return body


def main() -> int:
    host = sys.argv[1] if len(sys.argv) > 1 else "<host>"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 28812
    token = session(host, port)
    print("[+] token:", token.decode(errors="replace"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
