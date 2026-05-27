# PortHound

PortHound es un escaner de red en Python para auditorias autorizadas. Esta version usa `wsbuilder` como base HTTP/WebSocket y organiza el proyecto en modos `master`, `agent` y `standalone`.

Sitio oficial: [https://porthound.jorgelsc.dev](https://porthound.jorgelsc.dev)

Repositorio: [https://github.com/jorgelsc-dev/porthound](https://github.com/jorgelsc-dev/porthound)

Distribucion PyPI: `porthound`

Comando principal: `porthound`

Palabras clave: `python`, `network-scanner`, `port-scanner`, `cybersecurity`, `banner-grabbing`, `sqlite`, `websocket`, `master/agent`.

## Resumen

- Escaneo TCP, UDP, ICMP y SCTP.
- Banner grabbing con reglas y probes por servicio.
- Persistencia local en SQLite.
- API HTTP y WebSocket.
- Frontend opcional en Vue 3.
- Documentacion publica en GitHub Pages.

## Documentacion

- Sitio publico: [porthound.jorgelsc.dev](https://porthound.jorgelsc.dev)
- Este README es la fuente de verdad del proyecto.
- La documentacion publica replica este contenido en forma de landing page.
- El repositorio mantiene solo los archivos necesarios para codigo, build, despliegue y soporte.

## Flujo de ramas

- `main`: rama estable y publica.
- `develop`: integracion y trabajo continuo.
- `feature/*`: nuevas funciones o cambios grandes.
- `fix/*`: correcciones.
- `docs/*`: cambios de documentacion.
- `chore/*`: mantenimiento.

Reglas:

1. El trabajo normal entra por ramas auxiliares.
2. `develop` integra cambios antes de publicar.
3. `main` queda para releases y estado estable.
4. Los paquetes se publican desde `main` o desde un release tag.

## Requisitos

- Python 3.12 o superior.
- `wsbuilder>=0.17.7`.
- Puertos de red abiertos entre nodos si usas `master` y `agent`.

## Instalacion

### Desde PyPI

```bash
python3 -m pip install porthound
```

### Entorno local

```bash
python3 -m venv env
env/bin/python -m pip install --upgrade pip
env/bin/python manage.py
```

## Inicio rapido

### 1. Arrancar el master

```bash
env/bin/python manage.py --role master --db-path Master.db
```

Valores por defecto:

- `host`: `127.0.0.1`
- `port`: `45678`
- `db`: `Master.db`

### 2. Usar la interfaz local

- UI/API: `http://127.0.0.1:45678`
- Vista de agentes: `http://127.0.0.1:45678/cluster/agents/`

### 3. Conectar un agente

```bash
env/bin/python manage.py '<BASE64_DEL_MASTER>'
```

La cadena base64 contiene la credencial de enrolamiento generada por el master.

## Modos de ejecucion

### Master

```bash
porthound --role master --host 0.0.0.0 --port 45678 --db-path ./Master.db
```

### Agent

```bash
porthound --role agent --master http://127.0.0.1:45678 --agent-id <id> --agent-token <token>
```

### Standalone

- Usa `manage.py` sin enrolamiento si solo quieres correr el stack local.
- El modo standalone conserva la base local del rol y no depende de un master remoto.

## Escaneo

### Protocolos

- `tcp`: escaneo de puertos y banners.
- `udp`: escaneo de puertos y banners.
- `icmp`: descubrimiento de host.
- `sctp`: escaneo cuando el runtime soporta sockets SCTP.

### Rangos

- `common`: 1-1023
- `not_common`: 1024-65534
- `full`: 1-65534

### Notas

- `timesleep` ajusta la velocidad del scan.
- El estado de progreso se guarda en SQLite para permitir reanudacion.
- `GET /protocols/` muestra los protocolos activos en runtime.

## Banner grabbing

- Se usan probes especificos por servicio y un fallback generico.
- Las respuestas se guardan en la tabla `banners`.
- TCP y UDP usan rutas de procesamiento separadas.
- El flow intenta parar pronto cuando ya hay suficientes respuestas utiles.

## API y WebSocket

- WebSocket: `ws://HOST:PORT/ws/`
- HTTP API: disponible desde el mismo servidor.
- La API controla scans, agentes y vistas de estado.

Comportamientos comunes:

- Texto: eco.
- Binario: eco con prefijo.
- Mensajes con alias pueden registrarse en SQLite para demo/chat.

## Datos y persistencia

- Los datos de reglas y mapas viven en `data/`.
- La DB por defecto del master es `Master.db`.
- La DB del agente usa `Agent.db`.
- La DB standalone usa `Standalone.db`.

## Empaquetado

### Debian

```bash
./packaging/deb/build.sh
sudo apt install ./dist/deb/porthound_<version>-1_all.deb
```

### ZIP

```bash
./packaging/zip/build.sh
unzip dist/zip/porthound_<version>-1.zip
cd porthound_<version>-1
python3 manage.py
```

## Despliegue

- GitHub Pages publica la documentacion en `https://porthound.jorgelsc.dev`.
- El dominio usa `docs/` como raiz publica del sitio.
- `docs/index.html` es la landing del proyecto.

## Responsabilidad

PortHound solo debe usarse en sistemas propios o con autorizacion explicita. El uso no autorizado puede violar politicas internas y leyes locales.

## Estructura

- `manage.py`: launcher principal.
- `master.py`: arranque del nodo master.
- `agent.py`: arranque del nodo agent.
- `server.py`: API de escaneo.
- `app.py`: aplicacion base.
- `data/`: datasets.
- `docs/`: sitio publico.
- `packaging/`: scripts de `.deb` y `.zip`.

## Soporte

- Issues: [https://github.com/jorgelsc-dev/porthound/issues](https://github.com/jorgelsc-dev/porthound/issues)
- Licencia: MIT
