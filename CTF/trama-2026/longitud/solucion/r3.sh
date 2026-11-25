#!/bin/bash
cd /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/longitud || exit 1
echo "===== funcion en 0x4018a5 (pulso) ====="
objdump -d --start-address=0x4018a5 --stop-address=0x401ac7 longitud_heredada | sed -n '7,120p'
echo
echo "===== main 0x401ac7 ====="
objdump -d --start-address=0x401ac7 --stop-address=0x401d80 longitud_heredada | sed -n '7,200p'
