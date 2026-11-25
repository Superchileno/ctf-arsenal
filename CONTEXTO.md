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

- Raíz creada como carpeta hermana de `AUDITORIA_IA_V2`, en `Agentes IA\CTF`.
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

### 2026-11-24 — Importación de writeups locales

- Nuevo `arsenal\import_local.ps1`: copia solo documentación y scripts
  (`.md .py .sh .txt .csv .json`, ≤ 256 KB), excluyendo `work\`, `evidence\`,
  `flags\`, `backups\` y binarios.
- `ctf\` de `AUDITORIA_IA_V2` → `CTF\trama-2026\` (319 archivos, 50 carpetas).
- `ANCI\` de `AUDITORIA_IA_V2` → `CTF\anci-2026\` (234 archivos, 14 carpetas).
- Saneamiento de lo importado con `arsenal\sanitize.py --fix`:
  trama: 431 flags, 63 hosts, 70 IPs, 11 rutas; anci: 25 flags, 98 hosts,
  37 correos, 4 IPs, 6 rutas. Verificación posterior: **0 hallazgos**.
- Informes: `backups\saneo-trama.md`, `backups\saneo-anci.md`.
- Carpeta con nombre corrupto `se?alfantasma` renombrada a `senalfantasma`.

### 2026-11-24 — Reparación de archivos y rutas de perfil

- Incidencia: un script de reemplazo con arreglos aplanados de PowerShell corrompió
  texto en `AGENTS.md`, `CONTEXTO.md` y `herramientas\kali-wsl.md`.
- Reparación: `git checkout HEAD --` de los tres archivos y reaplicación manual de
  los cambios con el editor (nunca con reemplazos de un carácter).
- `sanitize.py`: nuevas reglas para rutas de perfil en forma WSL/msys
  (`/mnt/c/Users/<usuario>`, `/c/Users/<usuario>`) y con separador normal
  (`C:/Users/<usuario>`).
- Resultado: 146 reemplazos en 119 archivos de `CTF\`; verificación global
  **0 hallazgos** y sin restos del usuario real en el árbol.
- Informe: `backups\saneo-rutas-mnt.md`.

### 2026-11-24 — Repositorio Git local

- `git init -b main` en la raíz del proyecto, commit inicial
  `CTF arsenal: 33 skills, plantillas, cheatsheets y saneamiento` (187 archivos).
- Remote configurado: `origin https://github.com/Superchileno/ctf-arsenal.git`.
- **Push pendiente**: no hay `gh` ni credenciales guardadas en el entorno.

### 2026-11-24 — Intento de publicación (token revocado)

- `Superchileno/ctf-arsenal` **existe** en GitHub (creado vacío, público, rama `main`).
- Primer intento con PAT fine-grained: el token funcionó en la API (`login:
  Superchileno`) y luego pasó a `401 Bad credentials`; el push falló con
  *«Invalid username or token»*.
- Causa: el token fue revocado (GitHub revoca tokens expuestos en texto
  público/claros). **No se debe pegar el token en el chat.**
- Token eliminado del disco local y del remote; el remote quedó limpio
  (`https://github.com/Superchileno/ctf-arsenal.git`).
- Procedimiento seguro: guardar el token en
  `%TEMP%\opencode\gh_token.txt` y ejecutar `arsenal\crear_repo.sh`
  (push vía `GIT_ASKPASS`, sin exponer credenciales en la URL).

### 2026-11-24 — Pendiente

- Push a `github.com/Superchileno/ctf-arsenal` con un token nuevo que tenga
  **Contents: Read and write** sobre ese repositorio.

## Tabla de backups

| Fecha | Archivo original | Backup | Motivo |
|---|---|---|---|
| 2026-11-24 | `skills\` (árbol completo, 154 archivos) | `backups\skills.20261124-234047\` | Saneamiento previo a publicación |
| 2026-11-24 | `skills\` (informe) | `backups\saneo-skills-antes.md` | Detección previa al fix |
| 2026-11-24 | `skills\` (informe) | `backups\saneo-skills-fix.md` | Detalle de reemplazos aplicados |
| 2026-11-24 | `ctf\` local (informe) | `backups\saneo-trama.md` | Saneamiento de writeups importados |
| 2026-11-24 | `ANCI\` local (informe) | `backups\saneo-anci.md` | Saneamiento de writeups importados |
