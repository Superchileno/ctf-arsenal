import socket, time, re, sys

HOST, PORT = '<host>', 28809
ANSI = re.compile(rb'\x1b\[[0-9;]*m')

def clean(b):
    return ANSI.sub(b'', b).decode('utf-8', 'replace')

def run(inputs, wait=0.6, total=12):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(wait)
    out = b''
    t0 = time.time()
    def drain(t):
        nonlocal out
        end = time.time() + t
        while time.time() < end:
            try:
                c = s.recv(8192)
            except socket.timeout:
                continue
            if not c:
                return False
            out += c
        return True
    drain(1.2)
    for line in inputs:
        if isinstance(line, str):
            line = line.encode()
        s.sendall(line + b'\n')
        drain(0.7)
    drain(1.0)
    s.close()
    return clean(out)

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    seq = sys.argv[1:]
    out = run(seq)
    with open('last_session.log', 'w', encoding='utf-8') as f:
        f.write(out)
    print(out.encode('ascii', 'replace').decode('ascii'))
