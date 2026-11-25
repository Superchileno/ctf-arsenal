#!/bin/bash
cd "$(dirname "$0")/old-school-bins" || exit 1
echo "=== direct run ==="
./chall </dev/null 2>&1 | head -5
echo "rc=$?"
echo "=== run via provided libc.so as loader ==="
printf '5\n' | ./libc.so ./chall 2>&1 | head -12
echo "rc=$?"
echo "=== file permissions ==="
ls -l chall libc.so
