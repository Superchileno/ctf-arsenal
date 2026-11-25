#!/bin/bash
cd /mnt/c/Users/shapl/AppData/Local/Temp/opencode/longitud || exit 1
echo "=== ejecucion simple ==="
printf '8\nAAAA\n' | timeout 5 ./longitud_heredada 2>&1 | head -20
echo "=== exit: $? ==="
echo
echo "=== _start (entry) ==="
readelf -hW longitud_heredada | grep Entry
objdump -d --start-address=0x40173f --stop-address=0x4017a0 longitud_heredada | tail -25
