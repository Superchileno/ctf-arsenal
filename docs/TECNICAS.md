# Técnicas destiladas — de reto resuelto a patrón reutilizable

Este documento es el corazón del 70 % CTF: cada fila nació de un reto real y
quedó reducida a **señal → técnica → comando**. Sin flags, sin hosts, sin
nombres de eventos.

> Al cerrar un reto nuevo, agrega su fila. Si la técnica se repite tres veces,
> conviértela en script dentro de la skill correspondiente.

---

## 1. Esteganografía y archivos

| Señal | Técnica | Comando / script |
|---|---|---|
| Archivo «termina» pero pesa de más | Buscar datos tras el fin lógico | `arsenal/ctf-arsenal carve f` |
| Imagen con ruido uniforme | LSB bit 0, orden interleaved | `arsenal/ctf-arsenal lsb f --bit 0` |
| Imagen que se repite | Mosaico con periodo `p`; restar medias | `arsenal/ctf-arsenal pattern f` |
| ZIP dentro de PNG/JPEG | Polyglot: firmas `PK\x03\x04` tras IEND/EOI | `binwalk -e f`, `foremost f` |
| DOCX/XLSX sospechoso | Texto blanco, `vanish`, `customXml`, tamaño 1 | `arsenal/ctf-arsenal ooxml f` |
| Firma de archivo corrupta | Comparar con firma canónica y reparar 1–4 bytes | `xxd f | head` |
| ZIP cifrado sin clave | ZipCrypto + known plaintext con prefijo de flag | `bkcrack -C f -c flag.txt -p p.txt` |
| ZIP anidado en cadena | Desanidar en memoria, sin escribir a disco | `arsenal/ctf-arsenal zip f` |
| Imagen que no abre | Verificar CRC de chunks PNG | `pngcheck -v f` |

## 2. Criptografía clásica y casera

| Señal | Técnica | Comando |
|---|---|---|
| Texto cifrado + script cifrador | Reimplementar el cifrador al revés y validar round-trip | leer el script |
| Prefijo conocido frente al texto | Detectar César/Vigenère por diferencia de letras | `arsenal/ctf-arsenal vigenere` |
| Dos cifrados de igual longitud | Reutilización de keystream / two-time pad | `arsenal/ctf-arsenal xor diff` |
| Par (texto plano, cifrado) conocido | `keystream = C ⊕ P`, aplicar al objetivo | `arsenal/ctf-arsenal xor known` |
| Cadena de codificaciones | Decodificar por capas hasta texto legible | `arsenal/ctf-arsenal decode` |
| Glifos o lámina de símbolos | Catálogo por frecuencia + lámina de control | `arsenal/ctf-arsenal glyph` |
| Clave que «solo avanza en letras» | Vigenère inverso con avance condicional | `arsenal/ctf-arsenal vigenere --advance letters` |

## 3. Forense de audio

| Señal | Técnica | Comando |
|---|---|---|
| Audio sin música ni voz | Espectrograma: texto dibujado en frecuencias | `arsenal/ctf-arsenal spectrogram a.wav` |
| Tonos cortos repetidos | Dos tonos por símbolo → nibble alto/bajo | `arsenal/ctf-arsenal tones a.wav` |
| Ruido de fondo constante | LSB de muestras PCM, MSB-first | `arsenal/ctf-arsenal pcm-lsb a.wav` |
| Morse / DTMF / FSK | Detección por energía en bandas | `sox` + análisis propio |

## 4. Forense de red y logs

| Señal | Técnica | Comando |
|---|---|---|
| pcap con sesión FTP | Reconstruir stream y credenciales | `tshark -r f.pcap -z follow,tcp,ascii,N` |
| Logs de proxy + backend | Unir por id, ordenar por `(flow, seq)`, concatenar y decodificar | `arsenal/ctf-arsenal logs` |
| Eventos CEF con `cs1`/`cn1` | Ordenar por índice y decodificar Base64 | `arsenal/ctf-arsenal logs cef` |
| MFT + USN + no asignado | Recuperar archivo borrado | `arsenal/ctf-arsenal mft` |
| Beaconing | Periodicidad + jitter + destino raro | `zeek` + estadística |

## 5. Binarios y explotación

| Señal | Técnica | Comando |
|---|---|---|
| ELF pide token exacto | Localizar tabla en `.rodata` y revertir el cálculo | `arsenal/ctf-arsenal tables` |
| ELF sin símbolos | Encontrar `main` desde `_start` | `arsenal/ctf-arsenal find-main` |
| Comprobación byte a byte | Fuerza bruta con oráculo (256 × n) | `arsenal/ctf-arsenal oracle` |
| Format string | `%n` / `%hn` posicional con offset calculado | `arsenal/ctf-arsenal fmtstr` |
| Buffer + función win | Offset hasta RIP + ret2win | `arsenal/ctf-arsenal offset`, `ret2win` |
| Sin función win, `rax` controlado | SROP con `rt_sigreturn` | `arsenal/ctf-arsenal srop` |
| Off-by-one sobre puntero | Redirigir byte bajo a una tabla útil | cálculo manual + `gdb` |
| Heap musl | Grupos anidados de mallocng | pwndbg + análisis manual |
| Kernel | Dirty Pagetable / `tee()` sin `get_page` | plantilla propia |

## 6. Web

| Señal | Técnica | Comando |
|---|---|---|
| Parámetro `q` en buscador | SQLi: `ORDER BY` para columnas, `UNION SELECT` | `sqlmap -u 'URL?q=1' --batch` |
| Filtro «anti-inyección» | Lista negra sensible a mayúsculas o comentarios `/**/` | variantes de caso |
| Cookie con JSON legible | Cookie sin firma: editar rol y re-codificar | `base64` |
| JWT propio | `alg: none` con firma vacía | `arsenal` + python |
| JWT HS256 | Confusión de algoritmo con clave pública | script propio |
| SPA con login sin backend | Leer bundle y source maps | `curl` de `.js.map` |
| Plantilla que refleja entrada | SSTI: `{{7*7}}`, luego `{{config}}` | `tplmap` / manual |
| Ruta que concatena archivo | Path traversal con filtro no recursivo `....//` | manual |
| GraphQL | Introspección + mutaciones sin auth | `graphql-cop`, `clairvoyance` |
| Lógica de negocio | Cantidades negativas, cupones, redondeos | manual |

## 7. OSINT

| Señal | Técnica | Comando |
|---|---|---|
| Foto entregada | EXIF: GPS, cámara, `UserComment` | `exiftool f.jpg` |
| Cuenta «borrada» | Perfiles archivados y caché | Wayback, `archive.today` |
| Repo de GitHub | Historial de commits y ramas | `git log -p --all` |
| Coordenadas | Geocodificación inversa + vista de calle | mapas |
| Nombre de usuario | Enumeración multi-plataforma | `sherlock usuario` |

## 8. Boot2Root

| Señal | Técnica | Comando |
|---|---|---|
| Upload sin validar | Webshell y ejecución de comandos | `curl -F` |
| `sudo` sobre script escribible | Inyectar en el script | `ls -l`, editar |
| Backup público | Credenciales en `.sql`, `.bak`, `.zip` | `gobuster dir` |
| `.git` expuesto | Reconstruir repo y leer historial | `git-dumper` |
| Servicio antiguo | Búsqueda de exploit público | `searchsploit` |

---

## 9. Reglas de oro

1. **Un artefacto, una hipótesis a la vez**, con su criterio de falsación.
2. **Dos fallos = cambio de categoría**, no de payload.
3. **Todo resultado plausible pero raro es un señuelo** hasta que se confirme.
4. **Nunca descartes un artefacto por feo**: la firma corrupta es una pista.
5. **El writeup se escribe mientras se resuelve**, no después.
