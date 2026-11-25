#!/bin/bash
cd "$(dirname "$0")" || exit 1
printf '1\nHELLOMODEL123456789012345678901234567890\n\n\n\n100\n\n\n\n\n\n\n3\n0\n1\n5\n' > /tmp/one.txt
cat > /tmp/g8.gdb <<'EOF'
set pagination off
set confirm off
break idx_cmp_qsort
run < /tmp/one.txt
set $pie = (unsigned long)&garage - 0x54a0
printf "PIE %#lx\n", $pie
printf "&garage %#lx\n", (unsigned long)&garage
printf "&car_count %#lx\n", (unsigned long)&car_count
set $c0 = *(unsigned long*)&garage
set $m0 = *(unsigned long*)$c0
printf "car0 %#lx model %#lx\n", $c0, $m0
info symbol $m0
x/24gx $pie+0x6000
printf "--- string at model ---\n"
x/s $m0
quit
EOF
gdb -q -batch -ex "set disable-randomization off" -x /tmp/g8.gdb ./chall 2>/dev/null | sed -n '/PIE /,$p' | head -40
