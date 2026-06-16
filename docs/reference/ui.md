# Interfaz web

La SPA actual se construye con Vue 3 y Vuetify. El shell compartido vive en `frontend/src/App.vue` y monta la navegacion, el estado de autenticacion, el estado de WebSocket y el dialogo para guardar el token.

## Shell

La barra superior y la portada hacen el trabajo de control principal:

- el nombre del producto y el subtitulo de la consola;
- el chip de estado de autenticacion, que abre el dialogo de token;
- el chip de estado WebSocket;
- la base de API activa;
- un enlace de soporte;
- el campo de `API base URL` en la portada para cambiar de origen sin tocar codigo.

En desktop, la navegacion aparece como tabs en la top bar. En mobile, el mismo menu se abre en el drawer lateral.

## Navegacion activa

| Ruta | Vista | Proposito |
| --- | --- | --- |
| `/` | Dashboard | Snapshot operativo, mapa, accesos rapidos y ultimos resultados. |
| `/targets` | Targets | Definir scopes y controlar su ciclo de vida. |
| `/ports` | Ports | Revisar puertos descubiertos por protocolo y operar por lote. |
| `/banners` | Banners | Revisar banners capturados y favicons. |
| `/api` | API | Catalogo de endpoints expuestos por el backend. |

## Vistas principales

| Vista | Proposito | Acciones clave |
| --- | --- | --- |
| Dashboard | Snapshot operacional. | Ver metricas, mapa, ultimos targets, ultimos banners y accesos rapidos. |
| Targets | Control de scopes. | Crear, iniciar, reiniciar, parar y borrar targets. |
| Ports | Inteligencia de endpoints. | Cambiar de protocolo, filtrar, paginar y controlar scans por puerto. |
| Banners | Banners y favicons. | Revisar banners, abrir favicons y controlar banner grabbing. |
| API | Catalogo de endpoints. | Buscar rutas, metodos y descripciones del backend. |

## Dashboard

El dashboard combina:

- metricas de conteo;
- `MapPanel` con geolocalizacion y proyeccion flat/globe;
- accesos rapidos a las secciones core;
- tabla de targets recientes;
- tabla de banners recientes.
- chips de protocolo y ultima actualizacion.

## Targets

La vista de targets permite:

- definir una red CIDR;
- elegir protocolo;
- escoger `preset`, `single` o `range`;
- fijar el tipo de preset (`common`, `not_common`, `full`);
- ajustar `timesleep`;
- disparar `start`, `restart`, `stop` y `delete`.

Cuando eliges `single` o `range`, la UI envuelve el payload para que `agent_mode` quede en `local` y `agent_id` en `local`.

## Ports

La vista de ports:

- agrupa resultados por protocolo;
- pagina listas grandes;
- permite filtros por estado y texto;
- ofrece acciones globales por protocolo;
- reacciona a updates WebSocket para refrescar solo la pestaña activa cuando puede.

## Banners

La vista de banners alterna entre:

- banners capturados;
- favicons capturados.

Desde ahi puedes abrir un favicon en una pestaña nueva o reiniciar la captura de banners para un endpoint concreto.

## Vistas auxiliares

| Vista | Archivo | Enfoque |
| --- | --- | --- |
| Explorer | `frontend/src/views/ExplorerView.vue` | Busqueda global de targets, servicios, banners, tags y favicons. |
| Charts | `frontend/src/views/ChartsView.vue` | Analitica D3 sobre targets, ports, banners, tags y series temporales. |
| Tags | `frontend/src/views/TagsView.vue` | Registro de metadatos y tiempos capturados durante el scan. |
| Catalog | `frontend/src/views/CatalogView.vue` | Gestion DB-backed de reglas, probes e IP presets. |
| File Catalog | `frontend/src/views/FileCatalogView.vue` | Gestion de seeds JSON versionados. |
| Map World | `frontend/src/views/MapWorldView.vue` | Atlas inmersivo con proyecciones flat y globe. |

Estas vistas no estan en el menu principal actual, pero siguen siendo utiles como referencia tecnica y para futuras extensiones.

## Estado local

- `apiBase` se persiste en `localStorage`.
- `authToken` se persiste en `sessionStorage`.
- `wsStatus` se refleja en tiempo real.
- `authStatus` cambia entre `open`, `saved`, `checking`, `required` y `authenticated`.
