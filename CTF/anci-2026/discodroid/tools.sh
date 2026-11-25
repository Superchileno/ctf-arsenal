#!/bin/bash
D="/mnt/c/Users/luis.miranda/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ANCI/discodroid/extracted/discodroid"
echo "--- tools ---"
for t in qemu-system-x86_64 gcc musl-gcc tcc strip base64 cpio; do printf "%s: " "$t"; command -v "$t" || echo MISSING; done
echo "--- image ---"
file "$D/Image"
ls -l "$D"
echo "--- strings version ---"
strings -n 6 "$D/Image" | grep -m5 -E 'Linux version|5\.[0-9]+\.[0-9]+'
echo "--- busybox applets? ---"
ls ~/ddroot/bin ~/ddroot/usr/bin 2>/dev/null | head -40
