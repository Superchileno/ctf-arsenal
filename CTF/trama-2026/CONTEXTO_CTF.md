# CONTEXTO — CTF

## Objetivo

Documentar la resolución de cada desafío de CTF: enunciado, análisis, pasos, comandos
usados, hallazgos y flag obtenida.

## Estructura

```
ctf/
├── CONTEXTO_CTF.md          <- este archivo (índice + historial)
├── backups/                 <- copias de archivos antes de modificarlos
└── <carpeta-desafio>/       <- una carpeta por desafío
    ├── CONTEXTO.md | README.md  <- writeup (enunciado, análisis, solución, flag)
    ├── flag.txt
    ├── solucion/            <- scripts de resolución
    └── work/                <- artefactos intermedios
```

Convención de nombres: se respeta la carpeta que cree el usuario si ya existe
(p. ej. `casaembrujada/`); si no, `NN-nombre-desafio` (`01`, `02`, ...).
Nada de archivos sueltos en la raíz de `ctf/` ni en la raíz del proyecto.

## Índice de desafíos

| # | Desafío | Categoría | Estado | Flag |
|---|---------|-----------|--------|------|
| 01 | [Todo Gira](01-todo-gira/README.md) — TRAMA CTF 2026 MISC-015 | MISC / archivos anidados | ✅ resuelto | `flag{ejemplo}` |
| 02 | [La Mansión Blackwood](casaembrujada/CONTEXTO.md) | MISC / esteganografía LSB | ✅ resuelto | `flag{ejemplo}` |
| 03 | [Señal desde Blackwood](BW_SOC_3110/CONTEXTO.md) — BW_SOC_3110 | MISC / datos anexados a PNG (ZIP carving) | ✅ resuelto | `flag{ejemplo}` |
| 04 | [El Cuaderno de Claves](cuaderno-de-claves/CONTEXTO.md) | Crypto / cifrador casero (XOR+rot+swap) | ✅ resuelto | `flag{ejemplo}` |
| 05 | [Cartas](cartas/CONTEXTO.md) — lámina sin número | Crypto / sustitución de glifos (catálogo hex) | ✅ resuelto | `flag{ejemplo}` |
| 06 | [El baño VIP](El_Bano_VIP_Jugador/CONTEXTO.md) | Crypto / binario enmascarado + Base64 | ✅ resuelto | `flag{ejemplo}` |
| 07 | [Magma](Magma/CONTEXTO.md) — postal MG-07 | Stego visual / mosaico periódico | ✅ resuelto | `flag{ejemplo}` |
| 08 | [Mojojojo](mojojojo/CONTEXTO.md) — mensaje del micrófono | MISC / cadena hex→Base45→Base64→Ook!→Brainfuck | ✅ resuelto | `flag{ejemplo}` |
| 09 | [La Cuenta que No Existía](La_Cuenta_que_No_Existia/CONTEXTO.md) | OSINT / EXIF + perfiles archivados | ✅ resuelto | `flag{ejemplo}` |
| 10 | [El Ingrediente Secreto de Vlad](El_Ingrediente_Secreto_de_Vlad/CONTEXTO.md) | OSINT / GitHub (repo + historial) | ✅ resuelto | `flag{ejemplo}` |
| 11 | [6puntos](6puntos/CONTEXTO.md) — nodo VF0 | OSINT / EXIF + geolocalización + secuencia | ✅ resuelto | `flag{ejemplo}` |
| 12 | [Señal Fantasma](señalfantasma/CONTEXTO.md) — XimaTV / CentinelaOTA | Boot2Root / web upload + sudo eval | ✅ resuelto | USER: `flag{ejemplo}` · ROOT: `flag{ejemplo}` |
| 13 | [Libro de Visitas](librodevisitas/CONTEXTO.md) — `nc <host> 11071` | Pwn / format string (`%hn` posicional) | ✅ resuelto | `flag{ejemplo}` |
| 14 | [Turno Fantasma](turnofantasma/CONTEXTO.md) — `nc <host> 31547` | Pwn / stack overflow + ret2win | ✅ resuelto | `flag{ejemplo}` |
| 15 | [El Conde Ciber-Drácula](El_Conde_Ciber_Dracula/CONTEXTO.md) — charla en vivo en YouTube | OSINT + forense de video (DVR + OCR) | ✅ resuelto | `flag{ejemplo}` |
| 16 | [Eco Residual](ecoresidual/CONTEXTO.md) — `eco_residual` (ELF) | Reversing / token XOR con tabla de índices | ✅ resuelto | `flag{ejemplo}` |
| 17 | [El Cielo Falsificado](rutaespecial/CONTEXTO.md) — `ruta_espectral` | Reversing / ofuscación aritmética | ✅ resuelto | `flag{ejemplo}` |
| 18 | [La Partitura Muda](partitura/CONTEXTO.md) — `La_Partitura_Muda.zip` | Forense de audio / espectrograma + ZIP cifrado | ✅ resuelto | `flag{ejemplo}` |
| 19 | [La Lotería de los Condenados](condenados/CONTEXTO.md) — `Loteria_Condenados.zip` | Crypto / Base64 + XOR con clave repetida | ✅ resuelto | `flag{ejemplo}` |
| 20 | [La Feria del Persa](feriapersa/CONTEXTO.md) — `<host>` | Web / SQL injection UNION (SQLite) | ✅ resuelto | `flag{ejemplo}` |
| 21 | [El Coro de Treinta Voces](voces/CONTEXTO.md) — `Coro_Treinta_Voces.zip` | Forense de audio / tonos duales (nibbles) | ✅ resuelto | `flag{ejemplo}` |
| 22 | [Funa en el Bloc C](blocc/CONTEXTO.md) — `<host>` | Web / JWT `alg:none` + escalada de rol | ✅ resuelto | `flag{ejemplo}` |
| 23 | [Credencial prestada](cookies/CONTEXTO.md) — `<host>` | Web / cookie de alcance manipulable (BAC) | ✅ resuelto | `flag{ejemplo}` |
| 24 | [La Hermandad de las Sombras](sombras/CONTEXTO.md) — `fiesta-sombras-2026` (GitHub) | OSINT + ZIP anexado a JPEG + César | ✅ resuelto | `flag{ejemplo}` |
| 25 | [El Archivo Imposible](imposible/CONTEXTO.md) — `El_Archivo_Imposible.zip` | Estego / polyglot PNG+ZIP + gzip + ASCII85 + ZIP cifrado | ✅ resuelto | `flag{ejemplo}` |
| 26 | [El Chino — Misión Fotito](chino/CONTEXTO.md) — `interceptacion.txt` | Crypto / inversión + Vigenère (clave `COLINA`) | ✅ resuelto | `flag{ejemplo}` |
| 27 | [PagoAustral — El bono fantasma](austral/CONTEXTO.md) — `PagoAustral.zip` | Crypto / reutilización de keystream (two-time pad) | ✅ resuelto | `flag{ejemplo}` |
| 28 | [Registro Fantasma](fantasma/CONTEXTO.md) — `Registro_Fantasma.zip` | Forense / correlación proxy+backend + base64url + deflate | ✅ resuelto | `flag{ejemplo}` |
| 29 | [Memoria](memoria/CONTEXTO.md) — `Memoria.zip` | Estego / JPEG+ZIP anexado + QR + binario ASCII | ✅ resuelto | `flag{ejemplo}` |
| 30 | [Centinela](centinela/CONTEXTO.md) — `eventos.log` (CEF UniFi) | Forense de red / correlación de amenazas + base64 | ✅ resuelto | `flag{ejemplo}` |
| 31 | [Pirata 2 — Acta de Henry Every](pirata2/CONTEXTO.md) — `Pirata_2.zip` | Forense de DOCX / texto blanco en encabezado y pie | ✅ resuelto | `flag{ejemplo}` |
| 32 | [Cabecera Perdida](cabecera/CONTEXTO.md) — `fragmento_0317.bin` | Forense / reparación de firma PNG + payload hex | ✅ resuelto | `flag{ejemplo}` |
| 33 | [Puerta Abierta](intruso/CONTEXTO.md) — `intruso.pcap` | Forense de red / FTP brute force + exfiltración | ✅ resuelto | `flag{ejemplo}` |
| 34 | [Observa](observa/CONTEXTO.md) — `Observa.zip` | Forense / ZIP cifrado + firma DOCX dañada + texto blanco | ✅ resuelto | `flag{ejemplo}` |
| 35 | [El audio de la profesora Ximena](35-audio-profe-ximena/CONTEXTO.md) — 4.º C | Web / forense de app (chat, mensaje borrado) | 🚧 en curso | *(pendiente)* |
| 36 | [Documento Intervenido](intervenido/CONTEXTO.md) — MC-0421 | Forense de DOCX / base64 → ZIP → hex en `customXml` | ✅ resuelto | `flag{ejemplo}` |
| 37 | [Fresia](fresia/CONTEXTO.md) — Kimün / OVA boot2root | Boot2Root / credenciales filtradas (backup público + script de backup) | ✅ resuelto | USER: `flag{ejemplo}` · ROOT: `flag{ejemplo}` |
| 38 | [Las Veinte Puertas](puertas/CONTEXTO.md) — `Veinte_Puertas.zip` | Misc / grafo de sellos (3s+7 mod 17) + lectura por columnas | ✅ resuelto | `flag{ejemplo}` |
| 39 | [Operación Salitre](salitre/CONTEXTO.md) — SAL-16 / `Operacion_Salitre.zip` | Forense / correlación cámara-bitácora-rastreo-accesos + AES-256-CTR | ✅ resuelto | `flag{ejemplo}` |
| 40 | [Apocalipsis — Archivo Communio](boot2root/CONTEXTO.md) — `Apocalipsis.zip` | Boot2Root / backdoor en plugin WP + script sudo escribible | ✅ resuelto (offline) | USER: `flag{ejemplo}` · ROOT: `flag{ejemplo}` |
| 41 | [Un Byte Más](byte/CONTEXTO.md) — `un_byte_mas` / `<host>:3206` | Pwn / off-by-one sobre puntero de callback | 🚧 exploit local OK — host caído | *(pendiente)* |
| 42 | [El Susurro del Conde](susurro/CONTEXTO.md) — `ChismeAudio.wav` | Forense de audio / espectrograma + LSB Base64 + XOR | ✅ resuelto | `flag{ejemplo}` |
| 43 | [Bodega de farmacia](codigodemarte20261113/bodega-farmacia/CONTEXTO.md) — `203.0.113.10:8005` | Web / lógica de negocio (cantidad negativa → presupuesto) | ✅ resuelto | `flag{ejemplo}` |
| 44 | [Consola SICH](codigodemarte20261113/consola-sich/CONTEXTO.md) — `203.0.113.10:8007` | Web / JWT `alg: none` + escalada de rol | ✅ resuelto | `flag{ejemplo}` |
| 45 | [Sistema de avisos internos](codigodemarte20261113/avisos-internos/CONTEXTO.md) — `203.0.113.10:8008` | Web / SSTI Jinja2 (`{{config}}`) | ✅ resuelto | `flag{ejemplo}` |
| 46 | [Portal de acceso clínico](codigodemarte20261113/portal-clinico/CONTEXTO.md) — `203.0.113.10:8001` | Web / recon (`robots.txt` + backups expuestos) | ✅ resuelto | `flag{ejemplo}` |
| 47 | [Pharmatek](codigodemarte20261113/pharmatek/CONTEXTO.md) — `<host>:27370` | Web / secretos en el frontend (SPA + source maps) | ✅ resuelto | `flag{ejemplo}` |
| 48 | [Credencial digital del personal](codigodemarte20261113/credencial-digital/CONTEXTO.md) — `203.0.113.10:8002` | Web / cookie sin firma (rol editable) | ✅ resuelto | `flag{ejemplo}` |
| 49 | [Sistema central de recetas](codigodemarte20261113/recetas/CONTEXTO.md) — `203.0.113.10:8004` | Web / SQLi + filtro evadible (SQLite) | ✅ resuelto | `flag{ejemplo}` |
| 50 | [Archivo de historias clínicas](codigodemarte20261113/historias-clinicas/CONTEXTO.md) — `203.0.113.10:8006` | Web / path traversal (`....//`, filtro no recursivo) | 🚧 en curso — host sin respuesta | *(pendiente)* |
| 51 | [NexoDesk: asistente corrupto](codigodemarte20261113/nexodesk/CONTEXTO.md) — `203.0.113.10:8081` | Web / LLM + secreto fuera del contexto (attestation) | ✅ resuelto | `flag{ejemplo}` |
| 52 | [Lumen Flow](codigodemarte20261113/lumen-flow/CONTEXTO.md) — `203.0.113.10:8083` | Web / Q-learning + envenenamiento de recompensa | ✅ resuelto | `flag{ejemplo}` |
| 53 | [HIS: Historial Clínico Electrónico](codigodemarte20261113/his-historial-clinico/CONTEXTO.md) — `<host>:24235` | Auditoría web / GraphQL: `createUser` sin auth, IDOR de `resetToken`, JWT hardcodeado, SSTI (RCE) | ✅ resuelto y auditado | `flag{ejemplo}` |

## Historial

### 2026-11-13 — Desafío 53 «HIS: Historial Clínico Electrónico» resuelto y auditado — Código de Marte
- Objetivo `http://<host>:24235` (Express + Apollo GraphQL; enrutado por `Host: historial-clinico.internal`).
- Hallazgos críticos: `createUser` sin autenticación y con rol controlable (se creó una cuenta IT); IDOR en `profile(id)` que devuelve `resetToken` de cualquier usuario + `changePassword` sin autenticación; secreto JWT por defecto (`his-jwt-s3cr3t-hospital-eloisadiaz-2026`); SSTI en la plantilla de correo (Handlebars) vía `updateEmailConfig` + `sendTestEmail` → `child_process.execSync` (RCE).
- RCE usada para copiar `/flag_*` a `/app/public/` y leerla por HTTP; también se extrajo el código fuente del contenedor (`/app/src`) para el informe.
- Flag: `flag{ejemplo}`.
- Herramienta: `codigodemarte20261113/his-historial-clinico/scripts/solve.py`; evidencia y código fuente en `.../evidence/`.
- Instancia compartida: se restauró la plantilla original y se borraron los archivos temporales; quedan usuarios creados por la PoC.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261113-140232`.

### 2026-11-13 — Desafío 52 «Lumen Flow» resuelto — Código de Marte
- Objetivo `http://203.0.113.10:8083` (Flask + SPA; planta logística con Q-learning tabular).
- Recon: `GET /api/overview` expone `target` (ENV-900 en `recepcion|alta|baja`), tabla Q, historial de actualizaciones y `model` (alpha 0.25, gamma 0.8). `POST /api/replays` + `POST /api/replays/<id>/feedback` cierran episodios; `POST /api/simulation/start|resolve` ejecutan la prueba.
- Camino: el `observed_time` del feedback lo aporta el cliente y define la recompensa. Cerrar episodios de `recepcion|alta|baja` como `liberar` con `observed_time=5` y `scan_errors=0` produce `reward=4.0`; tras ~6 episodios `Q(liberar)` supera a `Q(retener)=4.5` y la decisión del envío cambia a `liberar`. Al resolver la simulación el paquete se desvía (`desvio_de_carga`) y `resolve` devuelve la bandera.
- Flag: `flag{ejemplo}`.
- Señuelos: `/static/audit-cache.js` (Base64 + XOR 57) → `flag{ejemplo}` y `flag{ejemplo}`.
- Herramienta: `codigodemarte20261113/lumen-flow/scripts/solve.py`; evidencia en `.../evidence/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261113-125534`.

### 2026-11-13 — Desafío 51 «NexoDesk: asistente corrupto» resuelto — Código de Marte
- Objetivo `http://203.0.113.10:8081` (Flask + Ollama; NexoDesk "centro de operaciones").
- Recon: `/api/chat`, `/api/tickets`, `/api/conversations/<id>`, `/api/status`, `/api/assistant/attestation`. El asistente responde con `[CORRUPTO]`/`[CORRUPTED]` y a veces agrega `ref xor b64 …` (señuelo `flag{ejemplo}`).
- Camino: el HTML lleva una nota ofuscada (`data-nd-obfuscated`, Base64 + XOR `0x39`) que apunta a **`/api/assistant/attestation`**. Ese endpoint devuelve `{"codec":"xor-b64","key":90,"payload":"GR4X…"}`; Base64 + XOR 90 → token de recuperación, servido fuera del contexto del modelo.
- Flag: `flag{ejemplo}` (variante `cdm{…}` si la plataforma es sensible a mayúsculas).
- Señuelos: `flag{ejemplo}` (conversación `USR-ARCHIVE`) y `flag{ejemplo}` (línea `ref`).
- Herramienta: `codigodemarte20261113/nexodesk/scripts/decode.py`; evidencia en `.../evidence/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261113-124853`.

### 2026-11-13 — Desafío 50 «Archivo de historias clínicas» — EN CURSO
- Objetivo `http://203.0.113.10:8006`. Visor `/ver?doc=`; el filtro hace `doc.replace("../","")` una sola vez y valida contención en `/app` con `realpath`.
- Bypass confirmado: `....//app.py` (y `....//Dockerfile`) → se leyó el **código fuente** de la app y su Dockerfile (Python/Flask 3.1.3, gunicorn, `WORKDIR /app`, usuario `ctf`).
- Las historias reservadas estarían en `/app/confidencial`, pero no se encontró el nombre del archivo; se descartó la fuerza bruta de nombres (no era el camino).
- **Bloqueo**: el servicio 8006 dejó de responder HTTP (los demás puertos del host sí respondían); probablemente saturación de los 2 workers o contenedor a reiniciar.
- Pendiente al reanudar: enumerar sin adivinar (`....//.git/index`, logs del repo, artefactos del build) y leer el archivo real de `confidencial/`.

### 2026-11-13 — Desafío 49 «Sistema central de recetas» resuelto — Código de Marte
- Objetivo `http://203.0.113.10:8004` (Flask + SQLite). Login `usuario`/`clave` «protegido por el filtro anti-inyección del SICH».
- Recon: `admin' #` devuelve `unrecognized token: "#"` (SQLite, `#` no es comentario); la consulta concatena la entrada.
- Filtro = lista negra **sensible a mayúsculas**: `' OR 1=1 --` y `' UNION SELECT …` se bloquean, pero `' or 1=1 --`, `' Or 1=1 --` y `'/**/or/**/1=1--` pasan.
- Bypass: `usuario=' or 1=1 --` anula el `AND` y devuelve la primera fila (jefatura) → credencial con la flag.
- Flag: `flag{ejemplo}`. Señuelo: comentario HTML con `soporte/Hosp2029-tmp` (deshabilitado).
- Herramienta: `codigodemarte20261113/recetas/scripts/solve.py`; evidencia en `.../evidence/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261113-121237`.

### 2026-11-13 — Desafío 48 «Credencial digital del personal» resuelto — Código de Marte
- Objetivo `http://203.0.113.10:8002`. `POST /` con `usuario=juan` → 302 a `/panel` y cookie `sich_sesion` (**JSON en Base64, sin firma**): `{"usuario":"juan","rol":"visitante","token":"…"}`; el propio token decodifica «solo codificada en base64, el rol es editable».
- Exploit: cambiar `rol` a `jefatura` y re-codificar en Base64 → `GET /panel` muestra «Expediente clasificado desbloqueado» + flag. `jefe` y `admin` no sirven; la comparación es insensible a mayúsculas.
- Flag: `flag{ejemplo}`.
- Trampa de herramienta: con `requests`, pasar `cookies=` junto al cookie del jar envía **dos** `sich_sesion` y el servidor toma el primero (visitante); hay que limpiar el jar o mandar el header `Cookie` a mano.
- Herramienta: `codigodemarte20261113/credencial-digital/scripts/solve.py`; evidencia en `.../evidence/`.

### 2026-11-13 — Desafío 47 «Pharmatek» resuelto — Código de Marte
- Objetivo `http://<host>:27370` (nginx + SPA Vite/React). Enunciado: «Ingresa y reclama tu bandera».
- Recon: `index-DxM6ovw5.js` referencia los chunks por página; los del portal son `page-Crn_T1qp.js` (login) y `page-C5Ytzon-.js` (dashboard). Ambos publican **source maps**.
- Login **sin backend**: compara contra `{username:"medico",password:"neurotech2024"}` y guarda `localStorage.isAuthenticated="true"` (la propia página anuncia el usuario `medico`).
- El dashboard solo valida `localStorage` (falsificable con una línea) y trae la flag en el campo `flag` del paciente `NX-005` (clase `text-gray-700/30`, casi invisible).
- Flag: `flag{ejemplo}`. Barrido de todos los assets y mapas: única aparición, sin señuelos.
- Herramienta: `codigodemarte20261113/pharmatek/scripts/solve.py`; evidencia en `.../evidence/` (HTML, bundle, chunk de login, chunk del dashboard, cabecera del `.map`).
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261113-120055`.

### 2026-11-13 — Desafío 46 «Portal de acceso clínico» resuelto — Código de Marte
- Objetivo `http://203.0.113.10:8001`. Portal de login (`u`/`p`) con dos comentarios HTML: credenciales `tecnico/Hosp2029` «desactivadas» (señuelo) y un Base64 que dice «el respaldo bueno no es el de ejemplo».
- `robots.txt` (pista de 1994) enumera `/panel-admin/`, `/phpmyadmin/` y **`/respaldo-sich/`**; los dos primeros son 403/404, el tercero tiene **listado de directorio abierto**.
- Archivos: `config.sample.bak` («plantilla de ejemplo», señuelo → `flag{ejemplo}`) y `sich.conf.bak` (2031-03-14, `entorno=produccion`, host `10.20.0.5`) con `token_integracion=flag{ejemplo}`.
- Flag: `flag{ejemplo}`. Login con `tecnico/Hosp2029` → «usuario o clave incorrectos».
- Herramienta: `codigodemarte20261113/portal-clinico/scripts/solve.py`; evidencia HTTP en `.../evidence/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261113-115645`.

### 2026-11-13 — Desafío 45 «Sistema de avisos internos» resuelto — Código de Marte
- Objetivo `http://203.0.113.10:8008` (Flask/Jinja2 + gunicorn); campo `mensaje` (200 chars) publicado en `<pre>[AVISO SICH] …</pre>`.
- Vulnerabilidad: **SSTI** — el mensaje se pasa a `render_template_string`. `{{7*7}}` → `49` y `{{7*'7'}}` → `7777777` confirman Jinja2.
- Exploit: `{{config}}` vuelca la configuración de Flask: `NOMBRE_MODULO`, `VERSION`, `TOKEN_DEMO` (`flag{ejemplo}`, señuelo) y **`CLAVE_SICH`** = flag.
- Entorno `SandboxedEnvironment`: `{{cycler.__init__.__globals__.os.popen('id').read()}}` → «Bloqueado :: el sandbox del SICH rechazo la operacion»; no hizo falta RCE.
- Flag: `flag{ejemplo}`.
- Herramienta: `codigodemarte20261113/avisos-internos/scripts/solve.py`; evidencia HTTP en `.../evidence/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261113-115354`.

### 2026-11-13 — Desafío 44 «Consola SICH» resuelto — Código de Marte
- Objetivo `http://203.0.113.10:8007`. `POST /` con `usuario=invitado` → 302 a `/consola` + cookie `sich_jwt` (HS256, payload `{"usuario":"invitado","rol":"visitante"}`).
- Pista del HTML: «el secreto HS256 se rota cada hora, un ataque de fuerza bruta a la firma es inutil» → el ataque no va por la clave.
- Vulnerabilidad: el servidor confía en el header del token y acepta **`alg: none`** con firma vacía (`none`, `None`, `NONE`).
- Exploit: token forjado `{"alg":"none"}` + `{"usuario":"admin","rol":"admin"}` → `GET /consola` con `Cookie: sich_jwt=<forjado>` habilita los comandos de administrador y muestra la flag.
- Flag: `flag{ejemplo}`. HS256 con firma inventada sí se rechaza («firma rechazada por el SICH»).
- Herramienta: `codigodemarte20261113/consola-sich/scripts/solve.py`; evidencia HTTP en `.../evidence/`.
- Reorganización: el evento quedó como carpeta contenedora (`codigodemarte20261113/README.md`) con un subdirectorio por reto: `bodega-farmacia/`, `consola-sich/`, `avisos-internos/`.

### 2026-11-13 — Desafío 43 «Bodega de farmacia» resuelto — Código de Marte
- Evento/carpeta: `codigodemarte20261113`; objetivo `http://203.0.113.10:8005` (Flask + gunicorn).
- Estado en cookie `session` firmado (Base64 legible): `{"inventario":{"gasa":0,"jeringa":0,"llave":0},"presupuesto":100}`. Precios: gasa 20, jeringa 15, llave 999.
- Vulnerabilidad: el formulario limita `cantidad` con `min=1 max=99` solo en HTML; el servidor hace `int(cantidad)` y `presupuesto -= cantidad*precio` sin validar el signo.
- Exploit: `item=gasa&cantidad=-50` → presupuesto 100 − (−50×20) = **1100**; `item=llave&cantidad=1` → presupuesto 101 y `inventario.llave=1`; `GET /` imprime la flag.
- Flag: `flag{ejemplo}`.
- Trampa de método: los POST responden **302** con el nuevo `Set-Cookie`; seguir la redirección descartando la cookie hace parecer que el estado no cambia (usar `curl -c/-b` o `requests.Session`).
- Descartado: forja del cookie (itsdangerous), rutas ocultas, `codigo=AUTH-1` (rechazado).
- Herramienta: `codigodemarte20261113/scripts/solve.py`; evidencia HTTP en `codigodemarte20261113/evidence/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261113-114848`.

### 2026-10-24 — Desafío 42 «El Susurro del Conde» resuelto
- Evidencia: `ctf/susurro/ChismeAudio.wav` (640.044 B, SHA256 `7CCD2A90…896011`), PCM 16-bit mono 44,1 kHz, 7,256 s, sin chunks extra.
- Secreto «para los ojos»: texto en el espectrograma (2,4–4,1 kHz) → `KEY: SweetBlood` (llave base).
- Secreto «para los oídos»: el **bit 0** de cada muestra PCM, empaquetado MSB-first, empieza con el Base64 `ByUkKDUBOHZLNyNECRAaKQVeVzsWGVYJKw8JREJULg==` (44 chars) + `0x00`.
- Decodificado: 31 B `07252428…5442e`; XOR con la variante leet **`SweetBl00d`** → `flag{ejemplo}`. Con `SweetBlood` el XOR se rompe en la posición 7 (falta el `0`).
- Descartado: DeepSound/steghide, bits 1–3, DTMF, FSK en la cola (100,03 Hz constante), Morse en las 14 ráfagas (son los glifos del texto).
- Herramientas: `susurro/solucion/descifrar_susurro.py`; artefactos en `susurro/work/`; análisis previo en `susurro/RESOLUCION_SUSURRO.md`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261024-182942`.

### 2026-10-24 — Desafío 41 «Un Byte Más» — exploit validado, flag remota pendiente
- Evidencia: `ctf/byte/un_byte_mas` (686.240 B, SHA256 `705e81f1…d8eebbf0`), ELF64 estático stripped, no PIE, NX, sin canary.
- Vulnerabilidad: `read(0, rsp, 0x21)` sobre buffer de 32 en `0x4018c0`; el byte 33 sobrescribe el byte bajo del puntero de callback `[rsp+0x20] = 0x478100`.
- Payload: `b"A"*32 + b"\x50"` → `0x478150` → NOP-sled `.callbacks` → `jmp 0x401991` → `fopen("/tmp/flag")`.
- Validado en local con `/tmp/flag` de prueba (`flag{ejemplo}`).
- Remoto **inaccesible**: `<host>` → `203.0.113.10`; timeout en 3206 (y 22/80/443) desde Kali y Windows; check-host.net 5 nodos (DE/IL/IT/TR/US) todos `Connection timed out` (`check-report/533185b4k4c6`). Control de red OK.
- Herramienta: `byte/solucion/solve.py`; artefactos en `byte/work/`. Flag pendiente hasta que la instancia vuelva a estar arriba.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261024-175435`.

### 2026-10-24 — Desafío 40 «Apocalipsis — Archivo Communio» resuelto (offline)
- Evidencia: `ctf/boot2root/Apocalipsis.zip` (203.0.113.10 B) → OVA con SHA-256 `5d4c9625…1f55fd` ✔ (Ubuntu_64, 2 vCPU, 2 GB).
- Sin VirtualBox: `qemu-img` VMDK→raw y montaje read-only de la partición 1 (offset 1074790400) para forense offline.
- USER: `/home/<usuario>/user.txt` → `flag{ejemplo}`.
- ROOT: `/root/root.txt` → `flag{ejemplo}`.
- Cadena reconstruida: `.git` expone el commit `aa84d56` que añade la puerta trasera `_arve_uc_init` al plugin ARVE (`sha256(token)=dd0d16d1…e73c`); credenciales de BD en `wp-config.php`; usuario `ezequiel` con shell restringida; sudo NOPASSWD sobre `/opt/communio/scripts/respaldo_archivo.sh` **escribible** (777).
- Señuelo: `.state.json` → Base64 `flag{ejemplo}` (no es la ROOT canónica).
- No se crackeó el token ni se ejecutó la ruta web en vivo; banderas por lectura directa del disco.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261024-175435`.

### 2026-10-24 — Desafío 39 «Operación Salitre» (SAL-16) resuelto
- Evidencia: `ctf/salitre/Operacion_Salitre.zip` (21.105 B, SHA256 `C3E6ECEC…58E875`), extraído en `salitre/evidencias/` (9 archivos: PNG, PDF, 4 CSV, 3 TXT).
- Hora: CAM-07 marca `03:17`, pero la bitácora la declara **adelantada** 11 min → `03:06` local; huso UTC-03:00 del informe → **`2026-01-16T06:06Z`**.
- Cruce: a las 03:06 locales el único acceso en CAM-07 (Tocopilla, muelle 3) es el alias **`cormoran`** (PORT-17, habilitación extraordinaria). A las 06:06Z hay dos zarpes: `Arauco Star` (**Mejillones** 3) y **`Nordkapp`** (Tocopilla 3); puerto/muelle descartan al primero.
- Manifiesto: `Nordkapp` → folio **A-1193**, contenedor **NYKU9087**. Sesión DNS `_meta/_p01..p04.cormoran.a1193`.
- Llave `SHA256("A-1193|NYKU9087|cormoran|2026-01-16T06:06Z")` = `2eb4e318…7baffc94`; AES-256-CTR con IV `2f369d81…ca376c9e`; SHA-256 del plano verificado `06a831b2…c54ef47e`.
- Flag: `flag{ejemplo}`.
- Señuelos: las 6 sesiones descifran y validan SHA-256; solo `cormoran` trae la flag y `azul` (A-1192 / Arauco Star) trae un acta de «desvío hacia muelle secundario». Llaves con hora sin corregir, hora local como UTC, folio en minúsculas o alias en mayúsculas fallan el SHA-256.
- Herramientas: `salitre/solucion/descifrar_sesion.py` y `salitre/solucion/verificar_sesiones.py`; artefactos en `salitre/work/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261024-173811`.

### 2026-10-24 — Desafío 38 «Las Veinte Puertas» resuelto
- Evidencia: `ctf/puertas/Veinte_Puertas.zip` (1.519 B, 4 TXT/CSV sin cifrar).
- Regla del controlador: `sello_siguiente = (3*sello + 7) mod 17`; entrada puerta 01, 7 puertas, dos salidas (IZQ/DER), solo una conserva el sello.
- Camino único: **01 → 06 → 12 → 03 → 17 → 10 → 05** (la 05 tiene estado `SALIDA`). Las puertas 02 y 19 son señuelos («marcos nuevos»).
- Lectura: bandas de 5 símbolos como **columnas** en orden de visita, luego 5 **filas** de izquierda a derecha.
- Flag: `flag{ejemplo}`.
- Herramienta: `puertas/solucion/resolver_puertas.py`; artefactos en `puertas/work/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261024-134251`.
### 2026-10-24 — Desafío 37 «Fresia» (Kimün) resuelto — BOOT2ROOT 2/2
- Evidencia: `ctf/fresia/Fresia.zip` (926 MB) → `fresia.ova` (SHA256 `4e788b90…a9fc6c` ✔); Ubuntu 24.04.4, 2 vCPU/2 GB, disco 16 GB.
- **Despliegue**: VirtualBox no instalado → VMware Workstation 16.1.2 + `ovftool --lax --diskMode=monolithicSparse`.
- **Bloqueo de red resuelto**: el OVA declara `enp0s3` (nombre de NIC de VirtualBox) y en VMware la NIC cambia de nombre → netplan nunca aplicaba DHCP. Fix: `qemu-img` a raw, montaje `losetup -P`, `/etc/netplan/99-ctf-any.yaml` con `match: name: "en*"`, reempaquetado a vmdk (`Fresia-disk1.vmdk.orig` conservado).
- **Acceso**: VM en NAT (`192.168.226.129`); Kali (WSL2 mirrored) no llega a VMnet8 y `netsh portproxy` exige admin → relay TCP en espacio de usuario `solucion/relay_tcp.py` (`8080→80`, `2222→22`, `3306→3306`, `8443→443`).
- **USER**: `/old/backup_2019.sql` público con hash bcrypt de `lautaro` → `caupolican` (tema mapuche + años, 6 s). Login admin en Dolibarr OK (302 a `admin/index.php`). Flag `flag{ejemplo}` (contraseña de BD de `conf.php` reutilizada, `D0l_Adm1n_2024`).
- **ROOT**: `backup_db.sh` de galvarino con la clave en claro (`mysqldump -u root -p'Tr4bajo_1nt3rn0_2024'`); verificada contra el hash yescrypt `$y$` de `/etc/shadow` con `crypt()` de Perl. Flag `flag{ejemplo}`.
- Nota: la RCE `dol_eval()` de la pista es real pero la instancia está a medio instalar (`setupnotcomplete`); el reto se resuelve encontrando credenciales.
- Artefactos: `fresia/work/` (backup SQL, conf.php, backup_db.sh, shadow, flags, configs) y `fresia/solucion/` (despliegue, fix netplan, relay, recon, crackers).
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261024-134105`.
### 2026-10-24 — Desafío 36 «Documento Intervenido» (MC-0421) resuelto
- Evidencia: `ctf/intervenido/documento_intervenido_0421.docx` (56.219 B, SHA256 `C5FE03C2…DB6AE9`), 19 partes OOXML.
- El texto visible es coherente; la anomalía está en `customXml/item1.xml` (`urn:trama:cache:v1`, canal **VF-12**), con un `<cache encoding="base64">` que es un **ZIP** (`UEsDBBQ` = `PK\x03\x04`).
- El ZIP interno contiene `registro_0421.dat` (`TRAMA_RECOVERY_CACHE`, `source=VF-12`, `timestamp=04:21:17`, `encoding=hex`) con un `payload` hex de 50 bytes.
- Flag: `flag{ejemplo}`.
- Herramienta: `intervenido/solucion/extraer_intervenido.py`; artefactos en `intervenido/work/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261024-130836`.

### 2026-10-24 — Desafío 35 «El audio de la profesora Ximena» (4.º C) iniciado
- Enunciado: audio de la profesora Ximena al grupo del 4.º C la noche previa a una prueba; un mensaje desapareció y el colegio conservó una copia del sistema para la investigación.
- Credenciales: `alumno` / `4toC2026!`. Cookies entregadas: `session=eyJsb2dnZWRfaW4iOnRydWUsInVzdWFyaW8iOiJhbHVtbm8ifQ.atyspg.-DiMmm_AajtuwE8TaV4orLiHZJY` (payload `{"logged_in":true,"usuario":"alumno"}`) y `trama_session=fcWp5lhLzYJrPaY6uVHgvPAkqNqrRd1yz242FO_SbGXVenGLENRP87mnh95naAQU`.
- DNS de `*.chals.io` verificado como **comodín** (`<host>` → 203.0.113.10/116), por lo que el host del reto no se puede descubrir por resolución: queda pendiente que el usuario entregue la URL.
- Carpeta creada: `ctf/35-audio-profe-ximena/` (`CONTEXTO.md`, `solucion/`, `work/`, `flags/`).
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261024-113424`.

### 2026-10-23 — Desafío 34 «Observa» (Expediente 01) resuelto
- Evidencia: `ctf/observa/Observa.zip` (12.135 B, SHA256 `711f016f...9af02216`) con `por_aqui.docx` **cifrado ZipCrypto** (12.862 B, CRC `5e1dce6e`).
- Contraseña: `zip2john` + `john --stdin` con rockyou → **`jhonny`** (CRC del DOCX descifrado coincide, clave correcta).
- Segundo ocultamiento: el DOCX arranca con `50 15 78 04` en vez de `PK\x03\x04`; reparando esos 4 bytes el OOXML se abre (10 partes).
- Tercer ocultamiento: en `word/document.xml` el texto está en **blanco** (`w:color FFFFFF`, dos runs): «La bandera es flag{ejemplo}».
- Flag: `flag{ejemplo}`.
- Herramienta: `observa/solucion/resolver_observa.py` (descifra, repara firma y extrae runs blancos); artefactos en `work/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-204617`.

### 2026-10-23 — Desafío 33 «Puerta Abierta» (intruso.pcap) resuelto
- Evidencia: `ctf/intruso/intruso.pcap` (147 paquetes, 3,99 s, 2026-10-19 15:33:11; SHA-256 `38e09b5c...6807c1c8`, coincide con `SHA256SUMS (2).txt`).
- Reconocimiento: barrido previo desde `203.0.113.37` a `198.51.100.10` en 22/23/80/443/445/3389; servidor `CentinelaFTP` en 21.
- Fuerza bruta: 5 fallos (`admin:admin`, `admin:123456`, `root:toor`, `soporte:soporte`, `soporte:Soporte2024`) y acceso válido con **`soporte:Verano2024`** (`230`).
- Exfiltración: `LIST` + `RETR credenciales.txt` por FTP pasivo (stream 14, 292 B); el contenido incluye credenciales VPN/panel/BD y la flag.
- Respuesta correcta: **203.0.113.37 | FTP/21 | 5 intentos fallidos | soporte / Verano2024 | credenciales.txt**.
- Flag: `flag{ejemplo}`.
- Herramienta: `intruso/solucion/analizar_intruso.py`; archivos recuperados en `work/credenciales.txt` y `work/listado.txt`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-204028`.

### 2026-10-23 — Desafío 32 «Cabecera Perdida» resuelto
- Evidencia: `ctf/cabecera/fragmento_0317.bin` (78.849 B). `file` lo ve como `data` porque el **primer byte de la firma PNG está a 0x00** (`00 50 4E 47 0D 0A 1A 0A` en vez de `89 50 4E 47 …`).
- Reparación: restaurar `data[0]=0x89` → PNG 1600×900; los CRC de `IHDR`, dos `IDAT` e `IEND` dan OK y no hay datos tras `IEND` (integridad total).
- Contenido: panel de terminal del nodo VF-0317 con volcado hex (`PAYLOAD // BLOQUE 03`) que decodifica a `flag{ejemplo}`.
- Nota: el payload está renderizado en la imagen; se transcribió visualmente (OCR con tesseract confunde `5` y `2` en el font del panel).
- Herramienta: `cabecera/solucion/reparar_fragmento.py` (repara, valida CRC y decodifica); PNG reparado en `work/cabecera_restaurada.png`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-203411`.

### 2026-10-23 — Desafío 31 «Pirata 2 — Acta de Henry Every» resuelto
- `Pirata_2.zip` → `acta_henry_every.docx` (25 753 B). El cuerpo solo tiene el acta; el interés está en `word/header1.xml` y `word/footer1.xml` (un .docx es un ZIP).
- Cabecera: flag en texto **blanco (`w:color FFFFFF`, 8 pt)** → `flag{ejemplo}`.
- Pie: `38.776970` (mismo truco de color) = **fragmento de navegación DG-004** para Pirata 3.
- Revisado el resto del paquete OOXML: no hay más texto blanco/`vanish`/tamaño 1.
- Pendiente: falta `Pirata_1.zip` (DG-003) para cerrar Pirata 3.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-192758`.

### 2026-10-23 — Desafío 30 «Centinela» resuelto
- Evidencia `centinela/eventos.log` (20 512 B, 37 eventos CEF de UniFi, SHA-256 `5f690e59…c4f855` verificado contra `SHA256SUMS`).
- Cinco alertas en total; el incidente son los **4 eventos `OUTBOUND.C2.Beacon`** de **PC-RECEPCION** (MAC `02:00:5e:a1:4f:a2`) hacia **203.0.113.37:8443**, todos «detected and blocked». Ruido: `OUTBOUND.DNS.Policy` (PC-BODEGA), `OUTBOUND.Web.Reputation` (PC-RECEPCION→otra IP), `OUTBOUND.PortScan` (NB-GERENCIA).
- Cada beacon traía `cs1=<base64>` + `cn1=<índice>`; ordenando 1→4 y decodificando: `Y29y`+`dG9f`+`ZWxf`+`YmVhY29u` = **`corto_el_beacon`**.
- Flag: `flag{ejemplo}` (host en minúsculas, MAC últimos 4 = `4fa2`, IP con guiones bajos, 4 intentos, mensaje con sus guiones bajos).
- Script: `centinela/solucion/analizar.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-192308`.

### 2026-10-23 — Desafío 29 «Memoria» (Expediente 02) resuelto
- Evidencia: `ctf/memoria/Memoria.zip` (30.340 B, SHA256 `10afb5be...40c4135`) con `registro_memoria.jpg` (31.070 B, 500×333, EXIF de 2012).
- Polyglot: tras el marcador `FFD9` del JPEG (offset `0x6b37`) hay un **ZIP anexado** desde `0x6b39` con `respaldo_0317.png` (924×924).
- Capas: el PNG interno es un **código QR**; su contenido son **grupos de 8 bits ASCII** (`01001100 00110000 …`) que decodifican a `L0s_Recuerd0s_N0_Se_B0rr4n_C0n_Un_C4fe`.
- Flag: `flag{ejemplo}`.
- Herramienta: `memoria/solucion/resolver_memoria.py` (carving del ZIP, extracción del PNG, `zbarimg`, binario→ASCII); artefactos en `work/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-192154`.

### 2026-10-23 — Desafío 28 «Registro Fantasma» (Completo al Vapor) resuelto
- Evidencia `fantasma/Registro_Fantasma.zip` (5 173 B): `access.log` (backend tras proxy), `proxy_trace.csv` (resultado real + `flow`/`seq`), `parte_turno.txt` y `LEEME.txt`.
- Método: unir por `rid`, quedarse con `proxy_result=OK`, ordenar por `(flow, seq)` y **concatenar los `p` como texto base64url antes de decodificar** (hay trozos de 5 chars: el base64 está partido) y luego inflar el deflate resultante.
- Resultado por flujo: **FV-9D6 / CAJA-07** → `flag{ejemplo}`; señuelos: FA-8E3/CAJA-09 → `informe_de_caja_equivocado`, FW-7B1/CAJA-02 → `premio_de_prueba_no_valido`, FE-2C8/CAJA-07 (todo REJECT) → «PREPRODUCCION: ensayo de telemetria descartado».
- El flujo bueno es el de la caja del incidente (CAJA-07) y el único que obliga a descartar los `REPLAY`/`REJECT` (si se incluyen, el deflate se corrompe).
- Scripts: `fantasma/solucion/reconstruir.py`, `analizar.py`, `correlacion.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-192115`.

### 2026-10-23 — Desafío 27 «PagoAustral — El bono fantasma» resuelto
- Evidencia `austral/PagoAustral.zip` (713 B): `mi_sesion.txt` (128 B, texto plano), `mi_token.txt` y `token_gerencia.txt` (128 B cada uno en hex).
- Los tres miden 128 B → se dispone de un **par conocido (texto plano, cifrado)**. Los dos tokens comparten los primeros 8 y los últimos 16 bytes (C1^C2 empieza y termina en ceros) ⇒ **mismo keystream** (cifrado de flujo con clave/nonce reutilizados).
- Método: `keystream = C_mio XOR P_mio`; `P_gerencia = C_gerencia XOR keystream`.
- Descifrado: `usuario=gerencia;rol=interno;nota=flag{ejemplo};region=cl;mfa=on`.
- Scripts: `austral/solucion/conocido_plano.py` (solver) y `xor_sesion.py` (pruebas descartadas).
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-191732`.

### 2026-10-23 — Desafío 26 «El Chino se pierde en el Cajón del Maipo: Misión Fotito» resuelto
- Artefacto `chino/interceptacion.txt` (674 B): registro de radio simulado con el mensaje `}0e0t_4pu...{QHEAZICH .QITCQST NH VP GQMNLPIS ...` y 4 notas de calibración.
- Pistas: (1) invertir el mensaje completo; (2) clave = última palabra del destino «TERMAS DE COLINA» → **COLINA**; (3) clave repetida que **solo avanza con letras A-Z**; (4) signos, dígitos y guiones bajos se mantienen y no consumen clave.
- Se probaron XOR y Vigenère (±): solo **Vigenère restando** da texto legible: `FUIMOS POR UNA FOTO. HABIA NIEVE Y NOS QUEDAMOS EN UN REFUGIO. flag{ejemplo}`.
- Solver: `chino/solucion/resolver.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-191528`.

### 2026-10-23 — Desafío 25 «El Archivo Imposible» resuelto
- Evidencia: `ctf/imposible/El_Archivo_Imposible.zip` (12.635 B, SHA256 `cc6d42dc...f1d19e73`) con un único `archivo_imposible.png` (14.030 B, 640×360 RGB).
- Polyglot: el PNG es válido, pero tras el chunk `IEND` (offset `0x3554`) hay un **ZIP anexado** desde `0x355c` (`nivel1.zip`, 370 B). Los `tEXt` daban `pista=polyglot: png+zip` y `clave_nivel4=pr1sma_oculto`.
- Capas: `nivel1.zip` → `nivel2.gz` (249 B) → gunzip → 287 B de texto **ASCII85** → `a85decode` → `nivel3.zip` (236 B) con `flag.txt` (42 B) cifrado ZipCrypto.
- Contraseña: `pr1sma_oculto` (chunk `tEXt clave_nivel4`) abre `flag.txt`.
- Flag: `flag{ejemplo}`.
- Herramienta: `imposible/solucion/resolver_imposible.py` (cadena completa automatizada; artefactos por nivel en `work/`).
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-191443`.

### 2026-10-23 — Desafío 24 «La Hermandad de las Sombras» (fiesta-sombras-2026) resuelto
- OSINT: búsqueda en la API de GitHub (`search/repositories?q=fiesta-sombras-2026`) → `CondeCyberDracula/fiesta-sombras-2026` (rama `main`, descripción «Shall we dance?»), con un único `README.md` que incrusta dos imágenes de `user-attachments`.
- Imágenes: `imagen1.png` (975.303 B, sin payload) y `Pista_Invitacion.png` (36.916 B, en realidad **JPEG**).
- Estego: el JPEG tiene un **ZIP anexado tras el EOI** en el offset `0x8f92` (firma `PK\x03\x04`), con un único `secreto.txt` (40 B, sin cifrado ZIP): `flag{ejemplo}`.
- Cifrado: **César −3** (el prefijo `TRAMACTF` frente a `WUDPDFWI` lo delata) → `flag{ejemplo}`.
- Herramienta: `sombras/solucion/resolver_sombras.py` (descarga, carving del ZIP y César con validación de prefijo); artefactos en `work/`.
- Flag: `flag{ejemplo}`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-191018`.

### 2026-10-23 — Desafío 23 «Credencial prestada» (Asterion/Crimson) resuelto
- Portal de proveedores `https://<host>/login` con `proveedor01` / `Crimson-0826!`. Entrega dos cookies: `asterion_session` (Flask, firmada) y **`access_scope=vendor`** (texto plano, sin firma).
- Historia y pistas en `/portal` y `/documents`: la entrega **CL-7903** se cerró a las 03:12 y a las 03:18 se añadió un anexo y se cambió su clasificación; el anexo figura como «Restringido / No disponible para la organización actual».
- Vulnerabilidad: **el alcance lo decide el cliente**. `/documents/anexo-cl-7903` da 403 con `access_scope=vendor` y **200 con `access_scope=internal`** (probados 36 valores; `interno`, `admin`, `asterion`, etc. no funcionan).
- El anexo interno revela el Programa HELIX (HX-103) y el código de validación: `flag{ejemplo}`.
- Script: `cookies/solucion/scope_bruteforce.py`. No hay segunda flag: rutas de actividad/entregas/API devuelven 404.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-191008`.

### 2026-10-23 — Desafío 22 «Funa en el Bloc C» resuelto
- Portal `https://<host>/login` con `vecino_c204` / `Bloc2026!` (campos `usuario`/`password`; la cookie de sesión resultante es el JWT `vecino_token`, HS256, `role=vecino`).
- Pistas en el propio muro: «hay una publicación en borrador visible solo para administración» y «la sesión se puede editar así nomás… vi algo de `alg` y `none`». El `/perfil` confirma: «el servidor confía en lo que declara el campo `alg`».
- Exploit: JWT con **`{"alg":"none"}`** y payload `role=admin` (firma vacía) → `/denuncias` muestra `Rol actual: admin` y se habilita **`/denuncias/borrador`** (con el token de vecino: 403).
- El borrador contiene el «código de validación» = flag: `flag{ejemplo}`. `alg: none/None/NONE` se aceptan igual; HS256 con clave vacía se rechaza (no era clave débil, era la confusión de algoritmo).
- Scripts: `blocc/solucion/jwt_none.py`, `admin_token.py`, `buscar_borrador.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-190537`.

### 2026-10-23 — Desafío 21 «El Coro de Treinta Voces» resuelto
- Evidencia: `ctf/voces/Coro_Treinta_Voces.zip` (143.030 B, SHA256 `fc403ff3...b9e6223`); contiene `coro_30_tomas.wav` (PCM 16 bit mono 8 kHz, 10,5 s = **30 tomas de 0,35 s**), `hoja_del_afinador.txt` y `planilla_de_mezcla.csv`.
- Esquema: cada toma tiene **dos tonos** (grave 520+40k, agudo 1400+40k, k=0..F); el grave es el nibble alto y el agudo el bajo → un byte ASCII por toma. Solo 22 tomas son **MAESTRAS**; 8 son CALIBRACIÓN (03, 06, 12, 13, 15, 23, 25, 29) y se descartan.
- Método: FFT (Hann, 32.768 puntos) sobre la ventana 0,05–0,28 s de cada toma; pico en 480–1220 Hz y 1320–2080 Hz; índice `round((f−base)/40)`; reordenar las maestras según la columna `orden` de la planilla.
- Resultado: bytes `6c615f636f6e666573696f6e5f766572646164657261` → `la_confesion_verdadera`; el encabezado/llaves los aporta el formato oficial → flag `flag{ejemplo}`.
- Señuelos: las calibraciones decodifican a `_ 1 m _ p u a u`, verosímiles pero corruptores.
- Herramienta: `voces/solucion/decodificar_coro.py`; volcado completo en `work/salida_decodificada.txt`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-190245`.

### 2026-10-23 — Desafío 20 «La Feria del Persa» resuelto
- Sitio en `https://<host>`. Todo respondía **403** («debe iniciarse desde la plataforma TRAMA CTF»); no era bypass de cabeceras ni token de API de CTFd: la puerta es la **cookie `trama_session`** que entrega la plataforma al lanzar la instancia.
- Mapa: `/catalogo` (12 productos), `/buscar?q=` (formulario GET), `/opiniones`, `/ticket`. Las pistas están en las reseñas («el puesto 13», «encontré la wa escondida») y en el ticket («pregunta por el descuento VIP en el buscador… el sistema reconoce a los que preguntan bonito»).
- Vulnerabilidad: **SQLi en `q`** → `ORDER BY 5` OK / `6` error ⇒ 5 columnas; `UNION SELECT` confirma **SQLite 3.46.1**. Render: col2=nombre, col3=descripción, col4=precio, col5=categoría.
- Enumeración: `sqlite_master` → `productos`, `resenas`, **`puesto_13`** (`id, item, codigo_garantia`).
- Flag extraída de `puesto_13.codigo_garantia`: `flag{ejemplo}`.
- Trucos del solver: marcar la fila inyectada con `'ZZZCAT'` en la columna 5 (el `ORDER BY` del sitio mezcla la fila) y no usar comas en las expresiones (`group_concat(x)`, `char(124)`), porque rompen la lista del `UNION`.
- Solver: `feriapersa/solucion/resolver.py` (end-to-end) + `sqli.py`, `fase1.py`, `fase2.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-190048`.

### 2026-10-23 — Desafío 19 «La Lotería de los Condenados» resuelto
- Evidencia: `ctf/condenados/Loteria_Condenados.zip` (1.821 B, SHA256 `bb47a5ad...dc3915c3`); contiene `LEEME.txt` y `la_urna.txt` (10 boletos con mensajes Base64).
- Pista: `la_urna.txt` describe la marca de archivo `nodo_trama_2026` como presente en todos los registros y «necesaria para revisarlos» → es la clave de un XOR repetido.
- Método: por boleto, Base64 → XOR con `nodo_trama_2026` repetida. Los diez decodifican a frases legibles; solo el **boleto 03** tiene estructura de flag.
- Señuelos: «Esta no abre», «Mas suerte la proxima», «Te falta, mortal», «Frio. Muy frio.», «Tibio, tibio... frio otra vez», etc.
- Flag: `flag{ejemplo}`.
- Herramienta: `condenados/solucion/decodificar_boletos.py` (recorre los 10 y marca la flag).
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-185959`.

### 2026-10-23 — Desafío 18 «La Partitura Muda» resuelto
- Evidencia: `ctf/partitura/La_Partitura_Muda.zip` (427.691 B, SHA256 `41ff1835...e3195b6c`); contiene `LEEME.txt`, `partitura.wav` (36 s, PCM 16 bit mono 16 kHz) y `premio.zip` (ZipCrypto, `flag.txt` de 49 B, método *stored*).
- Hallazgo: el audio no tiene música ni voz útil; el **espectrograma** (`sox ... spectrogram`) dibuja `RESONANCIA2026` entre ~1,2 y ~2,8 kHz. Esa cadena es la contraseña de `premio.zip`.
- Apertura: `zipfile.read('flag.txt', pwd=b'RESONANCIA2026')` → flag. Alternativa no usada: *known-plaintext* con `bkcrack` usando el prefijo `TRAMACTF{`.
- Flag: `flag{ejemplo}`.
- Herramientas: `sox` (espectrogramas `work/spec.png` y `work/spec_wide.png`) y `python3 zipfile`; no se requieren servicios externos.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-185821`.

### 2026-10-23 — Desafío 17 «El Cielo Falsificado» (`ruta_espectral`) resuelto
- Evidencia: `ctf/rutaespecial/ruta_espectral` (14.496 B, SHA256 `3fde2a98...f2f9fd63`); ELF64 **PIE dinámico, stripped**. Pide un `Vector:` de exactamente **36 bytes** (`strlen == 0x24`) y muestra «Trayectoria sincronizada» o «Trayectoria perdida».
- Clave: `main` construye en la pila `CANAL47` con dos dwords (`0x414e4143` "CANA" + `0x37344c41` "AL47", solapando la 'A').
- Bucle de 36 iteraciones con ofuscación: índice de entrada `(7*i) mod 36`, clave `i mod 7`, suma de `i`, dos rotaciones dinámicas (`0xAAAA…` y `0xCCCC…`), mezcla con tablas `TA` (0x21a0) y `TB` (0x2180), XOR con `0x41+0x13*i` y `0xa7`; exige `r13b == 0`.
- Resolución: `(7*i) mod 36` es una permutación y la condición es byte a byte → se prueban 256 valores por índice (36×256) con solución única. La emulación exacta de las divisiones mágicas se validó con **GDB** (breakpoints en `0x1380`, `0x13af`, `0x13c6`, `0x13f8`, `0x13fe`), lo que descubrió el `add esi, edi` que faltaba antes de la primera rotación.
- Señuelo: la segunda etapa (checksum de `TB` y comparación con `T3` en `0x2140`) es **código muerto** — el checksum da `0xf5` y exige `0x24`; `T3` son 36 bytes no imprimibles (incluye `0x0a`), imposibles de teclear con `fgets`.
- Vector/flag: `flag{ejemplo}` (verificado en el binario: «Trayectoria sincronizada.»).
- Herramienta: `rutaespecial/solucion/resolver_vector.py` (lee `TA`/`TB` del propio ELF y resuelve); trazas en `work/trace*.gdb`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-184511`.

### 2026-10-23 — Desafío 16 «Eco Residual» (Canal 03) resuelto
- Artefacto: `eco_residual`, ELF x86-64 PIE *stripped* de 14 496 bytes (SHA-256 `62c26646…5850`); pide un «Token recuperado».
- `main` en `0x123f` (localizado vía `_start`): bucle de 32 iteraciones que arma el token en la pila con
  `token[i] = "TRAMA"[ tabla_B[i % 5] ] XOR clave[i]`, con `tabla_B = {3,1,4,0,2}` y clave de 32 bytes en `.rodata:0x21a0`.
- El texto índice resulta **`MRATA`** repetido (TRAMA leído por los índices), de ahí la flag: `flag{ejemplo}`.
- El `cmp [rsp+0xc], 999` del final es código muerto (la variable nace en `0x54` y nunca cambia): el programa retorna 0 incluso con el token correcto; el éxito se ve en `Acceso restaurado.`
- Solver: `ecoresidual/solucion/recuperar_token.py` (recalcula el token desde `.rodata` y lo valida ejecutando el binario).
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-184500`.

### 2026-10-23 — Desafío 15 «El Conde Ciber-Drácula» resuelto
- Charla ubicada por OSINT en `nodotrama.cl`: «El lado oscuro de la IA: cómo los atacantes ya usan IA contra personas y empresas en Chile», **Daniela Inostroza Mancilla**, 23 OCT 2026 18:00–18:45.
- Stream: `@NodoTramaOficial`, video **`GXwU585x0HA`** («NodoTrama CTF - Dia 1 - Jornada Tarde», inicio 18:49:22Z); charla en el offset 131–176 min.
- Truco clave: el manifiesto HLS es una ventana deslizante de 15 min, pero los segmentos son direccionables por `/sq/N/` → se pueden recuperar fragmentos antiguos del DVR (ffmpeg -ss no puede).
- Los 3 fragmentos Base64 están en la esquina inferior derecha de los slides (texto verde ~8 px): `VFJBTUFDVEZ7bDRz` + `X3MzbjRsM3NfeTRf` + `bjBfM3gxc3Qzbn0=` → `flag{ejemplo}`.
- Extracción: canal verde + autocontraste + ×10 + tesseract psm 7 con whitelist; validación semántica (`bDRz→l4s` encaja con `s3n4l3s`).
- Herramientas: `El_Conde_Ciber_Dracula/solucion/` (`barrido_dvr.sh`, `extraer_marcas.py`, etc.); 334 frames en `work/dvr/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-184100`.

### 2026-10-23 — Desafío 14 «Turno Fantasma» resuelto
- Evidencia: `ctf/turnofantasma/turno_fantasma` (686.168 B, SHA256 `0f6f5cc3...d8b696`); ELF64 estático, stripped, sin PIE y sin canary (NX sí). Misma plantilla que «Libro de Visitas», pero **otro bug**.
- Reconocimiento: el banner imprime `Turno retirado: 0x4018a5`; esa rutina huérfana abre y muestra `/tmp/flag`. `main` delega la atención en `0x401906`.
- Vulnerabilidad: `sub rsp, 0x48` + `read(0, rsp, 0x100)` → desbordamiento directo de la dirección de retorno (offset `0x48`).
- Exploit: ret2win → `b"A"*0x48 + p64(0x4018a5)`; al retornar se ejecuta la rutina retirada y se imprime la flag. Validado en local con `/tmp/flag` de prueba y luego contra `<host>:31547`.
- Herramienta: `turnofantasma/solucion/exploit_turno.py` (parsea el leak y arma el payload); transcripción en `work/salida_remota.txt`.
- Flag: `flag{ejemplo}`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-183751`.

### 2026-10-23 — Desafío 13 «Libro de Visitas» resuelto
- Evidencia: `ctf/librodevisitas/libro_visitas` (686.168 B, SHA256 `e1c77c33...704c587`); ELF64 estático, stripped, **sin PIE y sin canary** (NX sí).
- Reconocimiento: `strings` → `Casillero de aprobacion: %p`, `Casillero destino (hex):`, `Nota:`, `/tmp/flag` y un señuelo `flag{ejemplo}`.
- Vulnerabilidad: `main` hace `printf(nota, dest, dest+2)` (format string) y luego `cmp dword [0x4a6a90], 0x1337c0de` antes de leer `/tmp/flag`. El global de aprobación (`.bss`, `0x4a6a90`) se filtra con `%p`.
- Exploit: dos `%hn` con especificadores posicionales — `%2$49374c%1$hn%2$21081c%2$hn` — escriben `0xc0de` en `0x4a6a90` y `0x1337` en `0x4a6a92`, dejando el int en `0x1337c0de`; el programa imprime la flag.
- Validación local con `/tmp/flag` de prueba (`work/payload_local.txt` → `work/salida_local.txt`), luego ejecución remota contra `<host>:11071`.
- Herramienta: `librodevisitas/solucion/exploit_libro.py` (parsea el leak y construye los anchos a partir de las mitades de `0x1337c0de`).
- Flag: `flag{ejemplo}`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-183429`.

### 2026-10-23 — Desafío 12 «Señal Fantasma» (XimaTV / CentinelaOTA) resuelto
- Evidencia: `ctf/señalfantasma/SenalFantasma.ova` (761.137.664 B, SHA256 `2c18dd28...9ef59aeed` verificado).
- Despliegue: sin VirtualBox en el equipo → OVA extraída con `tar` a `C:\CTF_VMs\SenalFantasma\`, disco `streamOptimized` convertido con `vmware-vdiskmanager -t 0`, `.vmx` manual (Ubuntu_64, 2 vCPU, 2048 MB, LSILogic, e1000 host-only VMnet1). `virtualHW.version 19` no soportado → **18**. IP DHCP: **192.168.159.128** (`senalfantasma`).
- Acceso: WSL mirrored no ve VMnet1 → pivote SOCKS5 en el host (`solucion/socks5_pivot.py`, 127.0.0.1:1080). Puertos: 22 y 80.
- Fase 1 (USER): landing XimaTV → `download/xima-tv.apk` (929 B) → `assets/c2.conf` Base64 → **token OTA `fl0t4_0ta_s3cr3t_2026`**; `/MarketServer/ota.php` acepta `POST multipart campo pkg` y guarda **sin validar extensión** → webshell `/ota/sh.php` como `www-data`; `/home/<usuario>/user.txt` (644) → `flag{ejemplo}`.
- Fase 2 (ROOT): `sudo -n -l` de www-data → `(root) NOPASSWD: /usr/local/sbin/ota-deploy`; el script hace `eval "sha256sum .../$PKG"` → inyección `x;cat /root/root.txt` → `flag{ejemplo}`.
- Herramientas: `señalfantasma/solucion/exploit.py` (cadena completa), `webcmd.py`, `scan_tcp.py`, `socks5_pivot.py`; artefactos en `work/` y banderas en `flag_user.txt` / `flag_root.txt`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-182817`.

### 2026-10-23 — Desafío 11 «6puntos» resuelto
- Evidencia: `ctf/6puntos/seis_pulsos.zip` (1.762.380 B); 6 JPEG 1440×900 con `Make: TRAMA`, `Model: VF0`.
- El EXIF conserva `DateTimeOriginal` (17→22 oct 2026, días consecutivos) y `GPS`: el orden de emisión se reconstruye pese a que los nombres de archivo fueron regenerados.
- Geocodificación inversa (Nominatim + Wikipedia/Commons): Viña del Mar → El Monte → Curicó → Talca → Osorno → Puerto Octay; latitud 33,0°→40,9° (recorrido norte→sur coherente).
- Flag: nombres sin tildes ni espacios, unidos con `_`. **Corrección posterior (2026-10-23):** la pista oficial («algunas ciudades pueden contener un nombre más corto») indica usar `Rupanco` en el punto 6 en lugar de `PuertoOctay`; con eso las iniciales forman **VECTOR**. Flag final: `flag{ejemplo}`.
- Herramientas: `6puntos/solucion/resolver_secuencia.py` (+ `extraer_exif.sh`, `geocodificar.py`, `recortes.py`, `tiles.sh`); artefactos en `work/zoom/` y `work/mapa/`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-181916` (y `...20261023-211034` antes de la corrección).

### 2026-10-23 — Desafío 10 «El Ingrediente Secreto de Vlad» resuelto
- Requiere internet (OSINT real en GitHub). Perfil `VladElVeg666` («Vlad The Vegeterian», bio «I love tomatos!!!», TransilVilla).
- Único repo: `VladElVeg666/Mis_Recetas_Favoritas`, un solo archivo `README.md`, una sola rama `main`, sin tags.
- 3 commits; el último («Update secret ingredient in README») cambió la flag. HEAD → `flag{ejemplo}`; commit anterior → `flag{ejemplo}` (versión obsoleta).
- Herramienta: `El_Ingrediente_Secreto_de_Vlad/solucion/recolectar.sh`; snapshots en `work/README_<sha>.md` y JSON de la API.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-181016`.

### 2026-10-23 — Desafío 09 «La Cuenta que No Existía» resuelto
- Evidencia: `ctf/La_Cuenta_que_No_Existia/La_Cuenta_que_No_Existia.zip` (51.180 B, SHA256 `F9D192F1...E66B36B3`); ya venía dentro de `ctf/`.
- Material: 5 fotos + 6 perfiles archivados + index.
- Hallazgo: 4 fotos sin EXIF; `ultima_foto.jpg` conserva `Artist = valen_nomade_priv`, `UserComment` «perfil espejo: valen_nomade_priv» y GPS 33°02'S 71°37'W (Viña del Mar).
- Cadena: EXIF → nombre del perfil espejo → `archivo_web/valen_nomade_priv.html` → código Base64 → flag.
- Señuelos: los otros 5 perfiles tenían códigos que parecían Base64 pero decodificaban a binario aleatorio.
- Herramienta: `La_Cuenta_que_No_Existia/solucion/rastrear_cuenta.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-180848`.

### 2026-10-23 — Desafío 08 «Mojojojo» resuelto
- Evidencia: `ctf/mojojojo/Mojojojos_v2.zip` (1.210 B, SHA256 `B9AD365E...77923BBD`); ya venía dentro de `ctf/`.
- Selección de registro por `control_de_cabina.txt`: 23:10 → `transmision.txt` (autorizado); 21:40 → `senal_2140_ensayo.txt` (señuelo que decodifica como `PRUEBA DE AUDIO`).
- Cadena real: hex → ASCII → **Base45** (alfabeto de 45 símbolos) → **Base64** → **Ook!** («un mono escribiendo») → **Brainfuck** (1.863 instrucciones) → flag.
- Falsa pista superada: el texto parecía modulado (1.242 bloques de 30 caracteres, 1 bit por bloque); extraer esos bits (mayoría, ITA2, ASCII 5-8 bits, base64/base85) no daba nada. La clave fue `set(texto) ⊆ alfabeto Base45` + longitud múltiplo de 3.
- Herramienta: `mojojojo/solucion/resolver.py`; artefactos `work/capa3_ook.txt`, `work/programa.bf`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-180646`.

### 2026-10-23 — Desafío 07 «Magma» resuelto
- Evidencia: `ctf/Magma/Magma.zip` (271.461 B, SHA256 `A3A51D06...4FCA6B`); ya venía dentro de `ctf/`.
- Contenido: `placa_magma.png` (2100×520), `lecturas_superficie.csv` (atrezzo), `LEEME.txt`.
- Descartado: EXIF, binwalk, chunks PNG, datos tras IEND, `strings`.
- Hallazgo: mosaico con periodo horizontal **164 px** (12,8 repeticiones). La resta contra el desplazamiento deja 63.682 píxeles fuera del patrón, concentrados en dos bandas de filas (108–179 y 303–374) que dibujan el texto.
- Método: autocorrelación para el periodo + máscara de diferencias; recortes ampliados por línea.
- Herramienta: `Magma/solucion/revelar_magma.py`; visuales en `work/diff_mask.png`, `work/linea1.png`, `work/linea2.png`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-175831`.

### 2026-10-23 — Desafío 06 «El baño VIP» resuelto
- Evidencia: `ctf/El_Bano_VIP_Jugador/El_Bano_VIP_Jugador.zip` (318 B, SHA256 `2A4C36CD...C9928EF5`); ya venía dentro de `ctf/`.
- Contenido: `ticket_0347.txt`, 72 líneas × 8 tokens de 5 caracteres, solo 2 tokens distintos (`-----`, `.----`).
- Mecánica: aparenta Morse pero es un flujo binario (576 bits = 72 bytes) con `'.' = 1`; resultado ASCII = Base64.
- Capas: rayas/puntos → bits → ASCII Base64 → flag. Polaridad opuesta (`'-' = 1`) da 72 × `0xFF`.
- Herramienta: `El_Bano_VIP_Jugador/solucion/decodificar_ticket.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-175526`.

### 2026-10-23 — Desafío 05 «Cartas» resuelto
- Evidencia: `ctf/cartas/Cartas.zip` (1.699 B, SHA256 `8C4A4363...D022EDFF`), movido desde la raíz del proyecto a `ctf/`.
- Contenido: acta de subasta, 2 catálogos de glifos, lámina PROMO (control) y lámina de La Quintrala (objetivo).
- Mecánica: 16 glifos Unicode → cifra hex, 2 glifos por byte. Catálogo auténtico `catalogo_glifos.txt`; la reimpresión intercambia los valores de `▽` y `▲` (9↔2).
- Validación: la lámina PROMO decodifica `ENSAYO DE IMPRENTA SIN VALOR DE TORNEO` solo con el catálogo auténtico; con el falso sale basura.
- Cebo: con el catálogo falso la flag sale plausible pero corrupta (`TYAMACTF{...}`).
- Herramienta: `cartas/solucion/decodificar_lamina.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-175311`.

### 2026-10-23 — Desafío 04 «El Cuaderno de Claves» resuelto
- Evidencia: `ctf/cuaderno-de-claves/cuaderno-de-claves.zip` (38.640 B, SHA256 `48DB0900...91E4C5F8`), movido desde la raíz del proyecto a `ctf/`.
- Contenido: `cifrador.py` (447 B), `bitacora.cifrada` (410 hex = 205 bytes), `qsl_cerro_alegre.png` (960×600).
- Cifrador: por byte → XOR con clave repetida, rotación izquierda `(i%7)+1`, swap de nibbles. Reversible; se descifra al revés.
- Clave: indicativo **`CE2RCA`** de la tarjeta QSL (Op. «El Viejo», 14-JUL-1987 0312 UTC, 7.045 MHz CW).
- Validación: round-trip `encrypt(decrypt(x)) == x` → True. Ataque alternativo con crib `"Bitacora"` (`solucion/ataque_crib.py`) recupera la misma clave y texto al 100% imprimible.
- Herramientas: `solucion/descifrar.py`, `solucion/ataque_crib.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-175139`.

### 2026-10-23 — Desafío 03 «Señal desde Blackwood» resuelto
- Evidencia: `ctf/BW_SOC_3110/BW_SOC_3110.png` (4.389 B, PNG 600×400 RGB, SHA256 `85910bf4...0f2f61da`). Carpeta movida desde la raíz del proyecto a `ctf/` para mantener limpia la raíz.
- Señal: `exiftool` → `Trailer data after PNG IEND chunk`; `binwalk` → ZIP completo desde el byte 4098.
- Mecánica: ZIP anexado tras el IEND con `flag.txt` (flag) y `nota.txt`.
- Trampa: el chunk IEND son 12 B y `find("IEND")` cae en el tipo → fin real = `iend + 8`.
- Herramienta: `BW_SOC_3110/solucion/carve_trailer.py`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-174920`.

### 2026-10-23 — Desafío 02 «La Mansión Blackwood» resuelto
- Evidencia: `casaembrujada/casaembrujada.png` (481.081 B, 400×400 RGB, SHA256 `12b4f39a...1118aa4`).
- Descartado: EXIF/metadatos, chunks extra PNG, datos tras IEND, `strings`, `binwalk` (solo IDAT normales).
- Hallazgo: payload en **LSB del bit 0**, orden píxel-interleaved (R,G,B por píxel, fila a fila), desde el offset 0. Media del LSB ≈ 0.5 en los tres canales.
- Herramienta: `casaembrujada/solucion/lsb_extract.py` (numpy + Pillow, bit parametrizable).
- Artefactos: `flag.txt`, `work/plane_*_bit*.png` (planos visuales), `solucion/salida.txt`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.<timestamp>`.

### 2026-10-23 — Desafío 01 «Todo Gira» resuelto
- Evidencia: `Todo_Gira.zip` (11.894 B, SHA256 `5CF23F48...2AC534AA`), copiada a `ctf/01-todo-gira/work/`.
- Mecánica: 100 capas de zip anidadas, nombres = Fibonacci descendente F(99) → F(0); `file_1_b.zip` desambigua la colisión F(1)=F(2)=1. Contenido final `LaFlag.txt`.
- Herramienta: `work/desanidar.py` (recursión en memoria con `io.BytesIO`), capas volcadas en `work/chain/`.
- Flag guardada en `01-todo-gira/flag.txt`.
- Backup previo de este índice: `backups/CONTEXTO_CTF.md.20261023-174222`.

### 2026-10-23 — Creación de la estructura
- Creada la carpeta `ctf/` con `CONTEXTO_CTF.md` y `backups/`.
- Definida la convención `NN-nombre-desafio/README.md` para cada writeup.
- Pendiente: recibir enunciado del primer desafío.
