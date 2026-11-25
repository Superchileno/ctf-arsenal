import subprocess, os
BIN = os.path.dirname(os.path.abspath(__file__))
data = open(os.path.join(os.path.dirname(BIN), 'min_crash.bin'), 'rb').read()
lines = data.split(b'\n')
for i, l in enumerate(lines):
    print(i, len(l), repr(l))
