#!/bin/bash
cd "$(dirname "$0")/old-school-bins" || exit 1
readelf -SW chall | grep -E 'debug|symtab|strtab'
echo "=== tail dwarf ==="
tail -20 dwarf.txt
echo "=== try objdump dwarf info ==="
objdump --dwarf=info chall 2>&1 | grep -c . 
objdump --dwarf=info chall 2>&1 | grep -n -A40 'DW_AT_name.*chall.c' | head -120
