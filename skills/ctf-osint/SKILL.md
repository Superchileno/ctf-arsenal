---
name: ctf-osint
description: 'OSINT de CTF: geolocalización por imagen y Street View, búsqueda inversa de imágenes,
  metadatos EXIF/GPS, enumeración de usuarios y perfiles (X, Tumblr, Bluesky, Telegram, GitHub,
  Steam), coordenadas MGRS y Plus Codes, DNS recon, Shodan, dorks de Google y homoglifos
  Unicode. Usar cuando la respuesta esté en fuentes públicas y haya que localizar, identificar
  o correlacionar.
  Keywords: CTF OSINT, geolocation, reverse image search, EXIF, username enumeration, MGRS,
  plus codes, Shodan, Google dorks, Telegram, Bluesky.'
domain: cybersecurity
subdomain: ctf
tags:
- ctf
- osint
- geolocation
- exif
- shodan
- social-media
version: '1.0'
author: auditoria-ia-v2
license: Apache-2.0
---

# CTF OSINT — localizar e identificar

## Cuándo usarla

El reto pide un lugar, una persona, un objeto, una cuenta o un dato verificable en
fuentes públicas: foto, video, perfil, coordenada o fragmento de texto.

## Procedimiento

1. Extraer lo que ya está en el archivo: EXIF, GPS, comentarios, miniaturas.
2. Separar lo verificable (metadatos) de lo interpretable (contexto visual).
3. Geolocalizar por capas: país → ciudad → calle → punto exacto.
4. Búsqueda inversa con recortes, no con la imagen completa.
5. Enumerar usuarios y perfiles por alias; correlacionar fechas y estilo.
6. Confirmar con una segunda fuente independiente antes de responder.

## Material de profundidad

Repo upstream: <https://github.com/ljagiello/ctf-skills> (MIT, commit `a6106aaf`).
Clonar aparte y leer `skills/_src/ljagiello-ctf-skills/ctf-osint/`; no se vendoriza en este repositorio.
(MIT).

| Tema | Archivo |
|---|---|
| Geolocalización y medios | `geolocation-and-media.md` |
| Redes sociales | `social-media.md` |
| Web y DNS | `web-and-dns.md` |

Complementa `solving-ctf-challenges-systematically` (OSINT de triaje) y las
tarjetas `osint-*` del repo general.

## Herramientas

`exiftool`, búsqueda inversa (Google Lens, Yandex), `what3words`, conversor MGRS,
`theHarvester`, `amass`, `shodan`, Wayback, `sherlock`.

## Guardrails

- Solo fuentes públicas; nada de cuentas privadas ni ingeniería social.
- No doxear personas reales: se responde con coordenada o alias.
- Registrar URL y fecha de consulta; el contenido público cambia.
