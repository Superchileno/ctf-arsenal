#!/bin/bash
cd ~
for c in {a..z} {0..9}; do
  s="nightgate$c"
  out=$(printf '%s\n' "$s" | ./night_shift 2>/dev/null)
  if echo "$out" | grep -q 'flag{'; then
    echo "FOUND [$s] -> $out"
  fi
done
echo done
