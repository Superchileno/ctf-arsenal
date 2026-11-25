import socket, time, threading, sys, re

HOST, PORT = "<host>", 28808
BIN = sys.argv[1] if len(sys.argv) > 1 else r"ANCI\discodroid\diag"
CMD = sys.argv[2] if len(sys.argv) > 2 else "/tmp/diag"
B64 = open(BIN + ".b64").read().splitlines()

buf = bytearray(); lock = threading.Lock(); stop = False

def reader(s):
    while not stop:
        try:
            d = s.recv(65536)
            if not d: break
            with lock: buf.extend(d)
        except socket.timeout: continue
        except Exception: break

def wait_for(pats, timeout=60):
    t0 = time.time()
    while time.time() - t0 < timeout:
        with lock: data = bytes(buf)
        for p in pats:
            if p in data: return p
        time.sleep(0.2)
    return None

def send(s, data, delay=0.004):
    if isinstance(data, str): data = data.encode()
    for i in range(0, len(data), 256):
        s.sendall(data[i:i+256]); time.sleep(delay)

def main():
    global stop
    s = socket.create_connection((HOST, PORT), timeout=20)
    s.settimeout(2)
    threading.Thread(target=reader, args=(s,), daemon=True).start()
    if not wait_for([b"/ $ "], 90):
        print("no shell"); return
    print("[*] shell up; uploading %d lines" % len(B64))
    send(s, "cat > /tmp/x.b64 << 'EOF'\n")
    for line in B64: send(s, line + "\n", 0.003)
    send(s, "EOF\n"); time.sleep(0.8)
    send(s, "base64 -d /tmp/x.b64 > /tmp/x && chmod +x /tmp/x && echo UPOK\n")
    if not wait_for([b"UPOK"], 60):
        print("upload failed"); return
    with lock: mark = len(buf)
    send(s, CMD + "; echo RUNEND\n")
    wait_for([b"RUNEND"], 300)
    time.sleep(0.8)
    with lock: out = bytes(buf)[mark:]
    print("=== OUT ===")
    print(out.decode(errors="replace"))
    stop = True; s.close()

main()
