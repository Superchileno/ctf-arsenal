#!/bin/bash
cd "$(dirname "$0")" || exit 1
gdb -q -batch ./chall \
  -ex "set pagination off" \
  -ex "run < ../crash_94.bin" \
  -ex "bt 20" \
  -ex "info registers rsp rbp rip" \
  -ex "x/6i \$rip-12" 2>&1 | tail -55
