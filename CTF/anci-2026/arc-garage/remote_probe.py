import socket, time, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HOST, PORT = '<host>', 28809
ANSI = re.compile(rb'\x1b\[[0-9;]*m')
def run(inputs, wait=0.5):
    s = socket.create_connection((HOST, PORT), timeout=10); s.settimeout(wait)
    out=b''
    def drain(t):
        nonlocal out
        end=time.time()+t
        while time.time()<end:
            try: c=s.recv(8192)
            except socket.timeout: continue
            if not c: return
            out+=c
    drain(1.0)
    for line in inputs:
        s.sendall(line.encode()+b'\n'); drain(0.45)
    drain(0.6); s.close()
    return ANSI.sub(b'', out).decode('utf-8','replace')

def probe(tag, seq):
    print('=====', tag)
    out = run(seq)
    print(out[-1200:].encode('ascii','replace').decode('ascii'))

probe('fmt', ['1','%p.%p.%p.%p.%p.%p','%x.%x','','','100','','','','','','','3','1','1','5'])
probe('menu6', ['6','5'])
probe('menu0', ['0','5'])
