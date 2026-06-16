# Arquitectura

PortHound esta organizado como una aplicacion local con cuatro capas claras: bootstrap, runtime HTTP/WebSocket, motor de escaneo/persistencia y frontend.

## Capas del runtime

| Capa | Archivo | Responsabilidad |
| --- | --- | --- |
| Bootstrap | `manage.py` | Carga entorno, normaliza el launcher publico y arranca la instancia local. |
| Configuracion | `settings.py` | Resuelve variables de entorno y defaults efectivos del runtime. |
| Web backend | `app.py` | Expone vistas HTML, API JSON, WebSocket, mapas y telemetria. |
| Persistencia y scan engine | `server.py` | Esquema SQLite, normalizacion, workers TCP/UDP/ICMP/SCTP y banner grabbing. |
| UI | `frontend/src/` | SPA Vue 3 + Vuetify para dashboard, tablas, paneles y refresco en vivo. |

## Flujo de datos

1. El usuario crea o edita un `target`.
2. `app.py` y `server.py` validan el payload y lo guardan en SQLite.
3. Los workers de `TCP`, `UDP`, `ICMP`, `SCTP`, `BannerTCP` y `BannerUDP` consumen esos targets.
4. Los resultados se escriben en `ports`, `tags`, `banners` y `favicons`.
5. `app.py` construye snapshots para dashboard, mapa, graficas, endpoint catalog y host intel.
6. `frontend/src/state/appStore.js` escucha cambios por WebSocket y refresca vistas relacionadas.

## Servicios en segundo plano

- `attack_telemetry` genera eventos sinteticos de ataque para la consola y la vista de resumen.
- `scan_map_telemetry` emite snapshots del mapa geolocalizado cuando cambian los hosts.
- `start_scanners_for_db` arranca los workers de escaneo sobre la base activa.
- `ws_demo.py` aporta el registro de clientes WebSocket y el chat efimero.

## Archivo por archivo

- `manage.py` aplica politicas de host y puerto fijos para la app local y materializa la configuracion de arranque.
- `settings.py` consolida los env vars que realmente ve el runtime.
- `app.py` usa `wsbuilder.App` como runtime principal, registra rutas y mantiene caches como `IP_INTEL_CACHE`.
- `server.py` concentra el acceso a SQLite y las reglas de normalizacion de targets, banners, catalogos y scan payloads.
- `frontend/src/state/appStore.js` administra `apiBase`, token de acceso, reconexion WebSocket y refresco de tablas.
- `frontend/src/views/` define las pantallas activas y las vistas auxiliares.

## Superficies auxiliares

El repositorio todavia contiene superficies auxiliares en el frontend que sirven como referencia tecnica y para futuras extensiones:

- `ExplorerView.vue` para busqueda global de targets, servicios, banners, tags y favicons.
- `ChartsView.vue` para analitica D3 sobre el catalogo de scans.
- `TagsView.vue` para el registro de metadatos y tiempos.
- `CatalogView.vue` y `FileCatalogView.vue` para catalogos DB-backed y seed files.
- `MapWorldView.vue` para el atlas inmersivo con proyecciones flat y globe.

## Persistencia y UI

La UI no habla con un ORM. Habla con SQLite por medio de `server.py` y con snapshots JSON por medio de `app.py`. Esa division es importante: `server.py` cambia el estado, `app.py` lo presenta y `frontend/src/state/appStore.js` decide cuando refrescar.
