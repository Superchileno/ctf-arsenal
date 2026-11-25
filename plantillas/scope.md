# Alcance (scope) — <cliente> / <objetivo>

> Fuente única de verdad del alcance. Todo lo que no esté aquí está prohibido.

## En alcance

| Tipo | Objetivo | Puertos / rutas | Notas |
|---|---|---|---|
| Dominio |  |  |  |
| IP |  |  |  |
| Aplicación web |  |  |  |
| API |  |  |  |
| Host interno |  |  |  |
| Cuenta de prueba |  |  |  |

## Fuera de alcance

- (listar explícitamente: dominios hermanos, proveedores, entornos productivos no
  autorizados, cuentas de terceros, endpoints de pago real, etc.)

## Reglas de enfrentamiento

| Regla | Valor |
|---|---|
| Requests por segundo por host | 5 (200 ms entre requests) |
| Ventana horaria |  |
| Autenticación permitida |  |
| Datos reales de clientes | prohibido extraer; usar cuentas de prueba |
| Fuerza bruta de credenciales | permitida / prohibida |
| Exfiltración de datos | solo prueba mínima, sin descargar el dataset |
| Detención ante crítico | sí |
| Contacto de emergencia |  |

## Activos excluidos por criticidad

| Activo | Motivo | Autorizado por |
|---|---|---|
|  |  |  |

## Registro de cambios

| Fecha | Cambio | Backup |
|---|---|---|
|  |  |  |
