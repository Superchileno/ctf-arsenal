---
name: ctf-misc
description: 'Retos misceláneos de CTF: pyjails y bash jails (evasión de audit hooks,
  normalización NFKC, traversal de objetos), codificaciones exóticas y esteganografía Unicode,
  Z3, RF/SDR e IQ, juegos y VMs, escalada local en contenedores y navegación de la plataforma
  sin navegador. Usar cuando el reto no encaje en web, pwn, crypto, forense ni reversing.
  Keywords: CTF misc, pyjail, bash jail, sandbox escape, Z3, encodings, Unicode steganography,
  SDR, IQ, SUID, docker group, CTFd.'
domain: cybersecurity
subdomain: ctf
tags:
- ctf
- misc
- pyjail
- encodings
- z3
- sdr
- privesc
version: '1.0'
author: auditoria-ia-v2
license: Apache-2.0
---

# CTF Misc — jails, codificaciones y señales

## Cuándo usarla

El reto entrega un intérprete restringido, un archivo sin categoría clara, una
señal de radio, una VM/juego o un acceso SSH de bajo privilegio.

## Procedimiento

1. Clasificar el artefacto: archivo, servicio interactivo, señal o binario SUID.
2. Intérprete restringido → mapear builtins y atributos accesibles antes de escribir payloads.
3. Entrada codificada → agotar la cadena de decodificaciones y revisar Unicode invisible
   (selectores de variación, bloque de tags).
4. Restricciones matemáticas → modelar con Z3 en vez de buscar a mano.
5. Shell disponible → revisar SUID, sudo, ACL, grupos (`docker`, `lxd`) y cron antes de exploits.
6. Señal → separar I/Q, espectrograma y modulaciones conocidas.

## Material de profundidad

Repo upstream: <https://github.com/ljagiello/ctf-skills> (MIT, commit `a6106aaf`).
Clonar aparte y leer `skills/_src/ljagiello-ctf-skills/ctf-misc/`; no se vendoriza en este repositorio.
(MIT).

| Tema | Archivo |
|---|---|
| Pyjails | `pyjails.md` |
| Bash jails | `bashjails.md` |
| Codificaciones | `encodings.md`, `encodings-advanced.md` |
| Juegos y VMs | `games-and-vms*.md` |
| Audio | `audio.md` |
| RF/SDR | `rf-sdr.md` |
| DNS | `dns.md` |
| Escalada local | `linux-privesc.md` |
| CTFd sin navegador | `ctfd-navigation.md` |

## Herramientas

`python3`, `z3-solver`, `pwntools`, GNU Radio, `inspect`, GTFOBins, `xxd`.

## Guardrails

- Probar las jails en local antes de golpear el servicio remoto.
- No ejecutar escapes fuera del contenedor del reto.
- Registrar la carga útil mínima que funcionó.
