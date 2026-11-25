# Desafío 35 — El audio de la profesora Ximena (4.º C)

| Campo | Valor |
|---|---|
| Evento | TRAMA CTF 2026 |
| Categoría | Web / forense de aplicación (chat escolar, mensaje eliminado, logs y respaldos) |
| Estado | 🚧 En curso — falta la URL del sistema asignado |
| Flag | *(pendiente)* |

## Enunciado

La profesora **Ximena** envió un audio al grupo del **4.º C** la noche anterior a una prueba.
Poco después comenzaron los rumores: alguien habría compartido información que no debía salir
del curso. Un mensaje desapareció y la conversación siguió como si nada.

El colegio conservó una **copia del sistema** para revisar el incidente, pero nadie tiene claro
cuánto quedó registrado ni qué alcanzó a ser eliminado.

> «Tienes acceso al sistema utilizado durante la investigación. Reconstruye lo ocurrido y
> descubre qué información intentaron hacer desaparecer.»
>
> Restricción del reto: **todo el análisis debe realizarse únicamente sobre la infraestructura
> asignada al reto.**

## Credenciales y tokens entregados por la plataforma

| Dato | Valor |
|---|---|
| Usuario | `alumno` |
| Contraseña | `4toC2026!` |
| Cookie de sesión de la app (`session`) | `eyJsb2dnZWRfaW4iOnRydWUsInVzdWFyaW8iOiJhbHVtbm8ifQ.atyspg.-DiMmm_AajtuwE8TaV4orLiHZJY` |
| Cookie de plataforma (`trama_session`) | `fcWp5lhLzYJrPaY6uVHgvPAkqNqrRd1yz242FO_SbGXVenGLENRP87mnh95naAQU` |

Payload decodificado de `session` (Base64URL):

```json
{"logged_in":true,"usuario":"alumno"}
```

Formato `payload.firma` partido por puntos — compatible con un token tipo Flask/itsdangerous
o JWT simplificado; la firma y el rol son el primer punto a auditar (posible manipulación de
`usuario`/`logged_in`).

## Hipótesis de trabajo

1. **Mensaje borrado**: soft-delete en la base (columna `deleted_at`, `visible`, `estado`) o
   borrado real → recuperar por respaldo / WAL / dump expuesto.
2. **El audio**: el archivo (`uploads/`, `.ogg`/`.mp3`/`.m4a`) puede seguir accesible por ID
   aunque el mensaje no se muestre; su transcripción o metadatos pueden contener la flag.
3. **Control de acceso**: IDs secuenciales de mensajes/usuarios/grupos (IDOR) y endpoints API
   (`/api/messages`, `/api/chat`, `/export`, `/admin`, `/backup`) sin autorización.
4. **Sesión**: firma débil o `secret` por defecto en la cookie `session` → escalar a la cuenta
   de la profesora o del alumno que filtró.
5. **Registro de la investigación**: el propio sistema de revisión puede exponer logs de
   auditoría (`audit.log`, `historial`, tabla `logs`) con la acción de borrado y su autor.

## Estructura

```
35-audio-profe-ximena/
├── CONTEXTO.md      <- este archivo (enunciado, hallazgos, flag, historial)
├── solucion/        <- scripts de resolución
├── work/            <- artefactos intermedios (respuestas HTTP, dumps, audio)
└── flags/           <- flags obtenidas (una por archivo)
```

## Pendiente / bloqueo

- **Falta la URL del sistema asignado** (patrón habitual de la plataforma:
  `https://hackinggame-<slug>.chals.io`). Sin el host no se puede iniciar el análisis; el DNS de
  `*.chals.io` es comodín (`203.0.113.10/116`), por lo que adivinar el slug no es fiable.

## Historial

### 2026-10-24 — Creación de la carpeta y registro del enunciado
- Se crea `ctf/35-audio-profe-ximena/` con estructura `solucion/`, `work/`, `flags/`.
- Se documentan credenciales (`alumno` / `4toC2026!`) y las dos cookies entregadas por la
  plataforma; se decodifica el payload de `session`.
- Verificado que el DNS de `chals.io` es comodín: `<host>` resuelve a las
  mismas IP que `<host>`, por lo que no se puede descubrir el
  host por resolución DNS.
- Estado: bloqueado a la espera de la URL del sistema del reto.
