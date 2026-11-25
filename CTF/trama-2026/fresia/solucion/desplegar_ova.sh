#!/bin/bash
# Despliegue del laboratorio Fresia (OVA VirtualBox -> VMware Workstation)
# Uso: ./desplegar_ova.sh <ruta al fresia.ova> [carpeta destino VM]
set -euo pipefail

OVA="${1:?uso: $0 <fresia.ova> [destino]}"
DEST="${2:-/mnt/c/VMs/fresia}"
OVFTOOL="/mnt/c/Program Files (x86)/VMware/VMware Workstation/OVFTool/ovftool.exe"
VMRUN="/mnt/c/Program Files (x86)/VMware/VMware Workstation/vmrun.exe"

echo "[1] verificando SHA256 del OVA"
if [ -f "$(dirname "$OVA")/fresia.ova.sha256" ]; then
  ( cd "$(dirname "$OVA")" && sha256sum -c fresia.ova.sha256 )
fi

echo "[2] importando con ovftool (modo monolithicSparse)"
mkdir -p "$DEST"
"$OVFTOOL" --lax --allowExtraConfig --diskMode=monolithicSparse -dm=monolithicSparse \
  "$OVA" "$DEST/Fresia/Fresia.vmx"

VMX="$DEST/Fresia/Fresia.vmx"
echo "[3] ajustando VMX: NIC en NAT + VNC en 5901"
cp -n "$VMX" "$VMX.orig.bak"
python3 - "$VMX" <<'PY'
import sys, re, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding='utf-8', errors='replace')
t = re.sub(r'ethernet0\.connectionType = "[^"]*"', 'ethernet0.connectionType = "nat"', t)
t = re.sub(r'ethernet0\.bridgedTo = "[^"]*"\r?\n', '', t)
extra = ('\nRemoteDisplay.vnc.enabled = "TRUE"\n'
         'RemoteDisplay.vnc.port = "5901"\n'
         'RemoteDisplay.vnc.password = "trama2026"\n'
         'bios.bootDelay = "6000"\n')
if 'RemoteDisplay.vnc.enabled' not in t:
    t += extra
p.write_text(t, encoding='utf-8')
print("VMX actualizado")
PY

echo "[4] arrancando en modo headless"
"$VMRUN" -T ws start "$VMX" nogui
sleep 45
echo "[5] IP asignada por vmnetdhcp (busca el MAC de la VM):"
grep -A5 "fresia" "/mnt/c/ProgramData/VMware/vmnetdhcp.leases" | tail -20 || true
echo
echo "Siguiente paso: solucion/fix_netplan.sh (la guest solo declara enp0s3 y VMware le da otro nombre)"
