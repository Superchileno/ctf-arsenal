#!/bin/bash
set -x
sudo apt-get update -qq > /tmp/apt.log 2>&1
sudo apt-get install -y -qq gdb python3-pip >> /tmp/apt.log 2>&1
tail -3 /tmp/apt.log
which gdb
pip3 install --quiet --break-system-packages pwntools >> /tmp/pip.log 2>&1
tail -3 /tmp/pip.log
python3 -c "import pwn; print('pwntools', pwn.__version__)"
