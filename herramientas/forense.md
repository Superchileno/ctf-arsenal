# Forense — memoria, disco, red y timeline

## Memoria (Volatility 3)

```bash
vol -f dump.mem windows.info
vol -f dump.mem windows.pslist
vol -f dump.mem windows.pstree
vol -f dump.mem windows.cmdline
vol -f dump.mem windows.netscan
vol -f dump.mem windows.malfind
vol -f dump.mem windows.hashdump
vol -f dump.mem linux.bash
vol -f dump.mem linux.pslist
vol -f dump.mem -o work/ windows.dumpfiles --virtaddr 0x...
```

## Disco

```bash
# Adquisición e integridad
dd if=/dev/sdX of=evidence.img bs=4M status=progress
sha256sum evidence.img > evidence.img.sha256

# Estructura
mmls evidence.img
fsstat -o <offset> evidence.img
fls -r -p -o <offset> evidence.img > work/fls.txt
icat -o <offset> evidence.img <inodo> > work/archivo_recuperado

# Timeline
fls -r -m '/' -o <offset> evidence.img > work/bodyfile.txt
mactime -b work/bodyfile.txt -d > work/timeline.csv
```

## Red

```bash
# tshark
tshark -r captura.pcap -q -z io,phs
tshark -r captura.pcap -Y 'http.request' -T fields -e http.host -e http.request.uri
tshark -r captura.pcap -z follow,tcp,ascii,3
tshark -r captura.pcap --export-objects http,work/http

# Zeek
zeek -r captura.pcap
cat conn.log | zeek-cut id.orig_h id.resp_h id.resp_p proto duration orig_bytes
cat dns.log  | zeek-cut query answers
```

Indicadores: beaconing periódico, DNS con subdominios largos, transferencias
asimétricas, JA3 raro, puertos no estándar.

## Logs y timelines

```bash
# EVTX con Chainsaw
chainsaw hunt evidencia/ --sigma /opt/sigma/ --mapping /opt/chainsaw/mappings/sigma-event-logs-all.yml

# Splunk / KQL / SPL: ver skills de threat hunting
# Timesketch
timesketch_importer -c <sketch> -f timeline.csv --timeline_name "host-01"
```

## YARA

```bash
yara -r reglas.yar work/
yara -s reglas.yar sospechoso.bin
```

## Calidad de la evidencia

| Regla | Detalle |
|---|---|
| Hash de todo | SHA-256 del original y de cada derivado |
| Cadena de custodia | quién, cuándo, desde dónde, con qué comando |
| Solo lectura | montar y analizar sobre copia, nunca el original |
| Redacción | credenciales y PII enmascaradas en el informe |

## Guardrails

- No modificar la evidencia original.
- Registrar cada comando con fecha y hora.
- `evidence/` no se versiona en el repositorio público.
