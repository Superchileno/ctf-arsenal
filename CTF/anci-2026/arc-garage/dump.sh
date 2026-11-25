#!/bin/bash
cd "$(dirname "$0")/old-school-bins" || exit 1
objdump -d -M intel --no-show-raw-insn chall > dis.txt
readelf --debug-dump=info chall > dwarf.txt
readelf --debug-dump=decodedline chall > lines.txt
echo "dis lines: $(wc -l < dis.txt)  dwarf lines: $(wc -l < dwarf.txt)"
grep -n "prompt_edit_string\|read_line\|prompt_edit_lap_time\|fmt_rating" dwarf.txt | head -40
