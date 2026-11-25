#!/bin/bash
cd ~
export PATH="$HOME/.local/bin:$PATH"
vmlinux-to-elf /tmp/vmlinux /tmp/vmlinux.elf 2>&1 | tail -5
ls -l /tmp/vmlinux.elf
echo "--- symbols of interest ---"
readelf -sW /tmp/vmlinux.elf 2>/dev/null | grep -iE 'splice_pipe_to_pipe|copy_page_to_iter_pipe|push_pipe|do_splice|iter_file_splice_write|link_pipe' | head
