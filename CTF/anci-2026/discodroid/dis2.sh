#!/bin/bash
cd ~
echo "=== iov_iter symbols ==="
nm /tmp/vmlinux.elf | grep -iE 'copy_page_to_iter|iov_iter' | head -20
echo "=== do_splice full ==="
objdump -d --start-address=0xffffffff81614590 --stop-address=0xffffffff816156c0 /tmp/vmlinux.elf 2>/dev/null | head -400
