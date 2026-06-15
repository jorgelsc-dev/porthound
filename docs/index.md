<div class="hero">
<img class="hero-mark" src="assets/logo.png" alt="PortHound">
<div class="hero-copy">
<div class="hero-kicker">Neon network reconnaissance</div>

<h1>PortHound</h1>

<p>Escaneo TCP/UDP con banners, favicons y telemetria en tiempo real para operaciones autorizadas.</p>

<div class="hero-actions">
<a class="link" href="getting-started.md"><span>Primeros pasos</span><strong>Instalacion y arranque</strong></a>
<a class="link" href="reference/ui.md"><span>Interfaz web</span><strong>Shell, tablas y paneles</strong></a>
<a class="link" href="reference/api.md"><span>API HTTP</span><strong>Rutas, respuestas y ejemplos</strong></a>
</div>
</div>
</div>

<div class="meta-grid">
<div class="meta"><span>Frontend</span><strong>Vue 3 + Vuetify</strong></div>
<div class="meta"><span>Backend</span><strong>Python 3.12 + SQLite</strong></div>
<div class="meta"><span>Canales</span><strong>HTTP, WebSocket y agente</strong></div>
<div class="meta"><span>Foco</span><strong>Targets, ports, banners y favicons</strong></div>
</div>

## Lo esencial

<div class="cards">
<div class="card"><strong>Targets</strong><br>Scopes por CIDR, protocolo y rango de puertos, con control de arranque y parada.</div>
<div class="card"><strong>Ports</strong><br>Filtros, paginacion y acciones por protocolo con refresco en vivo.</div>
<div class="card"><strong>Banners</strong><br>Captura de banners y favicons para inteligencia de servicios.</div>
<div class="card"><strong>API y Docs</strong><br>Contrato HTTP/WS estable y documentacion publica en GitHub Pages.</div>
</div>

## Ruta de operacion

<div class="diagram">
<div class="diagram-title">Flujo principal</div>
<div class="diagram-track">
<div class="diagram-node">Operador</div>
<div class="diagram-arrow">-&gt;</div>
<div class="diagram-node">Target</div>
<div class="diagram-arrow">-&gt;</div>
<div class="diagram-node">Engine</div>
<div class="diagram-arrow">-&gt;</div>
<div class="diagram-node">Dashboard</div>
</div>
<div class="diagram-rows" style="margin-top: 1rem;">
<div class="diagram-row">
<div class="diagram-step">Targets</div>
<div class="diagram-arrow">-&gt;</div>
<div class="diagram-step">Ports / banners / favicons</div>
<div class="diagram-note">Los resultados se guardan en SQLite y quedan listos para la API, la UI y exportacion posterior.</div>
</div>
</div>
</div>

## Mapa rapido

- [Primeros pasos](getting-started.md)
- [Arquitectura](architecture.md)
- [Interfaz web](reference/ui.md)
- [Configuracion](reference/configuration.md)
- [Seguridad](reference/security.md)
- [Catalogos](reference/catalogs.md)
- [Persistencia SQLite](reference/persistence.md)
- [API HTTP](reference/api.md)
- [WebSocket](reference/websocket.md)

## Uso autorizado

!!! warning
    PortHound solo debe usarse en sistemas, redes y rangos donde tengas autorizacion explicita.
