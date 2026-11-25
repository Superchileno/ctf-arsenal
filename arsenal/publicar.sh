#!/usr/bin/env bash
# Publica el repositorio en GitHub.
#
# Uso:
#   bash arsenal/publicar.sh            # intenta push al remote configurado
#   bash arsenal/publicar.sh --check    # solo verifica estado y credenciales
#   TOKEN=ghp_xxx bash arsenal/publicar.sh   # usa un token personal puntual
#
# Requisitos: git. Para crear el repositorio automaticamente hace falta `gh`
# autenticado (gh auth login) o haberlo creado antes en la web.

set -u
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ" || exit 1

REMOTE_URL="https://github.com/Superchileno/ctf-arsenal.git"
REPO="Superchileno/ctf-arsenal"
MODO="${1:-}"

echo "== Repositorio: $RAIZ"
echo "== Rama: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'sin git')"
echo "== Commits: $(git rev-list --count HEAD 2>/dev/null || echo 0)"

if ! git remote get-url origin >/dev/null 2>&1; then
    echo "== Configurando remote origin"
    git remote add origin "$REMOTE_URL"
fi

if [ -n "${TOKEN:-}" ]; then
    git remote set-url origin "https://${TOKEN}@github.com/${REPO}.git"
    echo "== Remote reescrito con el token entregado (no se imprime)"
fi

if [ "$MODO" = "--check" ]; then
    echo "== Estado local"
    git status --short | head -10
    echo
    if command -v gh >/dev/null 2>&1; then
        echo "== gh disponible: $(gh --version | head -1)"
        gh auth status 2>&1 | head -5
    else
        echo "== gh NO instalado"
    fi
    echo
    echo "Para publicar:"
    echo "  A) gh auth login && bash arsenal/publicar.sh --crear"
    echo "  B) crear el repo en la web y ejecutar: bash arsenal/publicar.sh"
    exit 0
fi

if [ "$MODO" = "--crear" ]; then
    if ! command -v gh >/dev/null 2>&1; then
        echo "[!] gh no esta instalado: sudo apt install -y gh && gh auth login"
        exit 1
    fi
    gh repo create "$REPO" --public --source=. --remote=origin --push
    exit $?
fi

echo "== Push"
GIT_TERMINAL_PROMPT=0 git push -u origin main
ESTADO=$?
if [ $ESTADO -ne 0 ]; then
    echo
    echo "[!] Push fallido (codigo $ESTADO). Causas habituales:"
    echo "    - el repositorio no existe todavia en GitHub"
    echo "    - faltan credenciales (token o gh auth login)"
    echo
    echo "Opciones:"
    echo "    1) gh auth login && bash arsenal/publicar.sh --crear"
    echo "    2) TOKEN=ghp_xxx bash arsenal/publicar.sh"
    echo "    3) Crear el repo en la web y repetir: bash arsenal/publicar.sh"
fi
exit $ESTADO
