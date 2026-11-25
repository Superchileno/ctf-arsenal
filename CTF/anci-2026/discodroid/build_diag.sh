#!/bin/bash
D="/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ANCI/discodroid"
cd ~
gcc -nostdlib -static -Os -fno-stack-protector -fno-pie -no-pie -fno-asynchronous-unwind-tables -o diag "$D/diag.c" && \
base64 -w 400 diag > "$D/diag.b64" && cp diag "$D/diag" && wc -c diag "$D/diag.b64"
