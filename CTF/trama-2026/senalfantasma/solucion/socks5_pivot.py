#!/usr/bin/env python3
"""SOCKS5 minimal (CONNECT, sin auth) para pivotar Kali/WSL hacia la red host-only
de VMware (192.168.159.0/24), que WSL en modo mirrored no ve.

Uso: python socks5_pivot.py [puerto]   (por defecto 1080, escucha en 0.0.0.0)
Solo CONNECT TCP; suficiente para nmap -sT, curl, ssh, gobuster, sqlmap, etc.
"""
import socket
import struct
import sys
import threading

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 1080
BUFSIZE = 65536


def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("EOF")
        data += chunk
    return data


def pipe(src, dst):
    try:
        while True:
            data = src.recv(BUFSIZE)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass


def handle(client):
    remote = None
    try:
        ver, nmethods = recv_exact(client, 2)
        if ver != 5:
            client.close()
            return
        recv_exact(client, nmethods)
        client.sendall(b"\x05\x00")

        ver, cmd, rsv, atyp = recv_exact(client, 4)
        if atyp == 1:
            host = socket.inet_ntoa(recv_exact(client, 4))
        elif atyp == 3:
            (ln,) = struct.unpack("!B", recv_exact(client, 1))
            host = recv_exact(client, ln).decode()
        elif atyp == 4:
            host = socket.inet_ntop(socket.AF_INET6, recv_exact(client, 16))
        else:
            client.sendall(b"\x05\x08\x00\x01" + b"\x00" * 6)
            client.close()
            return
        (port,) = struct.unpack("!H", recv_exact(client, 2))

        if cmd != 1:  # solo CONNECT
            client.sendall(b"\x05\x07\x00\x01" + b"\x00" * 6)
            client.close()
            return

        remote = socket.create_connection((host, port), timeout=15)
        remote.settimeout(None)
        bind_ip, bind_port = remote.getsockname()[:2]
        reply = b"\x05\x00\x00\x01" + socket.inet_aton(bind_ip) + struct.pack("!H", bind_port)
        client.sendall(reply)
        client.settimeout(None)

        t = threading.Thread(target=pipe, args=(remote, client), daemon=True)
        t.start()
        pipe(client, remote)
        t.join(timeout=5)
    except Exception:
        try:
            client.sendall(b"\x05\x01\x00\x01" + b"\x00" * 6)
        except OSError:
            pass
    finally:
        for s in (client, remote):
            if s is not None:
                try:
                    s.close()
                except OSError:
                    pass


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORT))
    srv.listen(128)
    print(f"[*] SOCKS5 escuchando en 0.0.0.0:{PORT}", flush=True)
    while True:
        try:
            client, addr = srv.accept()
        except OSError:
            continue
        threading.Thread(target=handle, args=(client,), daemon=True).start()


if __name__ == "__main__":
    main()
