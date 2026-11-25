#!/bin/bash
cd ~
for s in aaaaaaaaa bbbbbbbbb nightgate nnngggggg nnnnnnnnn aaaaaaaa aaaaaaaaaa n nnnnnnnn; do
  printf '%s\n' "$s" > in.txt
  echo -n "$s -> "
  gdb -q -batch -x gdb_end.txt ./night_shift 2>/dev/null | grep FINAL
done
