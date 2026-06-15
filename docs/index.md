# PortHound

<p align="center">
  <img src="assets/logo.png" alt="PortHound" width="220">
</p>

PortHound es un escaner de red en Python 3.12 para auditorias autorizadas. El proyecto combina un backend local, workers de escaneo, persistencia SQLite y una SPA Vue 3 + Vuetify para operar targets, resultados y telemetria en tiempo real.

## Que cubre

- Definicion de targets por CIDR, protocolo y rango de puertos.
- Escaneo TCP, UDP, ICMP y SCTP.
- Banner grabbing y captura de favicons.
- Persistencia local en SQLite.
- Dashboard, mapa, tablas y paneles de control.
- API HTTP, WebSocket y soporte de agente o cluster.
- Catalogos de reglas, probes e IP presets.

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

## Componentes clave

| Archivo | Responsabilidad |
| --- | --- |
| `manage.py` | Bootstrap, carga de entorno, launcher y persistencia de perfiles. |
| `app.py` | Aplicacion HTTP/WebSocket actual, snapshots, catalogos y telemetria. |
| `server.py` | Base de datos, validacion de payloads y workers de escaneo. |
| `frontend/src/` | SPA de Vue 3 + Vuetify. |
| `data/` | Seeds y catalogos versionados. |

## Uso autorizado

!!! warning
    PortHound solo debe usarse en sistemas, redes y rangos donde tengas autorizacion explicita.
