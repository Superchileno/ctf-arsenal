#!/bin/bash
cd ~
echo "=== anon_pipe_buf_release ==="
objdump -d --start-address=0xffffffff815d26b0 --stop-address=0xffffffff815d2740 /tmp/vmlinux.elf 2>/dev/null | sed -n '6,60p'
echo "=== anon_pipe_buf_try_steal ==="
objdump -d --start-address=0xffffffff815d2650 --stop-address=0xffffffff815d26b0 /tmp/vmlinux.elf 2>/dev/null | sed -n '6,40p'
