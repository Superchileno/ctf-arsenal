#!/bin/bash
cd ~
printf 'aaaaaaaaa\n' > in.txt
gdb -q -batch -x gdb_trace.txt ./night_shift 2>/dev/null | grep '^IP' > trace_a.txt
printf 'nightgate\n' > in.txt
gdb -q -batch -x gdb_trace.txt ./night_shift 2>/dev/null | grep '^IP' > trace_n.txt
wc -l trace_a.txt trace_n.txt
echo "--- A (first 80) ---"; head -80 trace_a.txt
echo "--- N (first 80) ---"; head -80 trace_n.txt
