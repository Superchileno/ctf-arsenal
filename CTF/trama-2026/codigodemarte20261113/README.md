# Código de Marte 2026-11-13

Desafíos del evento, resueltos el 2026-11-13. Objetivos: `203.0.113.10` (8001/8005/8007/8008) y `<host>` (contenedor en 27370).

| # | Desafío | Puerto | Categoría | Estado | Flag |
|---|---|---|---|---|---|
| 01 | [Bodega de farmacia](bodega-farmacia/CONTEXTO.md) | 8005 | Web / lógica de negocio (cantidad negativa) | ✅ resuelto | `flag{ejemplo}` |
| 02 | [Consola SICH](consola-sich/CONTEXTO.md) | 8007 | Web / JWT `alg: none` | ✅ resuelto | `flag{ejemplo}` |
| 03 | [Sistema de avisos internos](avisos-internos/CONTEXTO.md) | 8008 | Web / SSTI Jinja2 (`{{config}}`) | ✅ resuelto | `flag{ejemplo}` |
| 04 | [Portal de acceso clínico](portal-clinico/CONTEXTO.md) | 8001 | Web / recon (`robots.txt` + backups expuestos) | ✅ resuelto | `flag{ejemplo}` |
| 05 | [Pharmatek](pharmatek/CONTEXTO.md) | 27370 | Web / secretos en el frontend (SPA + source maps) | ✅ resuelto | `flag{ejemplo}` |
| 06 | [Credencial digital del personal](credencial-digital/CONTEXTO.md) | 8002 | Web / cookie sin firma (rol editable) | ✅ resuelto | `flag{ejemplo}` |
| 07 | [Sistema central de recetas](recetas/CONTEXTO.md) | 8004 | Web / SQLi + filtro evadible (SQLite) | ✅ resuelto | `flag{ejemplo}` |
| 08 | [Archivo de historias clínicas](historias-clinicas/CONTEXTO.md) | 8006 | Web / path traversal (`....//`) | 🚧 en curso (host sin respuesta) | *(pendiente)* |
| 09 | [NexoDesk: asistente corrupto](nexodesk/CONTEXTO.md) | 8081 | Web / LLM + secreto fuera del contexto | ✅ resuelto | `flag{ejemplo}` |
| 10 | [Lumen Flow](lumen-flow/CONTEXTO.md) | 8083 | Web / Q-learning + envenenamiento de recompensa | ✅ resuelto | `flag{ejemplo}` |
| 11 | [HIS: Historial Clínico Electrónico](his-historial-clinico/CONTEXTO.md) | 24235 | Auditoría web / GraphQL + SSTI (RCE) | ✅ resuelto | `flag{ejemplo}` |

## Estructura

```
codigodemarte20261113/
├── README.md              <- este índice
├── backups/               <- copias previas
├── deploy/                <- material de despliegue (vacío)
├── bodega-farmacia/
│   ├── CONTEXTO.md        <- writeup
│   ├── flag.txt
│   ├── scripts/solve.py
│   └── evidence/          <- peticiones/respuestas crudas
├── consola-sich/
│   ├── CONTEXTO.md
│   ├── flag.txt
│   ├── scripts/solve.py
│   └── evidence/
├── avisos-internos/
│   ├── CONTEXTO.md
│   ├── flag.txt
│   ├── scripts/solve.py
│   └── evidence/
├── portal-clinico/
│   ├── CONTEXTO.md
│   ├── flag.txt
│   ├── scripts/solve.py
│   └── evidence/
├── pharmatek/
│   ├── CONTEXTO.md
│   ├── flag.txt
│   ├── scripts/solve.py
│   └── evidence/
├── credencial-digital/
│   ├── CONTEXTO.md
│   ├── flag.txt
│   ├── scripts/solve.py
│   └── evidence/
├── recetas/
│   ├── CONTEXTO.md
│   ├── flag.txt
│   ├── scripts/solve.py
│   └── evidence/
├── historias-clinicas/
│   ├── CONTEXTO.md
│   ├── scripts/recon.py
│   └── evidence/
└── nexodesk/
    ├── CONTEXTO.md
    ├── flag.txt
    ├── scripts/decode.py
    └── evidence/
```

Además: `lumen-flow/` con `CONTEXTO.md`, `flag.txt`, `scripts/solve.py` y `evidence/`.

`his-historial-clinico/` (HIS, `<host>:24235`): `CONTEXTO.md` (informe de auditoría),
`flag.txt`, `scripts/solve.py` y `evidence/` (incluye el código fuente extraído vía RCE).
