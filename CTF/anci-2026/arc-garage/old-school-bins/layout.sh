#!/bin/bash
cd "$(dirname "$0")" || exit 1
python3 gen_build.py 60 90 > /tmp/build60.txt
cat > /tmp/g5.gdb <<'EOF'
set pagination off
set confirm off
break idx_cmp_qsort
commands
silent
set $n = *(int*)&car_count
printf "CARS %d\n", $n
set $i = 0
while $i < $n
  set $c = *(unsigned long*)((char*)&garage + 8*$i)
  printf "CAR %d %#lx model=%#lx team=%#lx driver=%#lx engine=%#lx\n", $i, $c, *(unsigned long*)$c, *(unsigned long*)($c+8), *(unsigned long*)($c+0x10), *(unsigned long*)($c+0x18)
  set $i = $i + 1
end
call (int)system("cat /proc/self/maps")
quit
end
run < /tmp/build60.txt
EOF
gdb -q -batch -ex "set disable-randomization off" -x /tmp/g5.gdb ./chall 2>/dev/null | grep -E "^CAR |^CARS|^0x|chall|libc.so|stack" | head -120
