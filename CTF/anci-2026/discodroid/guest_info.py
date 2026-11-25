import socket, time, sys

HOST, PORT = "<host>", 28808

def rd(s, t=4):
    s.settimeout(t)
    b = b""
    try:
        while True:
            c = s.recv(65536)
            if not c:
                break
            b += c
    except Exception:
        pass
    return b

s = socket.create_connection((HOST, PORT), timeout=15)
print(rd(s, 6)[-300:])
cmd = ("id; uname -r; ls -la /dev | head -30; echo ---; "
       "cat /proc/sys/kernel/unprivileged_userns_clone 2>&1; "
       "cat /proc/sys/user/max_user_namespaces 2>&1; "
       "cat /proc/sys/kernel/unprivileged_bpf_disabled 2>&1; "
       "ls -la /bin/busybox /init /etc/passwd; "
       "cat /proc/self/status | grep -i cap; "
       "cat /proc/mounts\n")
s.sendall(cmd.encode())
time.sleep(3)
print(rd(s, 5).decode(errors="replace"))
s.close()
