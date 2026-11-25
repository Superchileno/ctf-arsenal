# Desafío 52 — Lumen Flow

| Campo | Valor |
|---|---|
| Evento | Código de Marte 2026-11-13 (`codigodemarte20261113`) |
| Categoría | Web / aprendizaje por refuerzo (Q-learning tabular) + envenenamiento de recompensa |
| Dificultad | media-alta |
| Puntos | 586 (5 soluciones) |
| Objetivo | `http://203.0.113.10:8083` |
| Estado | ✅ resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado

> Plataforma logística con una planta de clasificación animada y un controlador de Q-learning
> tabular que decide cuándo liberar lotes en una cinta. Los cierres de episodios alimentan la
> recompensa del modelo.

## Reconocimiento

La aplicación es una SPA (Flask + JS) que se alimenta de una única llamada de estado:

```
GET /api/overview
```

Devuelve:

- `target`: el envío destacado `ENV-900` (`EXP-900`), con su estado y los **valores Q** de las
  tres acciones (`liberar`, `dosificar`, `retener`), la decisión actual y el canal asignado.
- `replays`: los casos/episodios con su estado, acción tomada y recompensa.
- `history`: el detalle de cada actualización del modelo (`old_value`, `new_value`, `reward`,
  `snapshot` de la tabla Q en ese estado).
- `model`: `alpha = 0.25`, `gamma = 0.8`, `episodes`, `target_episodes = 8`.
- `simulation`: la última prueba de clasificación.

El estado se codifica como `<zona>|<ocupación>|<calidad>`:

| Señal | Valores | Umbral observado |
|---|---|---|
| ocupación de la cinta | 0–100 | `>66` alta · `34–66` media · `<34` baja |
| calidad de lectura | 0–100 | `>66` alta · `34–66` media · `<33` baja |

`ENV-900` (ocupación 86, lectura 24) vive en `recepcion|alta|baja`.

### Dónde se entrega la bandera

En `app.js`, `showResult()` pinta la bandera solo cuando el resultado de la simulación tiene
`outcome === 'desvio_de_carga'`:

```js
const diverted = result.outcome === 'desvio_de_carga';
...
if (diverted) { ...; if (result.flag) box.append(el('code','flag-value',result.flag)); }
```

Y el flujo de una prueba es:

```
POST /api/simulation/start     -> {run_id, decision, duration_ms: 5000}
POST /api/simulation/<run_id>/resolve
```

`resolve` devuelve la bandera cuando la decisión tomada fue `liberar` y el paquete se desvió por el
canal C. Es decir: **hay que hacer que el modelo prefiera `liberar` en `recepcion|alta|baja`**,
aunque la política "correcta" para ese estado sea retener.

## El camino: envenenar la recompensa

Cada caso tiene un formulario de cierre:

```
POST /api/replays/<id>/feedback
{"action": "liberar" | "dosificar" | "retener", "observed_time": <s>, "scan_errors": 0..5}
```

El `observed_time` y los errores los aporta el **operador** (el cliente); el servidor los usa como
verdad para calcular la recompensa del episodio y aplicar la actualización Q. No hay verificación de
que el tiempo observado sea real.

El historial de la instancia mostraba exactamente ese abuso: episodios del estado
`recepcion|alta|baja` cerrados como `liberar` con `observed_time = 5` (frente a un
`nominal_time ≈ 90–116`) reciben `reward = 4.0`:

| Episodio | nominal | observed | acción | reward | Q(`liberar`) antes → después |
|---|---|---|---|---|---|
| EPI-2101 | 102 | 5 | liberar | 4.0 | −3.0 → −0.85 |
| EPI-2102 | 94 | 5 | liberar | 4.0 | −0.85 → 0.7625 |
| EPI-2103 | 116 | 5 | liberar | 4.0 | 0.7625 → 1.971875 |
| EPI-2104 | 89 | 5 | liberar | 4.0 | 1.971875 → 2.878906 |
| EPI-2105 | 108 | 5 | liberar | 4.0 | 2.878906 → 3.559179 |
| EPI-2106 | 97 | 5 | liberar | 4.0 | 3.559179 → 4.069384 |

Con `retener` estancado en `4.5`, en cuanto `Q(liberar)` lo supera (4.739028 en la captura) la
decisión del envío cambia:

```json
"target": {
  "code": "EXP-900", "state": "recepcion|alta|baja",
  "decision": "liberar",
  "values": {"dosificar": 0.5, "liberar": 4.739028, "retener": 4.5}
}
```

### Cadena completa

```bash
BASE=http://203.0.113.10:8083

# 1) Estado del modelo y del envío destacado
curl -s $BASE/api/overview | jq '.target.values, .target.decision'

# 2) Si "liberar" aún no domina: crear un caso en recepcion|alta|baja y cerrarlo
#    con una recompensa alta (observed_time=5, sin errores)
curl -s -X POST $BASE/api/replays -H 'Content-Type: application/json' \
  -d '{"name":"Lote prioritario de auditoria","zone":"recepcion",
       "queue_score":90,"confidence":10,"nominal_time":90}'
curl -s -X POST $BASE/api/replays/<id>/feedback -H 'Content-Type: application/json' \
  -d '{"action":"liberar","observed_time":5,"scan_errors":0}'
# repetir hasta que target.decision == "liberar"

# 3) Lanzar la prueba y resolverla pasada la duración (5 s)
curl -s -X POST $BASE/api/simulation/start -H 'Content-Type: application/json' -d '{}'
curl -s -X POST $BASE/api/simulation/<run_id>/resolve -H 'Content-Type: application/json' -d '{}'
```

Respuesta:

```json
{
  "decision": "liberar",
  "detail": "ENV-900 enviado a un canal de clasificación incorrecto",
  "flag": "flag{ejemplo}",
  "outcome": "desvio_de_carga",
  "run_id": "RUN-04627F1F9A"
}
```

Automatizado en `scripts/solve.py`: comprueba la tabla Q, entrena con feedback si hace falta,
inicia y resuelve la simulación, e imprime/guarda la bandera.

```text
[*] episodios=14 objetivo=EXP-900 estado=recepcion|alta|baja
[*] `liberar` ya domina recepcion|alta|baja: {'dosificar': 0.5, 'liberar': 4.739028, 'retener': 4.5}
[*] simulacion RUN-E8724E8C73 decision=liberar duracion=5000 ms
[*] resultado: {"decision": "liberar", ..., "flag": "flag{ejemplo}", "outcome": "desvio_de_carga", ...}
[+] FLAG: flag{ejemplo}
```

> La instancia es compartida entre participantes, así que al momento de resolver ya estaba
> entrenada por otros cierres de episodios (13–14 episodios, `Q(liberar) = 4.739028`). El script
> reproduce el entrenamiento desde cero si la tabla Q no prefiere `liberar`.

## Señuelos descartados

`/static/audit-cache.js` se anuncia como «Copia local de constancias antiguas. No participa en la
clasificación actual.» y trae dos tokens con `codec: 'xor-b64', key: 57`:

```js
records: [
  {id:'LF-ARCHIVE-18', status:'archived', token_payload:'en10QlUJXghKTQhaDWZaDVpRCmYBWAtE'},
  {id:'LF-CAL-24',     status:'verified', token_payload:'en10QlQJXQpVCWZaDVUIW0sNXQlmD18IRA=='}
]
```

| Artefacto | Decodificación (Base64 + XOR 57) | Veredicto |
|---|---|---|
| `LF-ARCHIVE-18` | `flag{ejemplo}` | señuelo "caché antigua" |
| `LF-CAL-24` | `flag{ejemplo}` | señuelo "modelo calibrado" |

La bandera real solo se sirve desde `resolve` cuando hay `desvio_de_carga`; los tokens del caché de
auditoría no participan del flujo.

## Lecciones / notas

- **El cliente no puede ser la fuente de verdad del reward.** Un `observed_time` arbitrario permite
  inyectar recompensa máxima y empujar cualquier acción a la cima de la tabla Q (reward poisoning).
- **Un agente que aprende de datos del usuario hereda los sesgos del usuario.** Aquí la política
  aprende a `liberar` en un estado donde lo correcto es retener, y el "desvío" es la consecuencia
  que entrega la bandera.
- El estado del modelo es global y persistente (instancia compartida): si no se puede reiniciar
  limpio, verificar la tabla Q actual antes de entrenar evita pasos innecesarios.
- Evidencia en `evidence/`: HTML, `audit-cache.js`, `app.js`, `/api/overview` y la respuesta de
  `resolve` con la bandera.
