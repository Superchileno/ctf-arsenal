#!/bin/bash
cd ~
objdump -d --start-address=0xffffffff816159c0 --stop-address=0xffffffff81615e40 /tmp/vmlinux.elf 2>/dev/null | sed -n '6,260p'
