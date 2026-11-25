#!/bin/bash
cd ~
run() {
  printf '%s\n' "$1" > in.txt
  out=$(gdb -q -batch -x gdb_trace.txt ./night_shift 2>/dev/null | grep '^IP' | tr '\n' ' ')
  n=$(echo $out | wc -w)
  echo "[$1] n=$n :: $out"
}
run anightgate
run xnightgate
run 0nightgate
run nnightgate
run nightgate0
run aaaaaaaaaa
