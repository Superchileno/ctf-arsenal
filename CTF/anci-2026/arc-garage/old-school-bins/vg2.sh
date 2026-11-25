#!/bin/bash
cd "$(dirname "$0")" || exit 1
python3 battery2.py > /tmp/bat2.txt
wc -l /tmp/bat2.txt
valgrind --error-exitcode=99 --leak-check=no --track-origins=no ./chall < /tmp/bat2.txt > /tmp/bat2.out 2> /tmp/bat2.err
echo "rc=$?"
grep -E "Invalid|ERROR SUMMARY|Process terminating" /tmp/bat2.err | sort | uniq -c | head -40
echo "--- first error context ---"
grep -n -m1 -A12 "Invalid" /tmp/bat2.err
