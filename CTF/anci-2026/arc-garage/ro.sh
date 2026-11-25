#!/bin/bash
cd "$(dirname "$0")/old-school-bins" || exit 1
objdump -s -j .rodata chall | head -220
