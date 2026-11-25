#!/bin/bash
D=/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/mantenimiento
cd "$D" || exit 1
echo "===== main (0x11f8) ====="
objdump -d pulso_mantenimiento --start-address=0x11f8 --stop-address=0x1400 | sed -n '6,120p'
echo
echo "===== .rodata ====="
objdump -s -j .rodata pulso_mantenimiento
echo "===== .data ====="
objdump -s -j .data pulso_mantenimiento
echo "===== .data.rel.ro / otras ====="
readelf -SW pulso_mantenimiento | sed -n '1,40p'
