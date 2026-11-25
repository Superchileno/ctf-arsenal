#!/bin/bash
cd /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/mantenimiento || exit 1
echo "=== ejecucion con la orden descifrada ==="
printf 'flag{ejemplo}\n' | ./pulso_mantenimiento
echo "[rc=$?]"
echo
echo "=== control: orden incorrecta ==="
printf 'flag{ejemplo}\n' | ./pulso_mantenimiento
echo "[rc=$?]"
