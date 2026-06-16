# WebSocket

PortHound expone un canal WebSocket en `/ws/`. La UI lo usa para refrescar vistas cuando cambian los datos y para recibir snapshots iniciales al conectar.

La SPA escucha `welcome`, `scan_map_snapshot` y `scan_map_update` para refrescar el mapa y disparar recargas ligeras de tablas sin repetir llamadas pesadas.

## Conexion inicial

Al abrir el socket, el servidor envía normalmente estos mensajes JSON:

- `welcome` con `client_id` y `subprotocol`.
- `scan_map_snapshot` con el estado actual del mapa.
- `attack_snapshot` con el feed reciente de ataques.
- `attack_summary` con el resumen agregado.

## Mensajes del cliente

El cliente puede enviar objetos JSON con la clave `action`.

| Action | Proposito |
| --- | --- |
| `scan_map_snapshot` | Pide un snapshot del mapa de scans. |
| `map_snapshot` | Alias de `scan_map_snapshot`. |
| `scan_map_refresh` | Pide una actualizacion del mapa. |
| `map_refresh` | Alias de `scan_map_refresh`. |
| `attacks_snapshot` | Pide un snapshot del feed de ataques. |
| `attacks_summary` | Pide el resumen agregado de ataques. |
| `attacks_pause` | Pausa el generador de telemetria de ataques. |
| `attacks_resume` | Reanuda el generador de telemetria de ataques. |
| `attacks_burst` | Genera una rafaga de eventos. |
| `attacks_push` | Inserta un evento custom en la telemetria. |

## Eventos del servidor

| Type | Contenido |
| --- | --- |
| `scan_map_snapshot` | Snapshot completo del mapa. |
| `scan_map_update` | Snapshot actualizado cuando cambia el estado. |
| `attack_snapshot` | Lista reciente de eventos de ataque. |
| `attack_summary` | Resumen de severidad, acciones, tipos y targets. |
| `attack_event` | Evento individual generado por la telemetria. |
| `attack_simulator_status` | Estado del simulador de ataques. |
| `attack_burst_ack` | Confirmacion de una rafaga generada. |
| `attack_push_ack` | Confirmacion de un evento custom. |

## Chat y eco

Si el mensaje no es un comando de control, el servidor lo interpreta como chat:

- texto plano o `alias: mensaje` se guarda en la tabla de chat en memoria (`ws_db`);
- el servidor responde con un eco de texto;
- los frames binarios se reenvian con el prefijo `BIN ECHO:`.

## Ping, pong y cierre

- Los frames `ping` reciben `pong`.
- Los frames de cierre se reflejan de vuelta antes de cerrar la conexion.
- La UI maneja reconexion automatica si el socket cae.

## Relacion con la API

Los sockets activos pueden consultarse por HTTP en `/api/ws/clients`.
Las acciones administrativas sobre clientes, pings y cierres usan la API HTTP, no mensajes WS.
Lo mismo aplica a `broadcast`, `ping` y `close` desde el panel administrativo.
