#!/bin/bash
cd ~
echo "=== symbols matching splice/pipe ==="
nm /tmp/vmlinux.elf 2>/dev/null | grep -iE 'splice|pipe_buf' | grep -iE ' T | t ' | head -40
echo "=== disasm splice_pipe_to_pipe ==="
objdump -d --start-address=0xffffffff81613000 --stop-address=0xffffffff81613230 /tmp/vmlinux.elf 2>/dev/null | grep -E 'call|jmp' | head -40
echo "=== look for pipe_buf_get symbol ==="
nm /tmp/vmlinux.elf | grep -i 'pipe_buf_get'
