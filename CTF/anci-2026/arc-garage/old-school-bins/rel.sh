#!/bin/bash
cd "$(dirname "$0")" || exit 1
cat > /tmp/g2.gdb <<'EOF'
set pagination off
set confirm off
break *(main+0x32)
commands
silent
set $pie = (unsigned long)&garage - 0x54a0
set $car = *(unsigned long*)&garage
set $off = *(unsigned short*)($car-2)
set $idx = (unsigned)*(unsigned char*)($car-3) & 31
set $grp = $car - 16*$off - 16
set $meta = *(unsigned long*)$grp
printf "RESULT pie=%#lx car=%#lx off=%d idx=%d grp=%#lx meta=%#lx delta_meta_pie=%#lx delta_car_meta=%#lx\n", $pie, $car, $off, $idx, $grp, $meta, $meta-$pie, $meta-$car
quit
end
run < /dev/null
EOF
for mode in on off; do
  for i in 1 2 3; do
    if [ "$mode" = on ]; then
      gdb -q -batch -ex "set disable-randomization off" -x /tmp/g2.gdb ./chall 2>/dev/null | grep RESULT
    else
      gdb -q -batch -ex "set disable-randomization on" -x /tmp/g2.gdb ./chall 2>/dev/null | grep RESULT
    fi
  done
done
