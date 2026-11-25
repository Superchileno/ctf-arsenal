#!/bin/bash
cd "$(dirname "$0")/old-school-bins" || exit 1
echo "=== pwd ==="; pwd
echo "=== program headers ==="
readelf -lW chall | sed -n '1,45p'
echo "=== functions ==="
readelf -sW chall | awk '$4=="FUNC" {print $2, $3, $8}' | sort
echo "=== strings (interesting) ==="
strings -a -n 5 chall | grep -Ei 'flag|token|win|shell|model|team|driver|engine|speed|lap|tune|name|%|buffer' | head -60
