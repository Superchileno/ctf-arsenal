#!/usr/bin/env python3
"""CDM CTF 2026-11-13 - NexoDesk: asistente corrupto (203.0.113.10:8081)

Camino:
1. El HTML trae una nota ofuscada (data-nd-obfuscated): Base64 + XOR 0x39.
   -> "NEXODESK RECOVERY RECORD: /api/assistant/attestation contains the
       verified recovery token. Status: complete"
2. /api/assistant/attestation devuelve un artefacto {"codec":"xor-b64","key":90,
   "payload":"..."} -> Base64 + XOR 90 (0x5A) = token de recuperacion.
3. El token es la bandera (vive fuera del contexto del modelo).

Uso: python decode.py [host:puerto]
"""
from __future__ import annotations

import base64
import json
import re
import sys
import urllib.request

HOST = sys.argv[1] if len(sys.argv) > 1 else "203.0.113.10:8081"
BASE = "http://" + HOST


def get(path: str) -> str:
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def xor_b64(payload: str, key: int) -> str:
    payload += "=" * (-len(payload) % 4)
    return bytes(b ^ key for b in base64.b64decode(payload)).decode("utf-8", "replace")


def main() -> int:
    # 1) Nota ofuscada del HTML
    for blob in re.findall(r'data-nd-obfuscated="([^"]+)"', get("/")):
        print("[*] nota:", xor_b64(blob, 0x39))

    # 2) Artefacto de attestation
    artefacto = json.loads(get("/api/assistant/attestation"))
    print(f"[*] artefacto: {artefacto}")
    token = xor_b64(artefacto["payload"], artefacto["key"])
    print(f"[+] RECOVERY TOKEN / FLAG: {token}")

    with open("flag.txt", "w", encoding="utf-8") as fh:
        fh.write(token + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
