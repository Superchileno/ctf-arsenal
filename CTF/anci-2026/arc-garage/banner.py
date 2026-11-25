import socket, time, sys
host, port = '<host>', 28809
s = socket.create_connection((host, port), timeout=15)
s.settimeout(5)
data = b''
t0 = time.time()
while time.time() - t0 < 7:
    try:
        c = s.recv(4096)
    except socket.timeout:
        break
    if not c:
        break
    data += c
s.close()
open('banner_raw.bin', 'wb').write(data)
print('bytes', len(data))
print('HEX ', data.hex())
print('REPR', repr(data))
txt = data.decode('utf-8', 'replace')
sys.stdout.buffer.write(('=== TEXT ===\n' + txt + '\n=== END ===\n').encode('utf-8', 'replace'))
