#!/bin/bash
echo "=== version/config strings ==="
strings -n 8 /tmp/vmlinux | grep -m5 -E '^Linux version|CONFIG_|6\.[0-9]+\.[0-9]+' | head -20
echo "=== gcc/clang ==="
strings -n 10 /tmp/vmlinux | grep -m3 -i 'clang version'
echo "=== net ==="
timeout 10 curl -s "https://html.duckduckgo.com/html/?q=splice_pipe_to_pipe+pipe_buf_get+removed+CVE" -A "Mozilla/5.0" | grep -oE 'result__a[^>]*>[^<]+' | head -10
