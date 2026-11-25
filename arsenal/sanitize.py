#!/usr/bin/env python3
"""Saneador de contenido antes de publicar.

Detecta (y opcionalmente reemplaza) datos que no deben salir del entorno local:
flags, IPv4, correos, rutas con nombre de usuario y hosts de plataformas de CTF.

Uso:
    python arsenal/sanitize.py --path docs/ --check
    python arsenal/sanitize.py --path reto.md --fix --report work/saneo.md
    python arsenal/sanitize.py --path . --ext .md,.py --check

Codigos de salida: 0 sin hallazgos, 1 hallazgos (modo --check), 2 error.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter

# (regex, reemplazo, etiqueta)
REGLAS = [
    # Flags: prefijo identificador + llaves, evitando f-strings y literales cortos
    (r"\b(?!(?:f|r|b|u|if|for|while|print|dict|set|list|tuple|format|str|repr|len"
     r"|json|os|sys|self|cls|item|obj|data|res|ctx|app|req|resp|args|kwargs"
     r"|config|env|var|val|key|name|path)\b)"
     r"([A-Za-z][A-Za-z0-9_]{1,20})\{(?!ejemplo\})([^{}\n]{6,200})\}",
     r"flag{ejemplo}", "flag"),
    # Correos
    (r"\b(?!usuario@example\.com\b)[A-Za-z0-9._%+-]+@(?!example\.com\b)"
     r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
     "usuario@example.com", "email"),
    # IPv4 publicas (deja 10.x, 192.168.x, 127.x, 172.16-31.x)
    (r"\b(?!10\.)(?!192\.168\.)(?!127\.)(?!172\.(?:1[6-9]|2\d|3[01])\.)"
     r"(?!203\.0\.113\.)(?!198\.51\.100\.)(?!0\.0\.0\.0)(?!169\.254\.)"
     r"(?:\d{1,3}\.){3}\d{1,3}\b",
     "203.0.113.10", "ip"),
    # Rutas Windows con usuario (el reemplazo es literal: se aplica vía función)
    (r"[A-Za-z]:\\\\?Users\\\\?[^\\\\/\s\"'<>]+",
     r"C:\Users\<usuario>", "ruta"),
    # Rutas Linux con usuario
    (r"/home/(?!<usuario>|ctf\b|user\b|ubuntu\b|root\b|node\b|app\b|kali\b)"
     r"[A-Za-z0-9._-]+",
     "/home/<usuario>", "ruta"),
    # Hosts de plataformas de CTF conocidas
    (r"\b[a-z0-9-]+\.(?:chals\.io|cloud\.chals\.io|campodemarte\.cl|hackrocks\.com)\b",
     "<host>", "host"),
]

EXCLUIR_DIRS = {"backups", "work", "flags", "evidence", ".git", "__pycache__", "node_modules"}
EXCLUIR_EXT = {".png", ".jpg", ".jpeg", ".gif", ".zip", ".gz", ".pcap", ".pcapng",
               ".ova", ".vmdk", ".iso", ".pyc", ".so", ".elf", ".bin", ".wav", ".mp3"}

# Palabras que delatan un f-string o una variable, no una flag
CONTENIDO_NO_FLAG = ("(", ")", "'", '"', "{", "}", "[", "]", "=", ".")


def es_flag_valida(m: "re.Match[str]") -> bool:
    """Descarta f-strings y placeholders que solo parecen flags."""
    prefijo = m.group(1)
    contenido = m.group(2)
    if prefijo.endswith("_"):
        return False
    if any(c in contenido for c in CONTENIDO_NO_FLAG):
        return False
    if contenido.lower() in {"ejemplo", "placeholder", "xxxxx", "aaaaa",
                             "payload", "etiqueta", "timestamp", "value",
                             "target", "visitados", "ioc_type"}:
        return False
    return True


VALIDADORES = {"flag": es_flag_valida}


def iterar_archivos(path: str, exts: set[str]):
    if os.path.isfile(path):
        yield path
        return
    for raiz, dirs, archivos in os.walk(path):
        dirs[:] = [d for d in dirs if d not in EXCLUIR_DIRS]
        for a in archivos:
            ext = os.path.splitext(a)[1].lower()
            if ext in EXCLUIR_EXT:
                continue
            if exts and ext not in exts:
                continue
            yield os.path.join(raiz, a)


def main() -> int:
    ap = argparse.ArgumentParser(description="Saneador de contenido para publicar")
    ap.add_argument("--path", required=True, help="archivo o carpeta a revisar")
    ap.add_argument("--ext", default="", help="extensiones a incluir, p. ej. .md,.py")
    ap.add_argument("--check", action="store_true", help="solo informa; no modifica")
    ap.add_argument("--fix", action="store_true", help="aplica los reemplazos")
    ap.add_argument("--report", default="", help="archivo donde dejar el informe")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        print(f"[!] no existe: {args.path}", file=sys.stderr)
        return 2

    exts = {e.strip().lower() for e in args.ext.split(",") if e.strip()}
    contadores: Counter = Counter()
    detalles: list[str] = []
    total_archivos = 0

    for ruta in iterar_archivos(args.path, exts):
        try:
            with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
                original = fh.read()
        except OSError:
            continue

        actual = original
        hallazgos_archivo = []
        for patron, reemplazo, etiqueta in REGLAS:
            validador = VALIDADORES.get(etiqueta)

            def rep(m, _r=reemplazo, _v=validador):
                return _r if (_v is None or _v(m)) else m.group(0)

            coincidencias = [m for m in re.finditer(patron, actual)
                             if validador is None or validador(m)]
            if not coincidencias:
                continue
            contadores[etiqueta] += len(coincidencias)
            for m in coincidencias[:5]:
                linea = actual[:m.start()].count("\n") + 1
                muestra = m.group(0)[:60].replace("\n", " ")
                hallazgos_archivo.append(f"    L{linea} [{etiqueta}] {muestra}")
            if args.fix:
                actual = re.sub(patron, rep, actual)

        if hallazgos_archivo:
            total_archivos += 1
            detalles.append(f"\n  {ruta}")
            detalles.extend(hallazgos_archivo)
            if args.fix and actual != original:
                with open(ruta, "w", encoding="utf-8", newline="") as fh:
                    fh.write(actual)

    modo = "CORREGIDO" if args.fix else "DETECTADO"
    print(f"[{modo}] {total_archivos} archivo(s) con hallazgos en {args.path}")
    if contadores:
        print("  resumen: " + ", ".join(f"{k}={v}" for k, v in sorted(contadores.items())))
    for linea in detalles:
        print(linea)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(f"# Informe de saneamiento\n\n- Ruta: {args.path}\n")
            fh.write(f"- Modo: {'fix' if args.fix else 'check'}\n")
            fh.write(f"- Archivos con hallazgos: {total_archivos}\n\n")
            fh.write("## Resumen\n\n")
            for k, v in sorted(contadores.items()):
                fh.write(f"- {k}: {v}\n")
            fh.write("\n## Detalle\n")
            fh.write("\n".join(detalles) + "\n")
        print(f"  informe: {args.report}")

    if args.check and total_archivos:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
