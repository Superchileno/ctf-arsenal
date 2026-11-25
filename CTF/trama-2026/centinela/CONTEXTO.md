# Centinela — incidente de beacon C2 en GW-CORP

| Campo | Valor |
|---|---|
| Categoría | Forense de red — análisis de logs CEF (UniFi) |
| Evidencia | `eventos.log` (20 512 B, 37 eventos) · SHA-256 `5f690e59…c4f855` |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado (resumen)

Durante una ventana de tiempo corta, el sistema de seguridad de una oficina vio
actividad aparentemente habitual. Un equipo interno intentó comunicarse
insistentemente con un destino externo; el sistema intervino pero los registros
dejan preguntas. Hay que determinar **qué equipo**, **origen y destino**, **cuántas
comunicaciones se bloquearon** y **el mensaje oculto**.

Formato: `flag{ejemplo}`

## El log

37 líneas, todas eventos **CEF** de UniFi Network (gateway `GW-CORP`,
`UNIFIdeviceIp=10.10.0.1`). Campos relevantes: `src`, `dst`, `dpt`,
`UNIFIsrcClientHostname`, `UNIFIsrcClientMac`, `UNIFIthreat`, y en los eventos
útiles `cs1Label=IncidentFragment cs1=<base64>` + `cn1Label=FragmentIndex cn1=<n>`.

### Amenazas registradas (separar ruido del incidente)

| Hora (UTC) | Amenaza | Equipo | Destino | ¿Parte del incidente? |
|---|---|---|---|---|
| 13:11:34.500 | `OUTBOUND.DNS.Policy` | PC-BODEGA (10.10.0.54) | 198.51.100.99:53 | ❌ ruido |
| **13:11:38.000** | **`OUTBOUND.C2.Beacon`** | **PC-RECEPCION (10.10.0.51)** | **203.0.113.37:8443** | ✅ frag. 1 |
| 13:12:04.250 | `OUTBOUND.Web.Reputation` | PC-RECEPCION (10.10.0.51) | 203.0.113.119:443 | ❌ ruido |
| **13:12:13.000** | **`OUTBOUND.C2.Beacon`** | PC-RECEPCION | 203.0.113.37:8443 | ✅ frag. 2 |
| 13:12:38.500 | `OUTBOUND.PortScan` | NB-GERENCIA (10.10.0.53) | 203.0.113.90:445 | ❌ ruido |
| **13:12:48.000** | **`OUTBOUND.C2.Beacon`** | PC-RECEPCION | 203.0.113.37:8443 | ✅ frag. 3 |
| **13:13:23.000** | **`OUTBOUND.C2.Beacon`** | PC-RECEPCION | 203.0.113.37:8443 | ✅ frag. 4 |

Los cuatro eventos del incidente son idénticos en equipo, destino y puerto
(`8443`), severidad 9 y mensaje *«…has been detected and blocked.»* → **4 intentos
bloqueados**.

## Respuesta a cada incógnita

| Dato | Valor | Regla de la flag |
|---|---|---|
| host | `PC-RECEPCION` → `pc_recepcion` | minúsculas, `-`→`_` |
| MAC | `02:00:5e:a1:4f:a2` → `4fa2` | últimos 4 hex, sin separadores |
| IP destino | `203.0.113.37` → `203_0_113_37` | `.`→`_` |
| intentos | `4` | eventos C2 bloqueados |
| mensaje | `corto_el_beacon` | base64 de los fragmentos 1…4 |

## El mensaje oculto

Cada beacon bloqueado arrastraba un trozo base64 y su índice:

```
cn1=1  cs1=Y29y      -> "cor"
cn1=2  cs1=dG9f      -> "to_"
cn1=3  cs1=ZWxf      -> "el_"
cn1=4  cs1=YmVhY29u  -> "beacon"
```

Concatenando **en orden de `cn1`** y decodificando base64:

```
Y29y dG9f ZWxf YmVhY29u   ->   corto_el_beacon
```

## Solución

```bash
python3 solucion/analizar.py
```

```
eventos totales: 37
tipos: Counter({'Network': 30, 'OUTBOUND.C2.Beacon': 4, ...})

PC-RECEPCION (10.10.0.51) MAC 02:00:5e:a1:4f:a2 -> 203.0.113.37:8443  eventos=4
fragmentos: 4 -> índices [1, 2, 3, 4]
mensaje: corto_el_beacon

flag{ejemplo}
```

## Flag

```
flag{ejemplo}
```

## Notas

- El log mezcla tráfico legítimo (Web/NTP/DNS/LAN) con cinco alertas; **solo las
  cuatro de `OUTBOUND.C2.Beacon` comparten equipo, destino y puerto** y llevan
  `IncidentFragment`. Las demás (`DNS.Policy`, `Web.Reputation`, `PortScan`) son
  ruido de otros equipos/destinos y no tienen fragmentos.
- El `UNIFIsrcClientAlias` trae la MAC abreviada (`4f:a2`), pero la completa está en
  `UNIFIsrcClientMac`; los últimos 4 hex coinciden en ambos.
- El mensaje va partido en el campo `cs1` de cada evento: sin ordenar por `cn1` el
  base64 concatenado no decodifica.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `eventos.log` | evidencia original |
| `SHA256SUMS (1).txt` | checksum entregado con el reto |
| `flag.txt` | flag final |
| `CONTEXTO.md` | este writeup |
| `solucion/analizar.py` | parsea CEF, agrupa el incidente y arma la flag |
