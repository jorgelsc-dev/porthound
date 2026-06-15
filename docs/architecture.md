# Arquitectura

PortHound esta organizado como una aplicacion local con cuatro capas claras: bootstrap, backend HTTP/WebSocket, motor de escaneo y frontend.

## Capas del runtime

| Capa | Archivo | Responsabilidad |
| --- | --- | --- |
| Bootstrap | `manage.py` | Carga entorno, selecciona perfil y arranca la instancia local. |
| Web backend | `app.py` | Expone vistas HTML, API JSON, WebSocket y telemetria. |
| Persistencia y scan engine | `server.py` | Esquema SQLite, normalizacion, workers TCP/UDP/ICMP/SCTP y banner grabbing. |
| UI | `frontend/src/` | SPA Vue 3 + Vuetify para dashboard, tablas y acciones. |

## Flujo de datos

1. El usuario crea o edita un `target`.
2. `server.py` valida el payload y lo guarda en SQLite.
3. Los workers de `TCP`, `UDP`, `ICMP`, `SCTP`, `BannerTCP` y `BannerUDP` consumen esos targets.
4. Los resultados se escriben en `ports`, `tags`, `banners` y `favicons`.
5. `app.py` construye snapshots para dashboard, mapa, graficas y API.
6. El frontend escucha cambios por WebSocket y refresca vistas relacionadas.

## Servicios en segundo plano

- `attack_telemetry` genera eventos sinteticos de ataque para la consola y la vista de resumen.
- `scan_map_telemetry` emite snapshots del mapa geolocalizado cuando cambian los hosts.
- `start_scanners_for_db` arranca los workers de escaneo sobre la base activa.
- `start_local_cluster_agent` puede levantar un agente local en modo master cuando el perfil lo requiere.

## Archivo por archivo

- `manage.py` aplica politicas de host y puerto fijos para la app local, carga perfiles persistidos y materializa certificados temporales si existen en la DB de launcher.
- `app.py` usa `wsbuilder.App` como runtime principal, registra rutas y mantiene caches como `IP_INTEL_CACHE`.
- `server.py` concentra el acceso a SQLite y las reglas de normalizacion de targets, banners y catalogos.
- `frontend/src/state/appStore.js` administra `apiBase`, token de acceso y conexion WebSocket.
- `frontend/src/views/` define las pantallas de usuario.

## Superficies auxiliares

El repositorio todavia contiene piezas heredadas o auxiliares que sirven como referencia tecnica:

- `ws_demo.py` para la demo y el chat WebSocket.
- `master.py` y `agent.py` para compatibilidad con modos distribuidos.
- `framework.py` para integraciones heredadas.

## Persistencia y UI

La UI no habla con un ORM. Habla con SQLite por medio de `server.py` y con snapshots JSON por medio de `app.py`. Esa division es importante: `server.py` cambia el estado, `app.py` lo presenta.
