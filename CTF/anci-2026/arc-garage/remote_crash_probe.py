import socket, time, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HOST, PORT = '<host>', 28809
ANSI = re.compile(rb'\x1b\[[0-9;]*m')
raw = open('min_crash.bin','rb').read()
lines = raw.split(b'\n')
s = socket.create_connection((HOST, PORT), timeout=10); s.settimeout(0.5)
out=b''
def drain(t):
    global out
    end=time.time()+t
    while time.time()<end:
        try: c=s.recv(8192)
        except socket.timeout: continue
        if not c: return False
        out+=c
    return True
drain(1.0)
alive=True
for i,l in enumerate(lines[:16]):
    try:
        s.sendall(l+b'\n')
    except Exception as e:
        print('send fail at', i, e); alive=False; break
    if not drain(0.5):
        print('CONNECTION CLOSED after line', i); alive=False; break
if alive:
    # try to see if it asks for the next field (survived)
    try:
        s.sendall(b'\n'); drain(0.4)
    except Exception as e:
        print('post-send fail', e)
txt = ANSI.sub(b'', out).decode('utf-8','replace')
print('=== tail ===')
print(txt[-1500:].encode('ascii','replace').decode('ascii'))
print('=== survived?', alive)
s.close()
