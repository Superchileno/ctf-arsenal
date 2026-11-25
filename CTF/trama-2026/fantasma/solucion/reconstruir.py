#!/usr/bin/env python3
"""
Desafío «Registro Fantasma» — reconstrucción de la telemetría
============================================================

Cada petición lleva un trozo de la telemetría en `p`. Dos lecturas posibles:

  A) cada trozo es base64 de una porción de bytes del flujo deflate
     -> decodificar cada uno y concatenar bytes;
  B) el flujo deflate se codificó entero en base64 y se PARTIÓ el texto
     -> concatenar los textos y decodificar una sola vez.

Los trozos de 5 caracteres (no múltiplos de 4) solo tienen sentido en la
lectura B, así que esa es la buena; se prueban ambas por completitud.

Reglas del parte de turno:
  * el access.log es del backend, detrás del proxy: la IP no identifica la caja;
  * el proxy conoce el resultado real (REJECT/OK) y el orden (flow, seq);
  * el orden de aparición en disco no es la secuencia original.
"""
import base64
import csv
import re
import zlib
from pathlib import Path

W = Path("/mnt/c/Users/shapl/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/fantasma/work")

patron = re.compile(r'\[([^\]]+)\].*"GET /telemetry/sync\?rid=([^&"]+)&p=([^ "]+)')
eventos = {}
for linea in W.joinpath("access.log").read_text(errors="replace").splitlines():
    m = patron.search(linea)
    if m:
        _, rid, p = m.groups()
        eventos[rid] = p

filas = list(csv.DictReader(W.joinpath("proxy_trace.csv").open()))
print(f"telemetría: {len(eventos)} | proxy: {len(filas)}")


def inflar(datos: bytes) -> bytes:
    for wbits in (-15, 15, 47):
        try:
            return zlib.decompress(datos, wbits)
        except Exception:
            continue
    return b"<<no se pudo inflar>>"


def piezas(filtro):
    out = []
    for f in filas:
        if filtro(f) and f["request_id"] in eventos:
            out.append((f["flow"], int(f["seq"]), f["request_id"]))
    out.sort(key=lambda x: (x[0], x[1]))
    return out


def mostrar(etiqueta: str, filtro) -> None:
    ps = piezas(filtro)
    print(f"\n=== {etiqueta}: {len(ps)} piezas")
    for flow in sorted({p[0] for p in ps}):
        trozos = [p for p in ps if p[0] == flow]
        texto_b64 = "".join(eventos[p[2]] for p in trozos).replace("-", "+").replace("_", "/")
        try:
            datos = base64.b64decode(texto_b64 + "=" * (-len(texto_b64) % 4))
            leido = inflar(datos)
        except Exception as e:
            leido = f"<error {e}>".encode()
        print(f"--- {flow} ({len(trozos)} trozos): {leido.decode(errors='replace')[:400]}")
        if b"TRAMACTF" in leido:
            print("    >>> FLAG:", re.search(rb"TRAMACTF\{[^}]*\}", leido).group(0).decode())


mostrar("solo proxy_result=OK", lambda f: f["proxy_result"] == "OK")
mostrar("todas las filas", lambda f: True)
