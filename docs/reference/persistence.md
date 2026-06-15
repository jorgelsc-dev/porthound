# Persistencia SQLite

PortHound usa SQLite como almacenamiento local. La base por defecto es `Standalone.db`; el launcher tambien conoce perfiles `Master.db` y `Agent.db` para compatibilidad con el modo cluster, aunque la distribucion publica arranca en standalone.

## Tablas principales

| Tabla | Proposito | Notas |
| --- | --- | --- |
| `targets` | Define los scopes de escaneo. | Guarda red CIDR, tipo, protocolo, modo de puertos, agente y progreso. |
| `ports` | Resultado de endpoints descubiertos. | Incluye `state`, `scan_state` y `progress`. |
| `banners` | Respuestas de banner grabbing. | Guarda el blob bruto y la version legible. |
| `favicons` | Favicons capturados por HTTP. | Guarda URL, MIME, tamano, hash y blob. |
| `tags` | Metadatos extraidos de cada endpoint. | Se usa para `service`, `product`, `server`, `version`, `runtime`, etc. |
| `banner_regex_catalog` | Reglas de extraccion por regex. | Mezcla reglas built-in, seed y custom. |
| `banner_probe_catalog` | Probes de banner por protocolo. | Contiene payloads `generic`, `http` y `port_override`. |
| `ip_catalog` | Presets de IP o CIDR. | Alimenta la UI de catalogos y semillas. |
| `cluster_agent_credentials` | Tokens de agente. | Guarda `agent_id`, hash del token y estado activo/inactivo. |
| `launcher_config` | Configuracion persistida del launcher. | Se usa para recordar perfiles y variables. |
| `launcher_blobs` | Certificados y CA persistidos. | Guarda blobs base64 para compatibilidad de perfiles. |

## Campos importantes

- `targets.network` solo acepta IPv4 CIDR.
- `targets.type` usa `common`, `not_common` o `full`.
- `targets.proto` usa `tcp`, `udp`, `icmp` o `sctp`.
- `targets.port_mode` usa `preset`, `single` o `range`.
- `targets.status` usa `active`, `stopped` o `restarting`.
- `ports.state` describe el estado del endpoint observado.
- `ports.scan_state` controla si un endpoint sigue activo, detenido o en reinicio.
- `mutable = 0` marca catalogos seed o built-in de solo lectura.

## Bootstrap y seeds

Al arrancar, `server.py` crea o ajusta el esquema, importa los catalogos desde `data/banner_regex_rules.json`, `data/banner_probe_requests.json` y `data/ip_presets.json`, y sincroniza el seed GeoIP desde `data/geoip_blocks.seed.jsonl.gz`.

## Flujo de escritura

- `insert_targets` y `update_targets` guardan la definicion del scope.
- `insert_port`, `insert_tags`, `insert_banners` e `insert_favicon` guardan resultados de los workers.
- `clear_target_artifacts` borra resultados asociados a un target cuando se reinicia o elimina.
- `delete_ports_where_*`, `delete_banners` y `delete_favicons` limpian resultados por protocolo o globalmente.

## Regla practica

Si buscas el punto de entrada para entender la persistencia, empieza por `server.py` y sigue el flujo hacia `app.py`. Ese par sustituye aqui al patron de un `orm.py` tradicional.
