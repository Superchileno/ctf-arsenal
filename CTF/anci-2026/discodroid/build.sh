#!/bin/bash
D="/mnt/c/Users/luis.miranda/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ANCI/discodroid"
cd ~
gcc -nostdlib -static -Os -fno-stack-protector -fno-pie -no-pie -fno-asynchronous-unwind-tables -o dp "$D/dp.c" 2>&1 | head -20
ls -l dp
file dp
python3 - "$D/dp" <<'PY'
import sys
d=open(sys.argv[1],'rb').read()
print("size",len(d))
open("/tmp/dp.b64","wb").write(__import__("base64").b64encode(d))
print("b64 size",len(__import__("base64").b64encode(d)))
PY
