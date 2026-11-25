#!/bin/bash
cd "$(dirname "$0")" || exit 1
gdb -q -batch ./chall \
  -ex "set pagination off" \
  -ex "run < ../min_crash.bin" \
  -ex "bt 20" \
  -ex "info registers rsp rbp rip rax rdi rsi" \
  -ex "x/10i \$rip-20" 2>&1 | tail -40
