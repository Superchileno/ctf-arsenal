#!/bin/bash
set -e
D="/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ANCI/discodroid/extracted/discodroid"
cd ~
rm -rf ddroot && mkdir ddroot && cd ddroot
cpio -idmv < "$D/rootfs.cpio" 2>/dev/null | tail -3
echo "=== top ==="
ls -la
echo "=== init ==="
cat init 2>/dev/null || true
echo "=== passwd ==="
cat etc/passwd 2>/dev/null || true
echo "=== setuid ==="
find . -perm -4000 -o -perm -2000 2>/dev/null | head -20
echo "=== interesting ==="
ls -la flag* root* dev 2>/dev/null || true
echo "=== kernel version ==="
strings "$D/Image" | grep -m3 -E 'Linux version [0-9]' || true
