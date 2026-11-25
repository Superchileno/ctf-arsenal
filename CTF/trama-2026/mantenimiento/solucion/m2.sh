#!/bin/bash
D=/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/mantenimiento
cd "$D" || exit 1
echo "=== prueba ORION-03 ==="
printf 'ORION-03\n' | ./pulso_mantenimiento
echo
echo "=== entry / main ==="
readelf -hW pulso_mantenimiento | grep Entry
objdump -d pulso_mantenimiento --start-address=0x1000 --stop-address=0x1400 2>/dev/null | sed -n '6,80p'
