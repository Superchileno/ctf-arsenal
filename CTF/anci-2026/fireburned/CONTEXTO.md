# ANCI — CTF "Fireburned"

**Evento:** CTF ANCI — reto web
**Nombre interno:** Fireburned
**URL:** https://<host>/fireburned/
**Formato de flag:** `flag{..}`
**Fecha de registro:** 2026-10-29
**Estado:** 🔎 en curso — el upstream del reto no responde (timeout); reintentando.

---

## Enunciado

> Una institución implementó una consola de administración para automatizar el
> envío de notificaciones y documentos a distintos sistemas internos y servicios
> externos.
>
> La plataforma utiliza webhooks para recuperar borradores de documentos y
> generar vistas previas de tarjetas de notificación antes de distribuirlas a sus
> destinatarios.
>
> Tras su puesta en producción, el equipo de operaciones detectó comportamientos
> que podrían indicar problemas en los mecanismos de seguridad de la integración.
>
> En incidentes reales, el compromiso de integraciones entre plataformas y el uso
> de credenciales con permisos excesivos han permitido a atacantes acceder a
> información y recursos de organizaciones afectadas.
>
> Tu misión consiste en investigar la consola, analizar su comportamiento y
> descubrir qué está ocurriendo dentro de la plataforma.

---

## Hipótesis iniciales

La pieza central son los **webhooks que recuperan documentos**:

1. **SSRF**: el servidor hace `fetch()` de una URL controlada por el usuario →
   acceso a servicios internos / metadata cloud (`169.254.169.254`), puertos
   locales (Redis, admin API) o `file://`.
2. **Fuga de credenciales**: el webhook usa un token/Secreto con permisos
   excesivos y la respuesta (o la vista previa de la tarjeta) lo refleja.
3. **Inyección en la vista previa**: el "documento" recuperado se renderiza como
   tarjeta (Markdown/HTML/template) → XSS/SSTI en el panel admin.
4. **Robo de webhook**: URL de webhook adivinable / firma no verificada → se
   inyectan documentos arbitrarios en la cola de distribución.

## Plan de trabajo

1. Obtener el front (`/fireburned/`) cuando el upstream responda; identificar
   endpoints (`api/health`, `api/version`, formularios, JS).
2. Enumerar la API (crear/listar webhooks, preview, drafts, distribución).
3. Probar SSRF contra el propio host (`127.0.0.1`, `localhost`, servicios
   internos) y metadata; buscar el `flag{..}` en las respuestas.
4. Si el preview renderiza templates/Markdown, probar inyección.
5. Documentar y extraer la flag.

## Bitácora

| Fecha (UTC) | Acción | Resultado |
|---|---|---|
| 2026-10-29 15:2x | `GET /fireburned/` | timeout (sin respuesta) |
| 2026-10-29 15:3x | `GET /` (host) | `403` nginx (host vivo) |
| 2026-10-29 15:3x | `GET /blind-spot/api/health` (control) | timeout → todo el upstream del host está caído/inestable |
| 2026-10-29 15:48 | `GET /fireburned/` (timeout 70 s) | `504 Gateway Time-out` a los 60 s (nginx) |
| 2026-10-29 15:48 | `/api/v1/`, `/api/token/`, `/api/challenges/` | `502 Bad Gateway` inmediato |
| 2026-10-29 15:49 | Puerto 8080 del host | Apache por defecto (sitio ajeno al reto) |
| 2026-10-29 15:49 | `GET /fireburned/` con cookie JWT | `504` (la cookie no influye) |
| 2026-10-29 15:50 | `<host>` | "All Systems Operational" (solo mide hackrocks.com, no los retos) |

**Diagnóstico:** nginx de `<host>` está arriba, pero **todos los
upstreams de retos y el API están caídos** (504/502). El reto *blind-spot*, que
funcionaba hace una hora, también está caído: es una caída de infraestructura
del CTF, no del reto. Reintentador de 1 h en segundo plano (`fetch_until.py`).

Lectura: nginx responde, pero los contenedores de los retos no. Se deja un
reintentador en paralelo (`fetch_until.py`) que guarda `index.html` al primer
`200`.

## Archivos

- `CONTEXTO.md` — este documento.
- `cli.py` — cliente con reintentos para la API del reto.
- `fetch_until.py` — insiste en paralelo hasta obtener `200` y guarda el HTML.

## Autorización

Reto CTF público de HackRocks/ANCI. Pruebas limitadas a
`<host>` (y sus servicios internos, en el contexto del reto).
