#!/bin/bash
D="/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ANCI/discodroid/extracted/discodroid"
cd ~
python3 - <<'EOF'
d=open("/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ANCI/discodroid/extracted/discodroid/Image","rb").read()
i=d.find(b"\x1f\x8b\x08")
print("gzip offset",hex(i))
open("/tmp/kernel.gz","wb").write(d[i:])
EOF
zcat /tmp/kernel.gz > /tmp/vmlinux 2>/dev/null || true
ls -l /tmp/vmlinux
file /tmp/vmlinux
readelf -h /tmp/vmlinux 2>/dev/null | head -5
echo "--- symbols ---"
readelf -sW /tmp/vmlinux 2>/dev/null | grep -iE 'splice_pipe_to_pipe|iter_file_splice|copy_page_to_iter_pipe|push_pipe' | head
