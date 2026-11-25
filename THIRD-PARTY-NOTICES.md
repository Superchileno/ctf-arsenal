# Third-Party Notices

Este repositorio combina material propio con skills derivadas de proyectos de
terceros. Cada skill conserva en su frontmatter el campo `license` y `author`
original.

---

## 1. Skills en `skills/` — Apache-2.0

Las 20 skills de pentest/auditoría y las 13 de CTF declaran `license: Apache-2.0`.
Su origen:

| Origen | Autoría | Licencia | Uso aquí |
|---|---|---|---|
| Colección interna `auditoria-ia-v2` (agente propio) | `auditoria-ia-v2` | Apache-2.0 | 13 skills de CTF |
| [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | `mahipal` | Apache-2.0 | 20 skills de pentest/auditoría |

Texto de la licencia Apache 2.0:
<https://www.apache.org/licenses/LICENSE-2.0>

Al redistribuir: conserva el frontmatter de cada `SKILL.md` (name, author,
license) y este aviso.

> Todas las skills fueron **saneadas**: no contienen flags de eventos, hosts,
> IPs, credenciales, correos ni nombres de personas reales.

---

## 2. Material de profundidad CTF — MIT

Las skills puente `ctf-web`, `ctf-misc`, `ctf-ai-ml`, `ctf-malware`, `ctf-osint`
y `ctf-orquestacion` resumen en español la técnica y enrutan a material de
terceros:

| Proyecto | Autor | Licencia | Commit de referencia |
|---|---|---|---|
| [ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills) | ljagiello | MIT | `a6106aaf` |

Las skills puente **no duplican** ese contenido: describen el procedimiento y
remiten al árbol original. Si se vendoriza material en el futuro, debe incluirse
el aviso MIT de su autor.

---

## 3. Contenido propio

- `docs/`, `plantillas/`, `herramientas/`, `arsenal/` y las técnicas destiladas
  de retos resueltos: obra propia bajo **MIT** (`LICENSE`).
- Los writeups derivan de competiciones reales; se publican sin flags, sin datos
  de infraestructura y sin identificar a terceros.
- La licencia MIT de `LICENSE` **no** se aplica a `skills/`, que conserva la
  licencia declarada en el frontmatter de cada `SKILL.md` (Apache-2.0 en las
  skills derivadas de terceros).

---

## 4. Marcas y plataformas

Los nombres de plataformas de CTF, herramientas y eventos se usan solo con fines
descriptivos. No hay afiliación ni patrocinio implícito.
