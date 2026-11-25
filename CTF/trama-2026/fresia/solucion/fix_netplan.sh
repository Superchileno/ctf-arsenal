#!/bin/bash
# Corrige el netplan de la guest Fresia: el OVA declara "enp0s3" (nombre de VirtualBox)
# pero VMware expone la NIC con otro nombre (p. ej. ens33), por lo que nunca aplica DHCP.
#
# Añade /etc/netplan/99-ctf-any.yaml con match por patrón y reescribe el disco.
# Uso: ./fix_netplan.sh [raw]
set -euo pipefail

IMG="${1:-/root/fresia.raw}"
VMDK="/mnt/c/VMs/fresia/Fresia/Fresia-disk1.vmdk"
MNT=/mnt/fresia

mountpoint -q "$MNT" || {
  L=$(losetup -f --show -P "$IMG")
  echo "loop=$L"
  mount -o ro "${L}p2" "$MNT" 2>/dev/null || mount -o ro "${L}p1" "$MNT"
}

mount -o remount,rw "$MNT"
cat > "$MNT/etc/netplan/99-ctf-any.yaml" <<'EOF'
network:
  version: 2
  ethernets:
    ctf-all:
      match:
        name: "en*"
      dhcp4: true
      dhcp6: false
      optional: true
EOF
chmod 600 "$MNT/etc/netplan/99-ctf-any.yaml"
ls -la "$MNT/etc/netplan/"
sync
umount "$MNT"
losetup -D

echo "[*] reempaquetando raw -> vmdk (se conserva el original en .orig)"
[ -f "$VMDK.orig" ] || cp -n "$VMDK" "$VMDK.orig"
rm -f "$VMDK"
qemu-img convert -f raw -O vmdk -o subformat=monolithicSparse "$IMG" "$VMDK"
qemu-img info "$VMDK" | head -6
echo "[*] listo: arranca la VM y debería obtener IP por DHCP"
