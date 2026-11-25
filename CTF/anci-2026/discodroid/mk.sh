#!/bin/bash
D="/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ANCI/discodroid"
name="$1"
cd ~
gcc -nostdlib -static -Os -fno-builtin -fno-stack-protector -fno-pie -no-pie \
    -fno-asynchronous-unwind-tables -o "$name" "$D/$name.c" || exit 1
cp "$name" "$D/$name"
base64 -w 400 "$name" > "$D/$name.b64"
wc -c "$name" "$D/$name.b64"
