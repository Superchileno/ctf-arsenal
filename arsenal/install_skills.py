#!/usr/bin/env python3
"""Instala las skills del repositorio en un directorio de skills de agente.

Uso:
    python arsenal/install_skills.py --dest ~/.agents/skills
    python arsenal/install_skills.py --only ctf-web,exploiting-jwt-algorithm-confusion-attack
    python arsenal/install_skills.py --list
    python arsenal/install_skills.py --dry-run

Cada skill se materializa como <dest>/<id>/ con su arbol completo
(SKILL.md, references, scripts, assets).
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(BASE, "skills")


def listar() -> list[str]:
    if not os.path.isdir(SKILLS):
        return []
    return sorted(
        d for d in os.listdir(SKILLS)
        if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md"))
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Instala skills en el directorio de un agente")
    ap.add_argument("--dest", default=os.path.expanduser("~/.agents/skills"),
                    help="directorio destino (default: ~/.agents/skills)")
    ap.add_argument("--only", default="", help="lista separada por comas de ids")
    ap.add_argument("--list", action="store_true", help="lista las skills disponibles")
    ap.add_argument("--dry-run", action="store_true", help="no copia, solo informa")
    ap.add_argument("--force", action="store_true", help="sobrescribe destinos existentes")
    args = ap.parse_args()

    disponibles = listar()
    if args.list:
        print(f"{len(disponibles)} skills disponibles en {SKILLS}\n")
        for s in disponibles:
            print(f"  {s}")
        return 0

    if not disponibles:
        print(f"[!] no hay skills en {SKILLS}", file=sys.stderr)
        return 1

    if args.only.strip():
        pedidas = [s.strip() for s in args.only.split(",") if s.strip()]
        desconocidas = [s for s in pedidas if s not in disponibles]
        if desconocidas:
            print(f"[!] no existen: {', '.join(desconocidas)}", file=sys.stderr)
            return 2
        seleccion = pedidas
    else:
        seleccion = disponibles

    os.makedirs(args.dest, exist_ok=True)
    copiadas = 0
    for sid in seleccion:
        origen = os.path.join(SKILLS, sid)
        destino = os.path.join(args.dest, sid)
        if os.path.exists(destino) and not args.force:
            print(f"  = {sid} (ya existe, usa --force para sobrescribir)")
            continue
        print(f"  + {sid} -> {destino}")
        if not args.dry_run:
            if os.path.exists(destino):
                shutil.rmtree(destino)
            shutil.copytree(origen, destino)
        copiadas += 1

    print(f"\n{copiadas} skill(s) {'simuladas' if args.dry_run else 'instaladas'} en {args.dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
