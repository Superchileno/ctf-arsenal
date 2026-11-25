#!/bin/bash
cd "$(dirname "$0")" || exit 1
python3 gen_build.py 60 90 > /tmp/build60.txt
cat > /tmp/g6.gdb <<'EOF'
set pagination off
set confirm off
break idx_cmp_qsort
commands
silent
set $n = *(int*)&car_count
printf "CARS %d pie=%#lx\n", $n, (unsigned long)&garage - 0x54a0
set $i = 0
while $i < $n
  set $c = *(unsigned long*)((char*)&garage + 8*$i)
  if $i < 8 || $i > 55
    printf "CAR %d %#lx model=%#lx\n", $i, $c, *(unsigned long*)$c
  end
  set $i = $i + 1
end
info proc mappings
quit
end
run < /tmp/build60.txt
EOF
gdb -q -batch -ex "set disable-randomization off" -x /tmp/g6.gdb ./chall 2>/dev/null | sed -n '/CARS/,$p' | head -70
