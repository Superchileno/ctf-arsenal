#!/bin/bash
cd /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode 2>/dev/null || mkdir -p /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/longitud
mkdir -p /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/longitud
cd /mnt/c/Users/<usuario>/AppData/Local/Temp/opencode/longitud || exit 1
cp -f "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/longitud/longitud_heredada" . 2>/dev/null
chmod +x longitud_heredada
file longitud_heredada
echo "--- sha256 ---"
sha256sum longitud_heredada
echo "--- checksec ---"
checksec --file=longitud_heredada 2>/dev/null || (readelf -hW longitud_heredada | head -20; readelf -lW longitud_heredada | grep -i "GNU_STACK\|GNU_RELRO\|INTERP")
echo "--- ldd ---"
ldd longitud_heredada 2>&1 | head
echo "--- strings relevantes ---"
strings -n 5 longitud_heredada | grep -iE "flag|trama|pass|clave|longitud|heredad|/bin/sh|system|gets|fgets|scanf" | head -40
