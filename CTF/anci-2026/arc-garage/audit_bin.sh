#!/bin/bash
cd "$(dirname "$0")/old-school-bins" || exit 1
echo "=== binary strings: AI-ish ==="
strings -a -n 3 chall | grep -Ei -w 'ai|agent|assistant|llm|gpt|ignore|instruction|prompt|curl|bit\.ly|http|human|claude|chatgpt|opencode' || echo "(none)"
echo "=== binary strings: urls ==="
strings -a -n 5 chall | grep -Ei 'https?://|bit\.ly|\.com|\.net|\.org' || echo "(none)"
echo "=== libc strings: AI-ish ==="
strings -a -n 5 libc.so | grep -Ei -w 'ai|agent|assistant|llm|gpt|ignore|instruction|prompt|curl|bit\.ly' || echo "(none)"
echo "=== flag.txt hex ==="
xxd flag.txt
echo "=== Dockerfile hex ==="
xxd Dockerfile
echo "=== file hashes ==="
sha256sum chall libc.so flag.txt Dockerfile
