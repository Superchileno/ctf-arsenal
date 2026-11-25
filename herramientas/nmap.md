# nmap — reconocimiento de red

> Autorizado solo sobre hosts en `scope.txt`. 200 ms entre requests por defecto.

## Descubrimiento

```bash
# Hosts vivos en la LAN
nmap -sn 10.0.0.0/24

# Ping sweep rápido sin DNS
nmap -sn -n --min-rate 500 10.0.0.0/24
```

## Puertos

```bash
# Top 1000 + versiones + scripts por defecto
nmap -sC -sV -oA work/nmap-inicial <host>

# Todos los puertos, rápido (útil en CTF)
nmap -p- --min-rate 2000 -T4 -oN work/nmap-all <host>

# Luego versiones sobre los abiertos
nmap -sV -sC -p 22,80,443,8080 -oA work/nmap-detalle <host>
```

## UDP (no olvidar)

```bash
sudo nmap -sU --top-ports 50 -sV <host>
```

## Web / TLS

```bash
nmap --script http-title,http-headers,http-enum -p 80,443 <host>
nmap --script ssl-enum-ciphers -p 443 <host>
nmap --script smb-vuln* -p 445 <host>
```

## Evasión (solo si el alcance lo permite)

```bash
nmap -sS -f --data-length 24 -D RND:10 <host>
nmap --source-port 53 <host>
```

## Lectura de resultados

| Puerto | Siguiente paso |
|---|---|
| 22 | usuarios válidos, claves débiles (`hydra` solo si está autorizado) |
| 80/443 | `whatweb`, `ffuf`, `nikto`, `nuclei` |
| 139/445 | `smbclient -L`, `enum4linux-ng`, `netexec smb` |
| 389/636 | `ldapsearch`, `netexec ldap` |
| 3306/5432 | credenciales por defecto, solo lectura |
| 8080/8443 | misma batería web que 80/443 |

## Guardrails

- `-T4` y `--min-rate` altos solo en CTF o con autorización explícita.
- Nunca `--script` con categorías `dos`, `intrusive` o `exploit` sin permiso.
- Registrar el comando exacto en `CONTEXTO.md` del objetivo.
