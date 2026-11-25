#!/bin/bash
cd "$(dirname "$0")" || exit 1
printf '5\n' > /tmp/x.txt
cat > /tmp/g9.gdb <<'EOF'
set pagination off
set confirm off
break *(main+0x32)
run < /tmp/x.txt
set $pie = (unsigned long)&garage - 0x54a0
printf "PIE %#lx _end-ish %#lx\n", $pie, $pie+0x6990
call (void*)brk(0)
printf "brk0 %#lx\n", $rax
call (void*)malloc(26)
printf "malloc26 %#lx\n", $rax
call (void*)malloc(200)
printf "malloc200 %#lx\n", $rax
call (void*)malloc(2000)
printf "malloc2000 %#lx\n", $rax
info proc mappings
quit
EOF
gdb -q -batch -ex "set disable-randomization off" -x /tmp/g9.gdb ./chall 2>/dev/null | sed -n '/PIE /,$p' | head -40
