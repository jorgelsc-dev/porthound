# Aplicacion

PortHound se usa desde una SPA Vue 3 + Vuetify. La barra superior muestra el estado de autenticacion, el estado de WebSocket, la base de API activa y el acceso al token local.

## Pantallas principales

- `Dashboard`: conteos, mapa, ultimos targets y ultimos banners.
- `Explorer`: busqueda cruzada de targets, servicios, banners, tags y favicons.
- `Targets`: crear y controlar scopes.
- `Ports`: revisar puertos por protocolo y operar por lote.
- `Banners`: ver banners y favicons.
- `Tags`: inspeccionar metadatos y tiempos detectados.
- `Catalog`: administrar reglas, probes y presets guardados en SQLite.
- `Files`: revisar catalogos versionados desde `data/`.
- `Map`: explorar hosts geolocalizados con proyecciones flat y globe.
- `Charts`: analizar resultados agregados.
- `Security`: gestionar token local, credenciales de agente y estado de cluster.
- `API`: buscar rutas del backend.

## Navegacion

- En desktop, las secciones aparecen como tabs.
- En mobile, se abren en un drawer lateral.
- La portada permite cambiar `API base URL` si la UI y el backend no comparten origen.

`/agents` se mantiene como ruta heredada y redirige a `/security`.

## Estado local

- `apiBase` se guarda en `localStorage`.
- `authToken` se guarda en `sessionStorage`.
- `wsStatus` cambia en tiempo real.
- `authStatus` pasa por `open`, `saved`, `checking`, `required` y `authenticated`.
