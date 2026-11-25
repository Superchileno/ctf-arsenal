import subprocess, random, os, sys, signal

BIN = os.path.dirname(os.path.abspath(__file__))
LOADER = os.path.join(BIN, 'libc.so')
CHALL = os.path.join(BIN, 'chall')

def run(data, timeout=2.0):
    try:
        p = subprocess.run([LOADER, CHALL], input=data, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=timeout, cwd=BIN)
        return p.returncode
    except subprocess.TimeoutExpired:
        return 'timeout'

pool = [b'', b'-', b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'999', b'-1',
        b'2147483647', b'4294967295', b'99999999999999999999', b'1m2s', b'300m0s',
        b'A'*10, b'B'*79, b'C'*72, b'D'*1023, b'%p%p%p', b'../../flag.txt', b'nan', b'inf', b'1e999']

def rand_line():
    r = random.random()
    if r < 0.5:
        return random.choice(pool)
    if r < 0.8:
        return bytes(random.choice(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ') for _ in range(random.randint(1, 1100)))
    return bytes(random.randint(1, 255) for _ in range(random.randint(1, 60))).replace(b'\n', b'x')

crashes = []
random.seed(1)
for it in range(400):
    lines = [b'3', b'0', b'1']  # show garage, sort none, ascending
    for _ in range(random.randint(0, 40)):
        choices = [b'1', b'3', b'4', b'2']
        lines.append(random.choice(choices))
        for _ in range(random.randint(0, 12)):
            lines.append(rand_line())
    lines.append(b'5')
    data = b'\n'.join(lines) + b'\n'
    rc = run(data)
    if rc not in (0, 'timeout'):
        crashes.append((it, rc, data))
        print('CRASH', it, rc, file=sys.stderr)
        with open('crash_%d.bin' % it, 'wb') as f:
            f.write(data)
        if len(crashes) > 5:
            break
print('done, crashes:', len(crashes))
for it, rc, data in crashes:
    print(it, rc, len(data))
