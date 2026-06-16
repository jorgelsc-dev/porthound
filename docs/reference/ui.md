# Aplicacion

PortHound se usa desde una SPA Vue 3 + Vuetify. La barra superior muestra el estado de autenticacion, el estado de WebSocket, la base de API activa y el acceso al token local.

## Pantalla principal

- `Dashboard`: conteos, mapa, ultimos targets y ultimos banners.
- `Targets`: crear y controlar scopes.
- `Ports`: revisar puertos por protocolo y operar por lote.
- `Banners`: ver banners y favicons.
- `API`: buscar rutas del backend.

## Navegacion

- En desktop, las secciones aparecen como tabs.
- En mobile, se abren en un drawer lateral.
- La portada permite cambiar `API base URL` si la UI y el backend no comparten origen.

## Vistas auxiliares

- `Explorer` para buscar targets, servicios, banners, tags y favicons.
- `Charts` para analitica.
- `Tags` para metadatos y tiempos.
- `Catalog` y `File Catalog` para catalogos.
- `Map World` para el atlas inmersivo.

## Estado local

- `apiBase` se guarda en `localStorage`.
- `authToken` se guarda en `sessionStorage`.
- `wsStatus` cambia en tiempo real.
- `authStatus` pasa por `open`, `saved`, `checking`, `required` y `authenticated`.
