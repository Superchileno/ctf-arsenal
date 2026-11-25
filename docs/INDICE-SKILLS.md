# Índice de skills — qué usar según la señal

33 skills cargables en `skills\<id>\` (`SKILL.md` + `references\` + `scripts\`).
Instalar en el agente: `python arsenal\install_skills.py --dest ~/.agents/skills`.

---

## CTF (13) — el 70 %

| Skill | Cuándo usarla | Scripts |
|---|---|---|
| `solving-ctf-challenges-systematically` | Metodología general, triaje, señuelos, boot2root, misc | `ctf_triage.py`, `verify_flag.py` |
| `ctf-orquestacion` | Enrutado entre skills, criterios de pivote, cierre de writeup | — |
| `analyzing-file-artifacts-for-steganography` | Imágenes, ZIP, DOCX, PDF, polyglots, LSB, capas | `carve_appended.py`, `lsb_extract.py`, `ooxml_scan.py`, `zip_nested.py`, `reveal_pattern.py` |
| `solving-classical-and-custom-cryptography` | Texto cifrado, XOR, Vigenère, codificaciones, glifos | `xor_tool.py`, `vigenere.py`, `crib_drag.py`, `decode_chain.py`, `glyph_catalog.py` |
| `performing-ctf-forensics-on-audio-and-logs` | WAV/MP3, logs, pcap, MFT, discos | `spectrogram.py`, `tone_nibbles.py`, `pcm_lsb.py`, `correlate_logs.py`, `mft_dat.py` |
| `exploiting-binary-vulnerabilities-in-ctf` | ELF + servicio: format string, ret2win, SROP, heap, kernel | `checksec_summary.sh`, `offset_finder.py`, `fmtstr_write.py`, `ret2win.py`, `srop_execve.py` |
| `reversing-obfuscated-binaries-and-vms` | Binarios stripped, tablas en `.rodata`, VMs de bytecode, oráculos | `find_main.py`, `extract_tables.py`, `oracle_bruteforce.py` |
| `ctf-web` | URL, API, SPA, JWT, SQLi, SSTI, SSRF, XXE, deserialización | puente a material MIT |
| `ctf-misc` | Pyjails, bash jails, codificaciones exóticas, Z3, SDR, contenedores | puente |
| `ctf-ai-ml` | Modelos, pesos, adversariales, prompt injection, LLM | puente |
| `ctf-malware` | Muestras, scripts ofuscados, PE/.NET, C2, YARA | puente |
| `ctf-osint` | Geolocalización, EXIF, perfiles, dorks, DNS recon | puente |
| `defending-against-prompt-injection-in-ctf-agents` | Contenido que contiene instrucciones dirigidas a la IA | `scan_prompt_injection.py` |

---

## Pentesting y auditoría (20) — el 30 %

### Web y API

| Skill | Cuándo usarla |
|---|---|
| `exploiting-api-injection-vulnerabilities` | SQLi/NoSQLi/OS command/LDAP/SSRF en parámetros de API |
| `testing-api-for-broken-object-level-authorization` | BOLA/IDOR: cambiar ids de objeto |
| `testing-api-authentication-weaknesses` | Tokens, JWT, API keys, sesión, credential stuffing |
| `testing-oauth2-implementation-flaws` | redirect_uri, PKCE, CSRF, scope escalation |
| `testing-websocket-api-security` | CSWSH, auth en upgrade, flooding |
| `exploiting-jwt-algorithm-confusion-attack` | RS256→HS256, `kid`/`jku`, clave pública como secreto |
| `performing-jwt-none-algorithm-attack` | `alg: none` con firma vacía |
| `performing-graphql-introspection-attack` | Introspección, depth limit, batching, mutaciones sin auth |

### Red

| Skill | Cuándo usarla |
|---|---|
| `scanning-network-with-nmap-advanced` | Descubrimiento, NSE, evasión, fingerprint de SO |
| `performing-dns-enumeration-and-zone-transfer` | AXFR, subdominios, registros, infraestructura |
| `analyzing-network-traffic-with-wireshark` | pcap: protocolos, extracción de artefactos, TLS |

### Forense y respuesta

| Skill | Cuándo usarla |
|---|---|
| `conducting-memory-forensics-with-volatility` | Volcado RAM: procesos, inyección, conexiones, credenciales |
| `performing-disk-forensics-investigation` | Imagen de disco, recuperación, timeline |
| `performing-threat-hunting-with-yara-rules` | Reglas YARA sobre archivos y memoria |
| `hunting-evtx-with-chainsaw` | EVTX con Sigma y keywords |
| `building-incident-timeline-with-timesketch` | Timeline multi-fuente |

### Sistemas y contenedores

| Skill | Cuándo usarla |
|---|---|
| `performing-active-directory-vulnerability-assessment` | PingCastle, BloodHound, Purple Knight |
| `escaping-containers-to-host` | Pods privilegiados, montajes de host, runC, socket Docker |
| `implementing-secrets-scanning-in-ci-cd` | gitleaks/trufflehog en pipelines |
| `performing-web-application-scanning-with-nikto` | Barrido inicial de servidor web |

---

## Enrutado rápido

```
señal                          → skill
--------------------------------|--------------------------------------------
archivo raro / imagen / docx   → analyzing-file-artifacts-for-steganography
texto cifrado / tokens         → solving-classical-and-custom-cryptography
wav / log / pcap / disco       → performing-ctf-forensics-on-audio-and-logs
ELF + nc host puerto           → exploiting-binary-vulnerabilities-in-ctf
ELF pide token / VM            → reversing-obfuscated-binaries-and-vms
URL / API / SPA                → ctf-web + skills de API
jail / SDR / Z3 / encoding     → ctf-misc
modelo / LLM / pesos           → ctf-ai-ml
muestra / C2                   → ctf-malware
foto / perfil / coordenadas    → ctf-osint
sin idea de por dónde empezar  → solving-ctf-challenges-systematically
hay que entregar writeup       → ctf-orquestacion
```

---

## Notas

- Las skills CTF propias incluyen **scripts ejecutables**; las seis puente
  (`ctf-web`, `ctf-misc`, `ctf-ai-ml`, `ctf-malware`, `ctf-osint`,
  `ctf-orquestacion`) resumen la técnica y remiten a material MIT de
  `ljagiello/ctf-skills` (ver `THIRD-PARTY-NOTICES.md`).
- Si un script no cubre el caso, escríbelo en `solucion\` del objetivo y, si se
  repite tres veces, promuévelo a `skills\<id>\scripts\`.
