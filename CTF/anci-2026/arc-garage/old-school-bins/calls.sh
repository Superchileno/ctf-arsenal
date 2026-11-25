#!/bin/bash
cd "$(dirname "$0")" || exit 1
echo "=== printf/puts/fprintf/fwrite/strlen calls with preceding 6 insns ==="
awk '
/^[ ]+[0-9a-f]+:/ { ins[NR]=$0 }
END{}
' dis.txt >/dev/null
grep -n -B6 "call.*<printf@plt>" dis.txt | grep -E "lea +rdi|mov +rdi|call|<.*>:" | head -120
