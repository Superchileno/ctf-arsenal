#!/bin/bash
cd ~
for a in 815d0730 81612760 815d06c0 815d0780; do
  echo "=== $a ==="
  objdump -d --start-address=0xffffffff$a --stop-address=0xffffffff$(printf '%x' $((0x$a+0x60))) /tmp/vmlinux.elf 2>/dev/null | sed -n '6,40p'
done
