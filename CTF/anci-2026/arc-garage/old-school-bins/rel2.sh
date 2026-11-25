#!/bin/bash
cd "$(dirname "$0")" || exit 1
cat > /tmp/g3.gdb <<'EOF'
set pagination off
set confirm off
break *(main+0x32)
commands
silent
set $pie = (unsigned long)&garage - 0x54a0
set $car = *(unsigned long*)&garage
set $stack = (unsigned long)$rsp
printf "RESULT pie=%#lx car=%#lx stack=%#lx\n", $pie, $car, $stack
info proc mappings
quit
end
run < /dev/null
EOF
for i in 1 2 3; do
  gdb -q -batch -ex "set disable-randomization off" -x /tmp/g3.gdb ./chall 2>/dev/null | grep -E "RESULT|/lib/ld-musl|chall|\[heap\]|\[stack\]" | head -20
  echo "-----"
done
