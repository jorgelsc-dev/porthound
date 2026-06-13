# PortHound

`PortHound` es un escaner de red en Python para auditorias autorizadas. Reune escaneo activo, banner grabbing, persistencia SQLite, dashboard SPA y control HTTP/WebSocket sobre `wsbuilder`.

Sitio oficial: [https://porthound.jorgelsc.dev](https://porthound.jorgelsc.dev)<br>
Repositorio: [https://github.com/jorgelsc-dev/porthound](https://github.com/jorgelsc-dev/porthound)<br>
PyPI: `porthound4`<br>
Comando: `porthound`

## Mapa rapido

`Operador -> dashboard SPA / API local -> targets -> scanners TCP/UDP/ICMP/SCTP -> SQLite -> mapas / analytics / banners / WebSocket`

## Bloques principales

- Escaneo activo para `tcp`, `udp`, `icmp` y `sctp` cuando el runtime lo soporta.
- Banner grabbing con probes y reglas regex editables.
- Persistencia local en SQLite para `targets`, `ports`, `banners`, `tags` y `favicons`.
- Dashboard Vue 3 + Vuetify servido por el mismo proceso.
- Snapshot de mapa, analitica, feed de ataques y canal WebSocket.
- Seed GeoIP versionado en `data/` para poblar la base al arrancar.

## Modelo de ejecucion

- El launcher publico trabaja en modo `standalone`.
- `manage.py` fija el bind en `127.0.0.1:45678` para el flujo documentado del repo.
- `--host` y `--port` existen por compatibilidad, pero el launcher standalone los ignora.
- La ruta `GET /` sirve la SPA cuando el cliente pide HTML y devuelve conteos JSON cuando no.
- Quedan endpoints `/api/cluster/*` para compatibilidad interna y pruebas, pero la ruta soportada para usuarios del repo es local y standalone.

## Instalacion

### Desde PyPI

```bash
python -m pip install --upgrade pip
python -m pip install porthound4
```

Uso inmediato:

```bash
porthound
```

### Desde el repo

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python manage.py
```

## Inicio rapido

### 1. Arrancar el runtime

```bash
porthound --db-path Standalone.db
```

O desde el repo:

```bash
python manage.py --db-path Standalone.db
```

Valores efectivos del launcher standalone:

- `host`: `127.0.0.1`
- `port`: `45678`
- `db`: `Standalone.db` si no defines `PORTHOUND_DB_PATH`

### 2. Abrir la interfaz local

- Dashboard: `http://127.0.0.1:45678`
- Catalogo de endpoints: `http://127.0.0.1:45678/api/endpoints/`

### 3. Confirmar el estado del backend

```bash
curl http://127.0.0.1:45678/api/dashboard/
curl http://127.0.0.1:45678/protocols/
```

### 4. Crear un target

```bash
curl -X POST http://127.0.0.1:45678/target/ \
  -H 'Content-Type: application/json' \
  -d '{
    "network": "192.168.1.0/24",
    "type": "common",
    "proto": "tcp",
    "timesleep": 0.5
  }'
```

## Flujo mental

1. Defines uno o varios `targets`.
2. `target/action` o `target/action/bulk` activa el scheduler.
3. Los scanners escriben puertos, tags, banners y favicons en SQLite.
4. `api/dashboard`, `api/charts/analytics` y `api/map/scan` resumen el estado.
5. `WS /ws/` emite snapshots de mapa, feed de ataques y mensajes de control.

## Superficie HTTP y WS

Rutas de trabajo mas utiles:

- `GET /protocols/`
- `GET /targets/`
- `POST|PUT|DELETE /target/`
- `POST /target/action/`
- `POST /target/action/bulk/`
- `GET|DELETE /ports/`, `/ports/tcp/`, `/ports/udp/`, `/ports/icmp/`, `/ports/sctp/`
- `GET|DELETE /banners/`
- `GET /tags/` y variantes por protocolo
- `GET|DELETE /favicons/` y `GET /favicons/raw/?id=<id>`
- `GET /api/dashboard/`
- `GET /api/charts/analytics`
- `GET /api/map/scan`
- `GET /api/ip/domains/`, `/api/ip/ttl-path/`, `/api/ip/intel/`
- `GET|POST|PUT|DELETE /api/catalog/*`
- `GET|POST /api/attacks/*`
- `GET|POST /api/ws/*`
- `WS /ws/`

## Configuracion y seguridad

Variables utiles:

- `PORTHOUND_DB_PATH`: ruta de la base SQLite activa.
- `PORTHOUND_CORS_ALLOW_ORIGIN`: origen permitido para CORS.
- `PORTHOUND_API_TOKEN`: token administrativo para `Authorization: Bearer <token>` o `X-API-Key`.
- `PORTHOUND_API_REQUIRE_TOKEN=1`: fuerza token incluso en loopback. Debe usarse junto con `PORTHOUND_API_TOKEN`.
- `PORTHOUND_DNS_RESOLVERS`: lista separada por comas como `udp://1.1.1.1,tcp://8.8.8.8`.
- `PORTHOUND_DNS_TIMEOUT_SECONDS`: timeout por resolvedor.
- `PORTHOUND_DNS_USE_SYSTEM_RESOLVER=1`: conserva el resolvedor del sistema como fallback.

Reglas importantes:

- Si no defines `PORTHOUND_API_TOKEN`, los endpoints administrativos solo aceptan clientes loopback.
- Si el navegador entra por loopback pero el `Origin` no es loopback, el backend tambien bloquea las acciones administrativas.
- El launcher deja `PORTHOUND_TLS_ENABLED=0` por defecto.
- La distribucion de CA y el enrollment por certificado estan deshabilitados; el flujo actual usa HTTP local y tokens.

## Componentes del repo

- `manage.py`: launcher standalone y normalizacion de entorno.
- `app.py` y `views.py`: SPA, API, WebSocket, dashboard y catalogos.
- `server.py`: motor de DB, scanners y modelos de runtime.
- `banner_rules.py` y `scan_payloads.py`: probes y reglas de identificacion.
- `dns.py`: resolucion y utilidades DNS para IP intel.
- `data/`: seeds GeoIP, presets de IP y catalogos iniciales.
- `frontend/`: SPA Vue 3 + Vuetify.

## Desarrollo

Backend:

```bash
python manage.py
```

Frontend:

```bash
cd frontend
npm ci
npm run serve
```

Validacion local:

```bash
python -m compileall -q .
python -m unittest discover -s tests -q
```

Checks de frontend:

```bash
cd frontend
npm run lint
npm run build
```

## Documentacion

- Sitio publico: [https://porthound.jorgelsc.dev](https://porthound.jorgelsc.dev)
- Landing publica: [docs/index.html](docs/index.html)
- Catalogo vivo de endpoints: `GET /api/endpoints/`
- Seeds y notas de datos: [data/README.md](data/README.md)

## Contribucion y soporte

- Usa el proyecto solo para trabajo autorizado.
- Abre ramas desde `develop` con `feat/<nombre>`, `fix/<nombre>`, `docs/<nombre>` o `chore/<nombre>`.
- Envia PRs a `develop` con un resumen corto y notas de riesgo.
- Si encuentras una vulnerabilidad, usa el canal privado descrito en `SECURITY.md`.
- Soporte y donacion opcional: `SUPPORT.md`
