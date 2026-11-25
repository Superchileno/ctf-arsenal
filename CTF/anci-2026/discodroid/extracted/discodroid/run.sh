#!/bin/sh

exec qemu-system-x86_64 \
    -cpu qemu64,+smep,+smap \
    -m 256M \
    -kernel Image \
    -initrd rootfs.cpio \
    -drive file=flag.txt,format=raw,if=none,id=flagdisk \
    -device virtio-blk-pci,drive=flagdisk \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -smp 2 \
    -nic none \
    -append "rdinit=/init console=ttyS0 kaslr pti=on loglevel=0 oops=panic panic=-1"
