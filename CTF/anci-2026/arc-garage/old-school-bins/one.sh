#!/bin/bash
cd "$(dirname "$0")" || exit 1
printf '1\nHELLOMODEL123456789012345678901234567890\n\n\n\n100\n\n\n\n\n\n\n3\n0\n1\n5\n' > /tmp/one.txt
cat > /tmp/g7.gdb <<'EOF'
set pagination off
set confirm off
break idx_cmp_qsort
run < /tmp/one.txt
set $pie = (unsigned long)&garage - 0x54a0
set $c0 = *(unsigned long*)&garage
set $m0 = *(unsigned long*)$c0
printf "PIE                  %#lx\n", $pie
printf "garage               %#lx\n", (unsigned long)&garage
printf "car0                 %#lx\n", $c0
printf "model0 ptr           %#lx\n", $m0
printf "model0 data          ", 
x/s $m0
printf "map of model0:\n"
info proc mappings
quit
EOF
gdb -q -batch -ex "set disable-randomization off" -x /tmp/g7.gdb ./chall 2>/dev/null | sed -n '/PIE /,$p' | head -50
