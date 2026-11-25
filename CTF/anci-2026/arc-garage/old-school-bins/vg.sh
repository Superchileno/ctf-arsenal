#!/bin/bash
sudo apt-get install -y -qq valgrind >> /tmp/apt.log 2>&1
cd "$(dirname "$0")/old-school-bins" 2>/dev/null || cd "$(dirname "$0")"
printf '1\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\n\n\n100\n\n\n\n\n\n\n5\n' > /tmp/vg.txt
valgrind --error-exitcode=99 --leak-check=no ./chall < /tmp/vg.txt > /tmp/vg.out 2> /tmp/vg.err
echo "rc=$?"
tail -40 /tmp/vg.err
