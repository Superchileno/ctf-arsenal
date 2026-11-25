# Entorno — Kali Linux en WSL2

## Invocación

```powershell
# Comando simple
wsl -d kali-linux -- bash -lc "nmap -sV 10.0.0.10"

# Con workdir
wsl -d kali-linux --cd /mnt/c/Users/<usuario>/ruta -- bash -lc "ls -la"
```

Scripts con bucles, comillas o `$variables`: escribir el `.sh` en
`%TEMP%\opencode\` y ejecutarlo desde WSL para evitar
el mangleo de PowerShell.

```powershell
wsl -d kali-linux -- bash "$(wslpath -u '%TEMP%\opencode\tarea.sh')"
```

## Estado y red

```bash
ip -br a             # interfaz y IP
ip route             # gateway
wsl -l -v            # desde PowerShell: distro y estado
```

Kali está en modo **mirrored**: comparte la LAN del host, así que alcanza
directamente `192.168.x.x` y `10.x.x.x`.

## Rutas entre sistemas

| Desde | Hacia Windows | Hacia Kali |
|---|---|---|
| Kali | `/mnt/c/...` | `/home/<usuario>/...` |
| Windows | `C:\...` | `\\wsl$\kali-linux\home\<usuario>\...` |

## Instalar herramientas

```bash
# Como root sin contraseña
wsl -d kali-linux -u root -- bash -lc "apt update && apt install -y <paquete>"

# Dentro de la distro
sudo apt install -y <paquete>
```

Conjuntos útiles por categoría:

| Categoría | Paquetes |
|---|---|
| Web | `ffuf gobuster feroxbuster nikto sqlmap nuclei whatweb wafw00f dalfox arjun commix` |
| Red | `nmap masscan tshark zeek netdiscover` |
| Pwn/reversing | `gdb radare2 ropper python3-pwntools binutils patchelf` |
| Forense | `sleuthkit autopsy volatility3 plaso foremost binwalk exiftool yara` |
| Cracking | `john hashcat hydra medusa hashid cewl crunch` |
| AD | `netexec impacket-scripts enum4linux-ng smbclient evil-winrm certipy bloodhound.py` |
| Estego/audio | `zsteg steghide pngcheck zbar-tools sox ffmpeg` |
| Python | `pip install pwntools pycryptodome gmpy2 pyzbar` |

## Git

`git` no está en el PATH de Windows. Usar:

```powershell
wsl -d kali-linux -- bash -lc "cd '/mnt/c/Users/<usuario>/OneDrive - <organizacion>/Agentes IA/CTF' && git status"
```

o `C:\Program Files\Git\bin\git.exe` si está instalado.

## Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `command not found` | tool no instalada | `apt install` (ver arriba) |
| Permisos en `/mnt/c` | montaje Windows | usar `work\` en la copia de WSL o `cp` primero |
| `sudo` pide contraseña | política del entorno | pedir la contraseña al usuario en la sesión |
| Red aislada | WSL NAT | relay TCP en espacio de usuario (`socat`) |
| Rutas con espacios | OneDrive | entrecomillar y usar `--cd` |
