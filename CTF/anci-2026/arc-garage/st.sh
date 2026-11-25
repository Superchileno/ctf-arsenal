#!/bin/bash
cd "$(dirname "$0")/old-school-bins" || exit 1
echo "=== strings with offsets (>=0x3000) ==="
strings -a -t x chall | awk '$1>="3000"'
echo "=== symbols all ==="
readelf -sW chall | awk '{print $2, $3, $4, $8}' | sort
