#!/bin/bash
cd ~
echo "=== ops symbols ==="
nm /tmp/vmlinux.elf | grep -iE 'pipe_buf_ops|pipe_buf_confirm|anon_pipe_buf_ops|page_cache_pipe_buf_ops'
echo "=== dump ops structs ==="
python3 - <<'PY'
import subprocess, re
syms={}
out=subprocess.run(["nm","/tmp/vmlinux.elf"],capture_output=True,text=True).stdout
for line in out.splitlines():
    p=line.split()
    if len(p)==3: syms[p[2]]=int(p[0],16)
for n in ["anon_pipe_buf_ops","page_cache_pipe_buf_ops","default_pipe_buf_ops","packet_pipe_buf_ops"]:
    if n in syms:
        a=syms[n]
        print(n,hex(a))
        out=subprocess.run(["objdump","-s","--start-address=%d"%a,"--stop-address=%d"%(a+48),"/tmp/vmlinux.elf"],capture_output=True,text=True).stdout
        print(out)
PY
