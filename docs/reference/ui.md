# Interfaz web

La SPA actual se construye con Vue 3 y Vuetify. El shell compartido vive en `frontend/src/App.vue` y monta la navegacion, el estado de autenticacion y el estado de WebSocket.

## Barra superior

La top bar muestra:

- el nombre del producto;
- el chip de estado de autenticacion;
- el chip de estado WebSocket;
- la base de API activa;
- un enlace de soporte;
- el dialogo para guardar o limpiar el token.

## Vistas principales

| Vista | Proposito | Acciones clave |
| --- | --- | --- |
| Dashboard | Snapshot operacional. | Ver metricas, mapa, ultimos targets y ultimos banners. |
| Targets | Control de scopes. | Crear, iniciar, reiniciar, parar y borrar targets. |
| Ports | Inteligencia de endpoints. | Cambiar de protocolo, filtrar, paginar y controlar scans por puerto. |
| Banners | Banners y favicons. | Revisar banners, abrir favicons y controlar banner grabbing. |
| API | Catalogo de endpoints. | Buscar rutas, metodos y descripciones del backend. |

## Dashboard

El dashboard combina:

- metricas de conteo;
- `MapPanel` con geolocalizacion;
- accesos rapidos a las secciones core;
- tabla de targets recientes;
- tabla de banners recientes.

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

## Estado local

- `apiBase` se persiste en `localStorage`.
- `authToken` se persiste en `sessionStorage`.
- `wsStatus` se refleja en tiempo real.
- `authStatus` cambia entre `open`, `saved`, `checking`, `required` y `authenticated`.

## Vistas auxiliares

El arbol fuente contiene vistas adicionales que documentan capacidades del backend aunque no formen parte del menu principal actual:

- `ChartsView.vue` para analitica con D3.
- `CatalogView.vue` y `FileCatalogView.vue` para catalogos y seed files.
- `ExplorerView.vue` para investigacion de IP intel.
- `MapWorldView.vue` para una vista inmersiva del mapa.

Esas vistas son utiles como referencia tecnica y para el mantenimiento del contrato API.
