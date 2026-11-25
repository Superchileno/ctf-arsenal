#!/bin/bash
cd "$(dirname "$0")" || exit 1
cat > /tmp/g.gdb <<'EOF'
set pagination off
set confirm off
break prompt_edit_string
commands
silent
printf "=== prompt_edit_string label=%s field=%p lenptr=%p\n", $rdi, $rsi, $rdx
printf "   *field=%p *len=%d\n", *(void**)$rsi, *(int*)$rdx
continue
end
run < ../min_crash.bin
printf "=== CRASH ===\n"
bt 8
printf "garage=%p car3=%p\n", &garage, *(void**)&garage[2]
printf "car3 model=%p team=%p driver=%p engine=%p\n", *(void**)&garage[2], *(void**)((char*)garage[2]+8), *(void**)((char*)garage[2]+0x10), *(void**)((char*)garage[2]+0x18)
printf "car5 model=%p team=%p driver=%p engine=%p\n", *(void**)&garage[4], *(void**)((char*)garage[4]+8), *(void**)((char*)garage[4]+0x10), *(void**)((char*)garage[4]+0x18)
EOF
gdb -q -batch -x /tmp/g.gdb ./chall 2>&1 | grep -v -E 'Invalid input|Car built|GARAGE|ARC|^1\.|^2\.|^3\.|^4\.|^5\.|Select:|Current Garage|Enter car|^\s*$' | tail -60
