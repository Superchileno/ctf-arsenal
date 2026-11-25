#!/bin/bash
cd ~
for L in $(seq 1 20); do
  s=$(printf 'a%.0s' $(seq 1 $L))
  printf '%s\n' "$s" > in.txt
  n=$(gdb -q -batch -x gdb_trace.txt ./night_shift 2>/dev/null | grep -c '^IP')
  last=$(gdb -q -batch -x gdb_trace.txt ./night_shift 2>/dev/null | grep '^IP' | tail -2 | tr '\n' ' ')
  echo "len=$L instr=$n tail=$last"
done
