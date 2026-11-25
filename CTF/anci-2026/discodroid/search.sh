#!/bin/bash
UA="Mozilla/5.0"
echo "=== search: pipe_buf_get splice CVE ==="
timeout 15 curl -s "https://html.duckduckgo.com/html/?q=%22splice_pipe_to_pipe%22+%22pipe_buf_get%22+CVE" -A "$UA" | grep -oE 'result__a[^>]*>[^<]+' | head -12
echo
echo "=== search: CVE-2026-31507 ==="
timeout 15 curl -s "https://html.duckduckgo.com/html/?q=CVE-2026-31507+splice+double+free" -A "$UA" | grep -oE 'result__a[^>]*>[^<]+' | head -12
echo
echo "=== opencve 31507 ==="
timeout 20 curl -s "https://app.opencve.io/cve/CVE-2026-31507" -A "$UA" | sed 's/<[^>]*>//g' | grep -iE 'description|splice|pipe|fixed|5\.|6\.' | head -30
