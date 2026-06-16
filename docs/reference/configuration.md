# Configuracion

PortHound lee variables de entorno y unos pocos flags de CLI. En la rama publica, la app corre en `127.0.0.1:45678` y la configuracion practica se concentra en la base de datos, el token y DNS.

## Lo que se usa

- `PORTHOUND_DB_PATH` para cambiar la base de datos.
- `PORTHOUND_API_TOKEN` para proteger rutas administrativas.
- `PORTHOUND_API_REQUIRE_TOKEN` para exigir token incluso en loopback.
- `PORTHOUND_CORS_ALLOW_ORIGIN` para limitar CORS.
- `PORTHOUND_DNS_RESOLVERS`, `PORTHOUND_DNS_TIMEOUT_SECONDS` y `PORTHOUND_DNS_USE_SYSTEM_RESOLVER` para resolver hosts.
- `PORTHOUND_IP` para fijar la IP de salida en pruebas o scans.

## Lo que queda fijo

- Host: `127.0.0.1`
- Puerto: `45678`
- Role: `standalone`
- TLS publico: desactivado

## Compatibilidad heredada

PortHound todavia acepta varias variables y flags del modo distribuido, pero no forman parte del flujo normal de uso:

- `PORTHOUND_MASTER`
- `PORTHOUND_MASTER_HOST`
- `PORTHOUND_MASTER_IP`
- `PORTHOUND_CA`
- `PORTHOUND_CA_ONELINE`
- `PORTHOUND_TLS_ENABLED`
- `PORTHOUND_TLS_CERT_FILE`
- `PORTHOUND_TLS_KEY_FILE`
- `PORTHOUND_TLS_REQUIRE_CLIENT_CERT`
- `PORTHOUND_AGENT_ID`
- `PORTHOUND_AGENT_TOKEN`
- `PORTHOUND_AGENT_SHARED_KEY`
- `PORTHOUND_AGENT_POLL_SECONDS`
- `PORTHOUND_AGENT_HTTP_TIMEOUT`
- `PORTHOUND_AGENT_TASK_LEASE_SECONDS`
- `PORTHOUND_AGENT_TASK_STALL_SECONDS`
- `PORTHOUND_AGENT_TLS_CHECK_HOSTNAME`

## CLI

```bash
python manage.py --db-path Standalone.db --api-token <token> --api-require-token 1
```

```bash
python manage.py --dns-resolvers udp://1.1.1.1,udp://8.8.8.8 --dns-timeout-seconds 1.4
```

!!! note
    Si solo usas la app en local, normalmente basta con dejar los defaults y arrancar `porthound`.
