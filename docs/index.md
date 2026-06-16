<div class="hero">
<img class="hero-mark" src="assets/logo.png" alt="PortHound">
<div class="hero-copy">
<div class="hero-kicker">Standalone network scanner</div>

<h1>PortHound</h1>

<p>Consola local para descubrir hosts, puertos, banners, favicons y tags, con API JSON, WebSocket y persistencia SQLite. El launcher publico mantiene la instancia en loopback y la UI concentra el control de targets, ports y banners.</p>

<div class="hero-actions">
<a class="link" href="getting-started.md"><span>Primeros pasos</span><strong>Instalacion y arranque</strong></a>
<a class="link" href="reference/ui.md"><span>Interfaz web</span><strong>Menu actual y vistas auxiliares</strong></a>
<a class="link" href="reference/api.md"><span>API HTTP</span><strong>Rutas, respuestas y ejemplos</strong></a>
</div>
</div>
</div>

<div class="meta-grid">
<div class="meta"><span>Menu actual</span><strong>Dashboard, Targets, Ports, Banners y API</strong></div>
<div class="meta"><span>Vistas auxiliares</span><strong>Explorer, Charts, Tags, Catalogs y Map World</strong></div>
<div class="meta"><span>Backend</span><strong>Python 3.12 + SQLite</strong></div>
<div class="meta"><span>Canales</span><strong>HTTP, WebSocket y soporte de agente</strong></div>
</div>

## Lo esencial

<div class="cards">
<div class="card"><strong>Dashboard</strong><br>Snapshot operativo con mapa, conteos y ultimos targets y banners.</div>
<div class="card"><strong>Targets</strong><br>Definicion de CIDR, protocolo, modo de puertos y acciones start/restart/stop/delete.</div>
<div class="card"><strong>Ports</strong><br>Filtros, paginacion y control por protocolo con refresco en vivo.</div>
<div class="card"><strong>Banners</strong><br>Banners y favicons con captura por endpoint y apertura de iconos.</div>
<div class="card"><strong>API y WS</strong><br>Contrato HTTP y WebSocket para UI, automatizacion e integraciones locales.</div>
<div class="card"><strong>Catalogos</strong><br>Reglas regex, probes y presets, tanto en DB como en seed files.</div>
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
<div class="diagram-step">Ports / banners / favicons / tags</div>
<div class="diagram-note">Los resultados se guardan en SQLite y quedan listos para la API, la UI y exportacion posterior.</div>
</div>
</div>
</div>

## Superficies

- El menu principal actual expone `Dashboard`, `Targets`, `Ports`, `Banners` y `API`.
- El arbol `frontend/src/views/` todavia contiene `Explorer`, `Charts`, `Tags`, `Catalog`, `FileCatalog` y `MapWorld` como superficies auxiliares o de referencia tecnica.
- La portada permite fijar el `apiBase` y el token local en el navegador.

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
