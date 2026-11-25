#!/bin/bash
cd ~
for L in 8 9 10 11 12; do
  s=$(printf 'a%.0s' $(seq 1 $L))
  printf '%s\n' "$s" > in.txt
  echo "=== len=$L ==="
  gdb -q -batch -x gdb_trace.txt ./night_shift 2>/dev/null | grep '^IP' | tr '\n' ' '
  echo
done
