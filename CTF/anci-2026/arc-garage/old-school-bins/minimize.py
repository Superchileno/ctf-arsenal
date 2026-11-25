import subprocess, os, sys

BIN = os.path.dirname(os.path.abspath(__file__))
CHALL = os.path.join(BIN, 'chall')

def crashes(data):
    try:
        p = subprocess.run([CHALL], input=data, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=3.0, cwd=BIN)
        return p.returncode < 0
    except subprocess.TimeoutExpired:
        return False

def ddmin(lines, tries):
    n = 2
    while len(lines) >= 2:
        chunk = max(1, len(lines)//n)
        reduced = False
        for i in range(0, len(lines), chunk):
            cand = lines[:i] + lines[i+chunk:]
            if not cand:
                continue
            tries[0] += 1
            if crashes(b'\n'.join(cand) + b'\n'):
                lines = cand
                n = max(n-1, 2)
                reduced = True
                print('reduced to', len(lines), 'lines after', tries[0], 'tries', flush=True)
                break
        if not reduced:
            if n >= len(lines):
                break
            n = min(len(lines), n*2)
    return lines

path = sys.argv[1]
data = open(path, 'rb').read()
lines = data.split(b'\n')
if lines and lines[-1] == b'':
    lines.pop()
print('start lines', len(lines), 'crash', crashes(b'\n'.join(lines)+b'\n'))
tries = [0]
lines = ddmin(lines, tries)
out = b'\n'.join(lines) + b'\n'
open('min_crash.bin', 'wb').write(out)
print('FINAL', len(lines), 'lines', len(out), 'bytes, tries', tries[0], 'crash', crashes(out))
for i, l in enumerate(lines):
    print(i, repr(l[:120]), '...' if len(l) > 120 else '')
