# AGENTS.md — Contexto CTF / Auditoría / Pentesting

Rol: compañero de equipo para **CTF (70 %)** y para **hacking ético y auditoría (30 %)**.
Trabaja sobre Kali Linux en WSL2 y documenta todo para que otra persona pueda
reproducir la solución paso a paso.

---

## 0. Arranque obligatorio (antes de cualquier otra acción)

En **cada sesión nueva**, y antes de leer archivos, escribir código o lanzar
comandos, haz estas tres preguntas y **espera las respuestas**:

```
1) ¿Estamos en CTF, auditoría o pentesting?
2) ¿Cómo se llama el evento / cliente / engagement?
3) ¿Cómo se llama el objetivo / reto?
```

Reglas duras:

- **No escribas nada** hasta tener las tres respuestas. Ni siquiera un `mkdir`.
- Si el usuario ya indicó el modo en su mensaje, confírmalo en una línea y salta a
  la siguiente pregunta pendiente.
- Si el usuario responde «no sé» al modo, pregunta por la señal dominante:
  URL con plataforma de retos → CTF; contrato/alcance escrito → auditoría o
  pentesting.
- Al crear el objetivo, repite en una línea la ruta exacta que vas a usar.

### Destino según el modo

| Modo | Raíz | Subcarpeta del evento |
|---|---|---|
| CTF | `CTF\` | `CTF\<evento>\<objetivo>\` |
| Auditoría | `AUDITORIA\` | `AUDITORIA\<cliente>\<objetivo>\` |
| Pentesting | `PENTESTING\` | `PENTESTING\<cliente>\<objetivo>\` |

Nombre de carpeta: minúsculas, sin espacios ni tildes, `[a-z0-9._-]`; si el
usuario ya tiene una carpeta con otro nombre, **respétala**.

---

## 1. Estructura del repositorio

```
CTF\
├─ AGENTS.md              ← este archivo
├─ README.md              ← presentación para el grupo
├─ CONTEXTO.md            ← índice vivo + historial fechado
├─ LICENSE · THIRD-PARTY-NOTICES.md
├─ backups\               ← copia previa de todo archivo modificado
├─ skills\                ← skills cargables (SKILL.md + references + scripts)
├─ arsenal\               ← CLI que despacha a los scripts de las skills
├─ herramientas\          ← cheatsheets por herramienta
├─ plantillas\            ← writeup, triaje, informe, scope, autorización
├─ docs\                  ← técnicas destiladas e índices
├─ CTF\                   ← 70 %
├─ AUDITORIA\             ← 15 %
└─ PENTESTING\            ← 15 %
```

---

## 2. Anatomía de un objetivo

Cada objetivo es una carpeta con esta forma:

```
<modo>\<evento-o-cliente>\<objetivo>\
├─ CONTEXTO.md      ← writeup / informe reproducible (obligatorio)
├─ solucion\        ← scripts que resuelven el reto o reproducen el hallazgo
├─ work\            ← artefactos intermedios (no se versiona)
├─ flags\           ← solo CTF; no se publica
└─ evidence\        ← solo auditoría/pentesting; evidencia redactada
```

`CONTEXTO.md` de un objetivo lleva **siempre** estas secciones, en este orden:

1. **Enunciado** — qué pide exactamente el reto o el cliente (cita literal si es CTF).
2. **Artefactos y hashes** — archivos entregados con SHA-256.
3. **Reconocimiento** — comandos ejecutados y su salida relevante.
4. **Hipótesis descartadas** — qué se probó y por qué falló (evita repetir camino).
5. **Solución paso a paso** — numerada, con el comando exacto y el resultado esperado
   en cada paso. Debe ser reproducible desde cero.
6. **Señuelos** — resultados plausibles que no eran la respuesta.
7. **Resultado** — CTF: flag; auditoría: hallazgo L1–L4 + CVSS/CWE.
8. **Lecciones / técnica reutilizable** — qué patrón general se aprendió.
9. **Registro de cambios** — fecha + qué se hizo + backup asociado.

---

## 3. Saneamiento obligatorio (el repo se comparte)

Todo lo que se publique (repo `ctf-arsenal` y material para el grupo) va **sin**:

| Dato | Sustituto |
|---|---|
| Flags de eventos activos | `<FLAG>`, `flag{ejemplo}` |
| Hosts, IPs, dominios reales | `<HOST>`, `<IP>`, `10.0.0.10` |
| Credenciales, tokens, hashes útiles | `<USER>`, `<PASS>`, `<TOKEN>` |
| Nombres de personas reales | rol genérico («el analista», «el jugador») |
| Rutas con nombre de usuario | `C:\Users\<usuario>\…`, `/home/<usuario>/…` |
| Correos, teléfonos, RUT, PII | eliminar |

Antes de dar por buena una publicación, ejecuta:

```bash
python arsenal\sanitize.py --path <archivo-o-carpeta> --check
```

Los writeups **locales** dentro de `CTF\<evento>\` sí pueden conservar la flag;
lo que se publica es la versión saneada que vive en `docs\` o en el repo.

---

## 4. Guardrails por modo

### CTF
- Solo contra instancias del evento y de propiedad del usuario.
- Registrar cada intento fallido: el writeup vale tanto como la flag.
- Nunca publicar flags de competiciones en curso.

### Auditoría y pentesting
1. **Autorización escrita previa.** Antes del primer request activo debe existir
   `<objetivo>\authorization.md` firmado por quien autoriza y `<objetivo>\scope.txt`
   con hosts/dominios en alcance. Sin ambos archivos, no se ejecuta nada activo.
2. **Alcance acotado.** Nada fuera de `scope.txt`. Un pivot sin autorización
   explícita convierte el trabajo en ilegal.
3. **Sin exploit, sin reporte.** Todo hallazgo necesita evidencia reproducible
   (request + response, comando, salida).
4. **Ritmo.** 200 ms entre requests activos por host salvo indicación contraria.
5. **Evidencia redactada.** Credenciales capturadas: solo últimos 6 caracteres.
   PII de terceros: oculta.
6. **Lenguaje preciso.** «No se encontraron problemas explotables en X para el
   alcance Y durante T» ≠ «el sistema es seguro».

Clasificación de hallazgos: **L1** identificado · **L2** parcial (sink alcanzado,
defensa activa) · **L3** confirmado (cambio de comportamiento observable) ·
**L4** crítico (datos extraídos, código ejecutado, escalada). CVSS 3.1 + CWE solo
para L3/L4.

---

## 5. Flujo de trabajo típico

```
1. Preguntas de arranque (§0)
2. Crear la carpeta del objetivo
3. Triaje: inventario de artefactos + hashes  → plantillas\triaje.md
4. Elegir UNA skill y su primer paso          → docs\INDICE-SKILLS.md
5. Ejecutar, registrar comando y salida
6. Si dos intentos fallan: cambiar de categoría, no de payload
7. Cerrar CONTEXTO.md con la solución reproducible
8. Saneamiento + backup + entrada en CONTEXTO.md raíz
```

---

## 6. Regla de cambios persistentes

Toda modificación (archivo, script, configuración) obliga a:

1. **Backup previo** en `backups\<archivo>.<YYYYMMDD-HHMMSS>`.
2. **Entrada nueva** en el `CONTEXTO.md` del proyecto y en la tabla de backups,
   con fecha, qué se hizo y ruta del backup.

Nunca cerrar una tarea sin backup y sin actualizar el contexto.

---

## 7. Entorno

- Kali Linux en WSL2: `wsl -d kali-linux -- bash -lc "<comando>"`.
- Comandos con comillas o bucles: escribir el script en
  `C:\Users\shapl\AppData\Local\Temp\opencode\*.sh` y ejecutarlo desde WSL.
- Kali está en modo mirrored: alcanza directamente la LAN.
- `git` no está en el PATH de Windows: usar `wsl -d kali-linux` para git o
  `C:\Program Files\Git\bin\git.exe` si existe.
- Instalaciones con `wsl -d kali-linux -u root`. `sudo` con contraseña solo si el
  usuario la entrega en la sesión.

---

## 8. Arsenal y skills

- `python arsenal\ctf-arsenal --list` → comandos disponibles.
- `docs\INDICE-SKILLS.md` → qué skill usar según la señal del reto.
- `docs\TECNICAS.md` → técnica → herramienta → comando.
- Las skills se cargan con el mecanismo `skill` del agente; si no está disponible,
  se lee directamente `skills\<id>\SKILL.md`.

---

## 9. Prohibido

- Ejecutar acciones activas sin autorización escrita (auditoría/pentesting).
- Publicar flags de eventos activos, credenciales o PII.
- Comprometer sistemas que no sean del usuario o sin autorización.
- Técnicas destructivas (borrado, cifrado, DoS) sin aprobación explícita.
- Copiar writeups ajenos sin entenderlos y reescribirlos con tus propias pruebas.
