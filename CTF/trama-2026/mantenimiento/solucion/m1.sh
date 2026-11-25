#!/bin/bash
D=/mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/mantenimiento
mkdir -p "$D" && cd "$D" || exit 1
cp -f "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/mantenimiento/pulso_mantenimiento" . 2>/dev/null
chmod +x pulso_mantenimiento
file pulso_mantenimiento
sha256sum pulso_mantenimiento
echo "--- checksec ---"
checksec --file=pulso_mantenimiento 2>/dev/null
echo "--- strings ---"
strings -n 4 pulso_mantenimiento | head -80
echo "--- ejecucion con entrada vacia ---"
echo "" | timeout 5 ./pulso_mantenimiento; echo "[rc=$?]"
