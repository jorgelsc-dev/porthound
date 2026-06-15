# API HTTP

PortHound expone una API JSON sobre el mismo servidor que monta la UI. Las rutas devuelven normalmente uno de estos patrones:

- `{"datas": [...]}` para listas.
- `{"count": n}` para contadores.
- `{"status": "ok"}` para mutaciones exitosas.
- `{"status": "mensaje"}` o `{"status": "error"}` para errores.

## Reglas comunes

- Las rutas que modifican estado requieren acceso administrativo.
- Si `PORTHOUND_API_TOKEN` esta configurado, debes enviarlo en `Authorization: Bearer` o `X-API-Key`.
- Si no hay token, solo se permite loopback.
- `stcp` se acepta como alias de `sctp` en varias rutas.

## Basicos

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/` | no | Devuelve un resumen de conteos o HTML si el cliente pide pagina. |
| GET | `/protocols/` | no | Protocolos soportados por el runtime. |
| GET | `/count/targets/` | no | Total de targets. |
| GET | `/count/ports/` | no | Total de ports. |
| GET | `/count/ports/tcp/` | no | Total TCP. |
| GET | `/count/ports/udp/` | no | Total UDP. |
| GET | `/count/ports/icmp/` | no | Total ICMP. |
| GET | `/count/ports/sctp/` | no | Total SCTP. |
| GET | `/count/ports/stcp/` | no | Alias de SCTP. |
| GET | `/count/banners/` | no | Total de banners. |

## Targets

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/targets/` | no | Lista todos los targets. |
| POST | `/target/` | si | Crea un target. |
| PUT | `/target/` | si | Actualiza un target. |
| DELETE | `/target/` | si | Borra un target por id. |
| POST | `/target/action/` | si | `start`, `restart`, `stop` o `delete` sobre un target. |
| POST | `/target/action/bulk/` | si | Accion masiva sobre targets de un protocolo. |

Payload base para crear target:

```json
{
  "network": "10.0.0.0/24",
  "type": "common",
  "proto": "tcp",
  "port_mode": "preset",
  "port_start": 0,
  "port_end": 0,
  "timesleep": 0.5,
  "agent_mode": "local",
  "agent_id": "local"
}
```

## Ports, banners y tags

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/ports/` | no | Lista todos los endpoints descubiertos. |
| GET | `/ports/tcp/` | no | Filtra TCP. |
| GET | `/ports/udp/` | no | Filtra UDP. |
| GET | `/ports/icmp/` | no | Filtra ICMP. |
| GET | `/ports/sctp/` | no | Filtra SCTP. |
| GET | `/ports/stcp/` | no | Alias de SCTP. |
| DELETE | `/ports/tcp/` | si | Limpia resultados TCP. |
| DELETE | `/ports/udp/` | si | Limpia resultados UDP. |
| DELETE | `/ports/icmp/` | si | Limpia resultados ICMP. |
| DELETE | `/ports/sctp/` | si | Limpia resultados SCTP. |
| DELETE | `/ports/stcp/` | si | Alias de SCTP. |
| POST | `/port/action/` | si | `start`, `restart` o `stop` para un endpoint concreto. |
| POST | `/banner/action/` | si | Alias de `port/action`. |
| GET | `/banners/` | no | Lista banners capturados. |
| DELETE | `/banners/` | si | Borra todos los banners. |
| GET | `/favicons/` | no | Lista favicons capturados. |
| DELETE | `/favicons/` | si | Borra todos los favicons. |
| GET | `/favicons/raw/?id=<id>` | no | Devuelve el blob binario de un favicon. |
| GET | `/tags/` | no | Lista todos los tags. |
| GET | `/tags/tcp/` | no | Filtra tags TCP. |
| GET | `/tags/udp/` | no | Filtra tags UDP. |
| GET | `/tags/icmp/` | no | Filtra tags ICMP. |
| GET | `/tags/sctp/` | no | Filtra tags SCTP. |
| GET | `/tags/stcp/` | no | Alias de SCTP. |

## Intel y analitica

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/api/dashboard/` | no | Snapshot de dashboard con counts, ports, banners, tags y cluster. |
| GET | `/api/charts/analytics` | no | Series agregadas para graficas. |
| GET | `/api/map/scan?limit=<n>` | no | Snapshot geolocalizado del mapa. |
| GET | `/api/ip/domains/?ip=<ipv4>&refresh=0|1` | si | Dominios relacionados con una IP. |
| GET | `/api/ip/ttl-path/?ip=<ipv4>&refresh=0|1` | si | Camino TTL y estimacion de saltos. |
| GET | `/api/ip/intel/?ip=<ipv4>&refresh=0|1` | si | Intel completa: dominios, TTL y perfil de host. |
| GET | `/api/endpoints/` | no | Catalogo de rutas expuestas por el backend. |

## Utilidades

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/api/hello` | no | Respuesta simple de prueba. |
| POST | `/api/echo` | no | Devuelve el cuerpo recibido como texto. |

## Catalogos

### File-backed

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/api/catalog/file/banner-rules` | no | Lee `data/banner_regex_rules.json`. |
| POST | `/api/catalog/file/banner-rules` | si | Añade una regla al fichero y la sincroniza en DB. |
| GET | `/api/catalog/file/banner-requests` | no | Lee `data/banner_probe_requests.json`. |
| POST | `/api/catalog/file/banner-requests` | si | Añade un probe al fichero y la sincroniza en DB. |
| GET | `/api/catalog/file/ip-presets` | no | Lee `data/ip_presets.json`. |
| POST | `/api/catalog/file/ip-presets` | si | Añade un preset al fichero y la sincroniza en DB. |

### DB-backed

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/api/catalog/banner-rules/?include_inactive=0|1` | no | Lista reglas regex. |
| POST | `/api/catalog/banner-rules/` | si | Crea regla custom. |
| PUT | `/api/catalog/banner-rules/` | si | Actualiza regla custom. |
| DELETE | `/api/catalog/banner-rules/` | si | Borra regla custom. |
| GET | `/api/catalog/banner-requests/?include_inactive=0|1&proto=tcp|udp` | no | Lista probes. |
| POST | `/api/catalog/banner-requests/` | si | Crea probe custom. |
| PUT | `/api/catalog/banner-requests/` | si | Actualiza probe custom. |
| DELETE | `/api/catalog/banner-requests/` | si | Borra probe custom. |
| GET | `/api/catalog/ip-presets/?include_inactive=0|1` | no | Lista presets. |
| POST | `/api/catalog/ip-presets/` | si | Crea preset custom. |
| PUT | `/api/catalog/ip-presets/` | si | Actualiza preset custom. |
| DELETE | `/api/catalog/ip-presets/` | si | Borra preset custom. |

## WebSocket y chat

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/ws/` | no | Canal realtime principal. |
| GET | `/api/ws/clients` | si | Lista clientes activos. |
| POST | `/api/ws/broadcast` | si | Emite texto o binario a clientes. |
| POST | `/api/ws/ping` | si | Envía ping a los clientes. |
| POST | `/api/ws/close` | si | Cierra un cliente o todos. |
| GET | `/api/chat/messages?limit=<n>` | no | Lista mensajes del chat. |
| POST | `/api/chat/clear` | si | Borra el chat. |

## Telemetria de ataques

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/api/attacks/feed?limit=<n>` | no | Feed reciente de eventos. |
| GET | `/api/attacks/summary` | no | Resumen agregado. |
| POST | `/api/attacks/simulate` | si | Inserta un evento custom. |
| GET | `/api/attacks/simulator` | no | Estado actual del simulador. |
| POST | `/api/attacks/simulator` | si | Activa, pausa o genera rafagas. |

Para `POST /api/attacks/simulator` puedes enviar un cuerpo como:

```json
{
  "running": true,
  "burst": 5
}
```

## Agentes y cluster

Las rutas de cluster ademas requieren que el runtime este en rol `master`.

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/api/agent/status` | no | Snapshot del runtime del agente local. |
| GET | `/cluster/agents/` | si | Vista HTML del cluster, solo master. |
| GET | `/api/cluster/agents` | si | Lista agentes y leases activas. |
| GET | `/api/cluster/agent/credentials` | si | Lista tokens de agente. |
| POST | `/api/cluster/agent/credentials` | si | Crea o rota un token. |
| DELETE | `/api/cluster/agent/credentials` | si | Revoca o borra un token. |
| POST | `/api/cluster/agent/control` | si | `stop` o `delete` un agente. |
| GET | `/api/cluster/ca` | si | Devuelve `410 Gone`. |
| GET | `/api/cluster/ca/raw` | si | Devuelve `410 Gone`. |
| GET | `/api/cluster/ca/oneline` | si | Devuelve `410 Gone`. |
| POST | `/api/cluster/agent/enroll` | si | Devuelve `410 Gone`. |
| POST | `/api/cluster/agent/register` | si | Registra un agente por token. |
| POST | `/api/cluster/agent/heartbeat` | si | Renueva lease y reporta progreso. |
| POST | `/api/cluster/agent/task/pull` | si | El agente pide la siguiente tarea. |
| POST | `/api/cluster/agent/task/submit` | si | El agente sube resultados. |

## HTML auxiliares

| Method | Path | Auth | Nota |
| --- | --- | --- | --- |
| GET | `/attacks/raw/` | no | Consola HTML de telemetria de ataques. |

## Ejemplos

Crear token de agente:

```json
{
  "agent_id": "edge-01",
  "token": "super-secret-token"
}
```

Pedir una accion sobre un target:

```json
{
  "id": 12,
  "action": "restart",
  "clean_results": true
}
```

Listar banners solo activos:

```bash
curl "http://127.0.0.1:45678/api/catalog/banner-rules/?include_inactive=0"
```

## Notas

- `GET /api/endpoints/` es la forma mas simple de enumerar la superficie publicada por el backend.
- Las vistas HTML y la API JSON comparten el mismo proceso y la misma base SQLite.
