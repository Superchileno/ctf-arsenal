#!/bin/bash
set -e
D="/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/El_Ingrediente_Secreto_de_Vlad/work"
mkdir -p "$D"
UA="User-Agent: ctf-research"
API="https://api.github.com/repos/VladElVeg666/Mis_Recetas_Favoritas"

echo "[i] perfil"
curl -s -H "$UA" https://api.github.com/users/VladElVeg666 -o "$D/usuario.json"
python3 -c "import json;d=json.load(open('$D/usuario.json'));print('  login:',d['login'],'| name:',d['name'],'| bio:',d['bio'],'| repos:',d['public_repos'])"

echo "[i] repositorios"
curl -s -H "$UA" https://api.github.com/users/VladElVeg666/repos -o "$D/repos.json"
python3 -c "import json;[print('  ',r['full_name'],'-',r['description']) for r in json.load(open('$D/repos.json'))]"

echo "[i] commits"
curl -s -H "$UA" "$API/commits?per_page=100" -o "$D/commits.json"
python3 -c "import json;[print('  ',c['sha'][:8],c['commit']['message'].splitlines()[0],c['commit']['author']['date']) for c in json.load(open('$D/commits.json'))]"

echo "[i] README por commit"
for sha in $(python3 -c "import json;[print(c['sha']) for c in json.load(open('$D/commits.json'))]"); do
  curl -s "https://raw.githubusercontent.com/VladElVeg666/Mis_Recetas_Favoritas/$sha/README.md" -o "$D/README_${sha:0:8}.md"
  echo "  guardado README_${sha:0:8}.md ($(wc -c < "$D/README_${sha:0:8}.md") bytes)"
done
curl -s "https://raw.githubusercontent.com/VladElVeg666/Mis_Recetas_Favoritas/main/README.md" -o "$D/README_main.md"

echo
echo "[+] flags encontradas en el historial:"
grep -ho "TRAMACTF{[^}]*}" "$D"/README_*.md | sort | uniq -c
