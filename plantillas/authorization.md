# Autorización — <cliente> / <objetivo>

> Obligatorio antes del primer request activo en `AUDITORIA\` y `PENTESTING\`.
> Sin este archivo completo, el agente no ejecuta acciones activas.

## Datos del engagement

| Campo | Valor |
|---|---|
| Cliente |  |
| Objetivo / sistema |  |
| Tipo | Auditoría / Pentesting |
| Modalidad | Caja negra / gris / blanca |
| Fecha de inicio |  |
| Fecha de término |  |
| Ventana horaria permitida |  |
| Contacto técnico del cliente |  |

## Autorizante

| Campo | Valor |
|---|---|
| Nombre y cargo |  |
| Organización |  |
| Correo / medio de contacto |  |
| Documento de respaldo (orden de trabajo, contrato, correo) |  |
| Fecha de la autorización |  |

## Declaración

Yo, `<autorizante>`, en representación de `<organización>`, autorizo a
`<equipo>` a realizar pruebas de seguridad sobre los sistemas descritos en
`scope.txt`, en las fechas y ventana indicadas, bajo las siguientes condiciones:

- [ ] Solo los sistemas listados en `scope.txt`.
- [ ] Sin técnicas destructivas (borrado, cifrado, DoS) salvo autorización aparte.
- [ ] Sin ingeniería social activa salvo autorización aparte.
- [ ] Detención inmediata ante hallazgo crítico que afecte disponibilidad.
- [ ] Confidencialidad de los hallazgos y de los datos encontrados.
- [ ] Entrega de informe y eliminación de evidencia al cierre.

## Exclusión explícita

Sistemas de terceros, proveedores cloud fuera del contrato, cuentas de clientes
finales y cualquier infraestructura no listada quedan **fuera de alcance**.

## Registro de cambios

| Fecha | Cambio | Backup |
|---|---|---|
|  |  |  |
