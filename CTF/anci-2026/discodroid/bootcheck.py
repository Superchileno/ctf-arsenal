import socket,time
s=socket.create_connection(("<host>",28808),timeout=20)
s.settimeout(5)
b=b""
t=time.time()
while time.time()-t<60:
    try:
        d=s.recv(65536)
        if not d: break
        b+=d
    except socket.timeout:
        pass
print(len(b))
print(b[-1500:].decode(errors="replace"))
s.close()
