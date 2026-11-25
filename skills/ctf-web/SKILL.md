---
name: ctf-web
description: 'Explotación web de CTF: SQLi (UNION, blind, time-based, error-based y bypass de
  WAF), XSS y bypass de CSP, SSTI, SSRF con callbacks, XXE, deserialización insegura, fallos de
  JWT/OAuth/SAML, prototype pollution y cadenas con CVEs. Usar cuando el reto entregue una URL,
  un servicio HTTP/API o el código de una aplicación web.
  Keywords: CTF web, SQLi, blind SQLi, XSS, CSP bypass, SSTI, SSRF, XXE, JWT, OAuth, SAML,
  prototype pollution, deserialization.'
domain: cybersecurity
subdomain: ctf
tags:
- ctf
- web
- sqli
- xss
- ssti
- ssrf
- jwt
version: '1.0'
author: auditoria-ia-v2
license: Apache-2.0
---

# CTF Web — explotación de aplicaciones

## Cuándo usarla

El reto da una URL, un servicio HTTP/API, una SPA o el código de la aplicación.
Complementa las tarjetas `web-*` del repo general (que son de pentest): aquí el
objetivo es la flag y el alcance es el host del reto.

## Procedimiento

1. Recon: rutas, cabeceras, cookies, tecnologías, `robots.txt` y endpoints ocultos.
2. Preguntas de entrada: ¿dónde se refleja la entrada?, ¿qué se firma?, ¿qué se
   deserializa?, ¿qué busca el servidor?
3. Elegir familia: inyección (SQLi/SSTI/XXE), control de acceso (IDOR/BFLA),
   cliente (XSS/CSP/prototype pollution) o sesión (JWT/OAuth/SAML).
4. Confirmar con la variante mínima; automatizar solo después.
5. Cegueras: usar callback propio (SSRF, XXE, XSS, OAuth redirect).
6. Stack con versión conocida → cruzar CVEs antes de inventar cadenas.

## Material de profundidad

Repo upstream: <https://github.com/ljagiello/ctf-skills> (MIT, commit `a6106aaf`).
Clonar aparte y leer `skills/_src/ljagiello-ctf-skills/ctf-web/`; no se vendoriza en este repositorio.

| Tema | Archivo |
|---|---|
| SQLi | `sql-injection.md` |
| Server-side | `server-side*.md`, `server-side-deser.md`, `server-side-exec*.md` |
| Cliente | `client-side*.md` |
| Auth | `auth-*.md` (JWT, OAuth, SAML) |
| Node | `node-and-prototype.md` |
| CVEs | `cves.md` |
| Notas | `field-notes.md` |

Instalación con profundidad: `python scripts/install_skills.py --repo . --only ctf-web --with-deep`.

## Herramientas

`curl`, `ffuf`, `sqlmap`, `nuclei`, `jwt_tool`, `ysoserial`, `tplmap`, DevTools.

## Guardrails

- Solo el host y alcance que declara el reto.
- Sin fuerza bruta de credenciales salvo que el reto lo permita.
- Registrar payload, respuesta y versión del servidor como evidencia.
