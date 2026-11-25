#!/bin/bash
cd ~
echo "=== tee/link symbols ==="
nm /tmp/vmlinux.elf | grep -iE 'link_pipe|do_tee|__x64_sys_tee|pipe_buf_get'
echo "=== disasm link_pipe ==="
A=$(nm /tmp/vmlinux.elf | awk '$3=="link_pipe"{print $1}')
echo "link_pipe at $A"
objdump -d --start-address=0x$A --stop-address=0x$(printf '%x' $((0x$A+0x400))) /tmp/vmlinux.elf 2>/dev/null | sed -n '1,200p'
