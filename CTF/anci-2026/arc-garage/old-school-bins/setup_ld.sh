#!/bin/bash
cd "$(dirname "$0")" || exit 1
sudo ln -sf "$PWD/libc.so" /lib/ld-musl-x86_64.so.1
./chall <<< "5" | head -3
echo "direct rc=$?"
