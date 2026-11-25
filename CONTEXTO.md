# CONTEXTO — repositorio CTF Arsenal

## Objetivo del repositorio

Concentrar el conocimiento de CTF (70 %) y de hacking ético / auditoría (30 %) en
un solo lugar, de forma que cualquier integrante del grupo pueda resolver un reto
o reproducir un hallazgo siguiendo el writeup paso a paso, sin depender de quien
lo resolvió originalmente.

Se comparte con el grupo de CTF y se publica en GitHub sin datos sensibles
(`AGENTS.md` §3).

## Estructura

```
CTF\
├─ AGENTS.md · README.md · CONTEXTO.md
├─ LICENSE · THIRD-PARTY-NOTICES.md · .gitignore
├─ backups\      copias previas de archivos modificados
├─ skills\       skills cargables (SKILL.md + references + scripts)
├─ arsenal\      CLI ctf-arsenal, install_skills, sanitize
├─ herramientas\ cheatsheets por herramienta
├─ plantillas\   writeup, triaje, autorización, scope, informe
├─ docs\         TECNICAS.md, INDICE-SKILLS.md, FORMATO
├─ CTF\          retos, por evento
├─ AUDITORIA\    auditorías, por cliente
└─ PENTESTING\   pentests, por engagement
```

## Convención de nombres

- Modo: `CTF` · `AUDITORIA` · `PENTESTING` (mayúsculas).
- Evento/cliente y objetivo: minúsculas, sin espacios ni tildes, `[a-z0-9._-]`.
- Si el usuario ya creó una carpeta con otro nombre, se respeta.

## Índice de objetivos

| Modo | Evento / cliente | Objetivo | Estado | Fecha |
|---|---|---|---|---|
| — | — | *(sin objetivos todavía)* | — | — |

## Inventario de skills

Ver `docs\INDICE-SKILLS.md` para el detalle y la tabla completa.
Resumen: **13 skills de CTF + 20 de pentest/auditoría = 33**.

## Historial

### 2026-11-24 — Creación del repositorio

- Raíz creada en `C:\Users\shapl\OneDrive - dipreca.cl\Agentes IA\CTF`.
- Carpetas base: `backups`, `skills`, `arsenal`, `herramientas`, `plantillas`,
  `docs`, `CTF`, `AUDITORIA`, `PENTESTING`.
- Skills copiadas desde `AUDITORIA_IA_V2\.agents\skills`: 13 de CTF y 20 de
  pentest/auditoría (detalle en `docs\INDICE-SKILLS.md`).
- Documentos base: `AGENTS.md` (protocolo de arranque con las tres preguntas),
  `README.md`, `CONTEXTO.md`, `LICENSE`, `THIRD-PARTY-NOTICES.md`, `.gitignore`.
- Arsenal: `ctf-arsenal` (despachador adaptado a `skills\<id>\scripts\`),
  `install_skills.py`, `sanitize.py`.
- Plantillas: writeup, triaje, autorización, scope, informe de auditoría.
- Cheatsheets iniciales en `herramientas\`.
- Decisión de repositorio: **nuevo** `github.com/Superchileno/ctf-arsenal`
  (no se reutiliza `cybersecurity-skills`).

### 2026-11-24 — Saneamiento de `skills\`

- Backup previo del árbol completo: `backups\skills.20261124-234047\` (154 archivos).
- `arsenal\sanitize.py` mejorado: validador de flags para descartar f-strings
  (`mascara_{etiqueta}`, `scan_report_{timestamp}`), exclusión de rangos de
  documentación y de IP link-local (`169.254.*`), exclusión de usuarios de
  contenedor (`/home/ctf`), y corrección del reemplazo de rutas Windows (ahora
  literal vía función, sin doble barra).
- Aplicado `--fix` sobre 17 archivos; verificación posterior: **0 hallazgos**.
- Reemplazada la ruta personal en las 6 skills puente por el repo upstream
  `https://github.com/ljagiello/ctf-skills` (MIT, `a6106aaf`).
- Informes: `backups\saneo-skills-antes.md` y `backups\saneo-skills-fix.md`.

### 2026-11-24 — Pendiente

- `git init` + push a `github.com/Superchileno/ctf-arsenal` (requiere `gh` o
  credenciales; `git` solo existe en Kali/WSL).
- Poblar `CTF\` con los retos de `AUDITORIA_IA_V2\ctf\` y `ANCI\`, saneados.

## Tabla de backups

| Fecha | Archivo original | Backup | Motivo |
|---|---|---|---|
| 2026-11-24 | `skills\` (árbol completo, 154 archivos) | `backups\skills.20261124-234047\` | Saneamiento previo a publicación |
| 2026-11-24 | `skills\` (informe) | `backups\saneo-skills-antes.md` | Detección previa al fix |
| 2026-11-24 | `skills\` (informe) | `backups\saneo-skills-fix.md` | Detalle de reemplazos aplicados |
