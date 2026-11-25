#!/bin/bash
cd "$(dirname "$0")" || exit 1
python3 gen_poc.py > /tmp/poc.txt
gdb -q -batch -ex "set disable-randomization off" -x hmap.py ./chall 2>/dev/null | sed -n '/^count/,$p' | head -120
