<div class="hero">
<img class="hero-mark" src="assets/logo.png" alt="PortHound">
<div class="hero-copy">
<div class="hero-kicker">Standalone network scanner</div>

<h1>PortHound</h1>

<p>Escaner local para revisar targets, puertos, banners, favicons y tags con una interfaz simple, API JSON, WebSocket y SQLite.</p>
</div>
</div>

## Mapa de plataforma

Cliente -> UI -> API -> SQLite -> resultados

La UI controla `Dashboard`, `Targets`, `Ports`, `Banners` y `API`. La API publica el estado, el motor guarda los resultados y el WebSocket mantiene las vistas sincronizadas.

## Flujo mental

1. Abres la consola local.
2. Ajustas la base de API y, si hace falta, el token.
3. Creas un target.
4. Recorres ports, banners, favicons y tags.
5. Consultas la API o el WebSocket cuando quieres automatizar o integrar.

## Guia rapida

<div class="links">
<a class="link" href="/getting-started/"><span>Empezar</span><strong>Instalacion y arranque</strong></a>
<a class="link" href="/reference/ui/"><span>Aplicacion</span><strong>UI, navegacion y estado local</strong></a>
<a class="link" href="/architecture/"><span>Arquitectura</span><strong>Capas y flujo de datos</strong></a>
<a class="link" href="/reference/api/"><span>Referencia HTTP</span><strong>Rutas, respuestas y ejemplos</strong></a>
</div>

## Uso autorizado

!!! warning
    PortHound solo debe usarse en sistemas, redes y rangos donde tengas autorizacion explicita.
