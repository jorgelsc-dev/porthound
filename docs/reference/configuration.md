# Configuracion

PortHound lee configuracion desde variables de entorno, ficheros de entorno y algunos flags de CLI. El launcher publico fija la instancia local en `127.0.0.1:45678`, asi que la configuracion sirve sobre todo para base de datos, seguridad, DNS y perfiles de agente.

Compatibilidad importante:

- `HOST` y `PORT` se aceptan como respaldo si no existen `PORTHOUND_HOST` o `PORTHOUND_PORT`.
- `PORTHOUND_AGENT_SHARED_KEY` actua como alias de `PORTHOUND_AGENT_TOKEN`.

## Variables de entorno

| Variable | Default | Uso |
| --- | --- | --- |
| `PORTHOUND_HOST` | `127.0.0.1` | Host HTTP local. |
| `PORTHOUND_PORT` | `45678` | Puerto HTTP local. |
| `PORTHOUND_DB_PATH` | `Standalone.db` | Base de datos activa. |
| `PORTHOUND_DEBUG` | `1` | Activa modo debug en el runtime local. |
| `PORTHOUND_API_TOKEN` | vacio | Token requerido para rutas administrativas. |
| `PORTHOUND_API_REQUIRE_TOKEN` | `0` | Obliga token aunque el cliente sea loopback. |
| `PORTHOUND_CORS_ALLOW_ORIGIN` | vacio | Origen CORS permitido. |
| `PORTHOUND_TLS_ENABLED` | `0` | Activa TLS en el launcher compatible. |
| `PORTHOUND_TLS_CERT_FILE` | `certs/master/master.cert.pem` | Certificado TLS principal. |
| `PORTHOUND_TLS_KEY_FILE` | `certs/master/master.key.pem` | Clave TLS principal. |
| `PORTHOUND_TLS_REQUIRE_CLIENT_CERT` | `0` | Exige certificado de cliente cuando TLS esta activo. |
| `PORTHOUND_CA` | vacio | Ruta a la CA para distribucion o compatibilidad heredada. |
| `PORTHOUND_CA_ONELINE` | vacio | CA inline en formato escapado con `\n`. |
| `PORTHOUND_MASTER` | vacio | URL del master en modo agente. |
| `PORTHOUND_IP` | vacio | IP fija de origen para pruebas o scans. |
| `PORTHOUND_AGENT_ID` | vacio | Identificador del agente. |
| `PORTHOUND_AGENT_TOKEN` | vacio | Token del agente. |
| `PORTHOUND_AGENT_SHARED_KEY` | vacio | Alias de `PORTHOUND_AGENT_TOKEN`. |
| `PORTHOUND_AGENT_POLL_SECONDS` | `8` | Intervalo de polling del agente. |
| `PORTHOUND_AGENT_HTTP_TIMEOUT` | `20.0` | Timeout HTTP del agente. |
| `PORTHOUND_AGENT_TASK_LEASE_SECONDS` | `300` | Duracion de la lease de tarea. |
| `PORTHOUND_AGENT_TASK_STALL_SECONDS` | `300` | Umbral para detectar tareas atascadas. |
| `PORTHOUND_AGENT_TLS_CHECK_HOSTNAME` | `1` | Verificacion de hostname en TLS del agente. |
| `PORTHOUND_DNS_RESOLVERS` | `udp://1.1.1.1,udp://8.8.8.8,udp://9.9.9.9` | Lista de resolvers por orden. |
| `PORTHOUND_DNS_TIMEOUT_SECONDS` | `1.4` | Timeout por intento DNS. |
| `PORTHOUND_DNS_USE_SYSTEM_RESOLVER` | `1` | Permite usar el resolvedor del sistema. |

## Flags de CLI

Los flags principales del launcher son:

```bash
python manage.py --db-path Standalone.db --api-token <token> --api-require-token 1
```

Otros flags utiles:

- `--env-file` para cargar uno o varios ficheros de entorno.
- `--env KEY=VALUE` para sobreescribir valores sin editar ficheros.
- `--tls-enabled`, `--tls-cert-file`, `--tls-key-file`.
- `--dns-resolvers`, `--dns-timeout-seconds`, `--dns-use-system-resolver`.

## Flags heredados

El launcher conserva opciones ocultas para compatibilidad con el modo distribuido:

- `--master`, `--master-host`, `--master-ip`
- `--agent-id`, `--agent-token`, `--agent-shared-key`
- `--agent-poll-seconds`, `--agent-http-timeout`, `--agent-task-lease-seconds`
- `--agent-enroll`

En la rama publica actual no forman parte del flujo normal de uso.

## Politica del launcher

- El host publico se normaliza a `127.0.0.1`.
- El puerto publico se normaliza a `45678` en standalone.
- Si cambias la base de datos, el launcher crea el fichero si no existe.
- `PORTHOUND_ROLE` se usa para recordar el perfil activo en la DB de launcher.

## Reglas practicas

- Usa `PORTHOUND_API_TOKEN` si expones la UI a algo que no sea loopback.
- Usa `PORTHOUND_CORS_ALLOW_ORIGIN` solo con orígenes confiables.
- Documenta cualquier nuevo env var en esta pagina y en `README.md`.
