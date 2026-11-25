#!/usr/bin/env bash
# Crea el repositorio en GitHub (si no existe) y publica el contenido local.
#
# Uso:
#   TOKEN=ghp_xxx bash arsenal/crear_repo.sh
#
# El token se usa solo para esta ejecución: al terminar, el remote queda limpio
# (sin credenciales embebidas). Revoca el token en GitHub cuando ya no lo uses.

set -u
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ" || exit 1

TOKEN="${TOKEN:-}"
USUARIO="${USUARIO:-Superchileno}"
REPO="${REPO:-ctf-arsenal}"
DESCRIPCION="CTF arsenal: skills, writeups saneados, plantillas y cheatsheets (70% CTF / 30% pentesting)"

if [ -z "$TOKEN" ]; then
    echo "[!] Falta el token: TOKEN=ghp_xxx bash arsenal/crear_repo.sh"
    exit 1
fi

API="https://api.github.com"
REMOTE_LIMPIO="https://github.com/${USUARIO}/${REPO}.git"
REMOTE_TOKEN="https://x-access-token:${TOKEN}@github.com/${USUARIO}/${REPO}.git"

echo "== 1/4 Verificando si el repositorio existe"
CODIGO=$(curl -s -o /tmp/repo_info.json -w '%{http_code}' \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    "${API}/repos/${USUARIO}/${REPO}")

if [ "$CODIGO" = "200" ]; then
    echo "   ya existe: ${USUARIO}/${REPO}"
elif [ "$CODIGO" = "404" ]; then
    echo "   no existe, creando..."
    CREACION=$(curl -s -o /tmp/repo_new.json -w '%{http_code}' -X POST \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Accept: application/vnd.github+json" \
        "${API}/user/repos" \
        -d "{\"name\":\"${REPO}\",\"description\":\"${DESCRIPCION}\",\"private\":false,\"has_issues\":true,\"has_wiki\":false}")

    if [ "$CREACION" = "201" ]; then
        echo "   creado: https://github.com/${USUARIO}/${REPO}"
    else
        echo "[!] No se pudo crear (HTTP ${CREACION}). Revisa los permisos del token (Contents: Read and write / Administration)."
        head -c 400 /tmp/repo_new.json; echo
        exit 2
    fi
else
    echo "[!] Respuesta inesperada de GitHub (HTTP ${CODIGO}). ¿Token válido y con scope repo?"
    head -c 400 /tmp/repo_info.json; echo
    exit 3
fi

echo "== 2/4 Preparando remote con el token (temporal)"
git remote remove origin >/dev/null 2>&1
git remote add origin "$REMOTE_TOKEN"

echo "== 3/4 Push de la rama main"
GIT_TERMINAL_PROMPT=0 git push -u origin main
ESTADO=$?

echo "== 4/4 Limpiando el token del remote"
git remote set-url origin "$REMOTE_LIMPIO"
git remote -v | head -1

rm -f /tmp/repo_info.json /tmp/repo_new.json

if [ $ESTADO -eq 0 ]; then
    echo
    echo "OK: publicado en https://github.com/${USUARIO}/${REPO}"
    echo "Recuerda revocar el token en https://github.com/settings/tokens"
else
    echo "[!] El push falló (código ${ESTADO})."
fi
exit $ESTADO
