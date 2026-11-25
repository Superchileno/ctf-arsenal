# CTF Arsenal — conocimiento para resolver retos y auditorías

Repositorio de trabajo y de estudio para **CTF (70 %)** con una capa de
**hacking ético y auditoría (30 %)**. Cada técnica está documentada para que otra
persona pueda reproducir la solución paso a paso, sin depender de quién la
resolvió primero.

> Uso responsable: solo contra sistemas propios o con autorización escrita previa.
> Ver `AGENTS.md` §4.

---

## Qué hay aquí

| Carpeta | Contenido |
|---|---|
| `skills\` | 33 skills cargables: 13 de CTF y 20 de pentest/auditoría, cada una con `SKILL.md`, `references\`, `scripts\` |
| `arsenal\` | `ctf-arsenal`, CLI que despacha a los scripts de las skills |
| `herramientas\` | Cheatsheets por herramienta (nmap, ffuf, sqlmap, pwntools, gdb, binwalk…) |
| `docs\` | Técnicas destiladas, índice de skills, formato de writeup |
| `plantillas\` | Writeup, triaje, autorización, scope, informe de auditoría |
| `CTF\` | Un directorio por evento y por reto resuelto |
| `AUDITORIA\` | Un directorio por cliente y objetivo auditado |
| `PENTESTING\` | Un directorio por engagement |

---

## Cómo se usa

### 1. Arrancar una sesión con el agente

Al abrir el agente en esta carpeta, responde las tres preguntas de `AGENTS.md` §0:

```
¿CTF, auditoría o pentesting?
¿Cómo se llama el evento / cliente?
¿Cómo se llama el objetivo / reto?
```

Con eso se crea la carpeta correcta y el agente documenta el trabajo ahí.

### 2. Instalar las skills en el agente

```bash
python arsenal\install_skills.py --repo . --dest ~/.agents/skills
```

### 3. Usar el arsenal

```bash
python arsenal\ctf-arsenal --list
python arsenal\ctf-arsenal triage reto.png
python arsenal\ctf-arsenal carve reto.png --out work\n
python arsenal\ctf-arsenal xor known --plain p.txt --cipher c1.hex --target c2.hex
```

### 4. Saneamiento antes de publicar

```bash
python arsenal\sanitize.py --path docs\ --check
```

---

## Estructura de un objetivo

```
CTF\<evento>\<reto>\
├─ CONTEXTO.md   ← writeup reproducible (obligatorio)
├─ solucion\     ← scripts de resolución
├─ work\         ← artefactos intermedios
└─ flags\        ← solo local, no se publica
```

La plantilla completa está en `plantillas\writeup.md` y la anatomía obligatoria en
`AGENTS.md` §2.

---

## Reglas de publicación

- Las skills y las técnicas se publican **saneadas**: sin flags, hosts, IPs,
  credenciales ni PII (`AGENTS.md` §3).
- Los writeups de competiciones en curso no se publican hasta que el evento cierre.
- Los directorios `work\`, `flags\`, `evidence\` y `backups\` no se versionan.

---

## Licencia y atribución

- Contenido propio (skills CTF, técnicas, plantillas, documentación): **MIT** (`LICENSE`).
- Material de terceros: ver `THIRD-PARTY-NOTICES.md`.
