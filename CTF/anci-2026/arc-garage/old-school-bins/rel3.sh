#!/bin/bash
cd "$(dirname "$0")" || exit 1
cat > /tmp/g4.gdb <<'EOF'
set pagination off
set confirm off
break *(main+0x32)
run < /dev/null
set $pie = (unsigned long)&garage - 0x54a0
set $car = *(unsigned long*)&garage
printf "RESULT pie=%#lx car=%#lx\n", $pie, $car
info proc mappings
quit
EOF
for i in 1 2; do
  gdb -q -batch -ex "set disable-randomization off" -x /tmp/g4.gdb ./chall 2>/dev/null | sed -n '/RESULT/,$p' | head -45
  echo "======"
done
