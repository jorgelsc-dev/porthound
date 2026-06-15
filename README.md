# PortHound

PortHound es un escaner de red en Python para auditorias autorizadas. Esta version usa `wsbuilder` como base HTTP/WebSocket y corre en modo unico `standalone`.

Sitio oficial: [https://porthound.jorgelsc.dev](https://porthound.jorgelsc.dev)<br>
Repositorio: [https://github.com/jorgelsc-dev/porthound](https://github.com/jorgelsc-dev/porthound)<br>
Distribucion PyPI: `porthound4`<br>
Comando principal: `porthound`<br>
Palabras clave: `python`, `network-scanner`, `port-scanner`, `cybersecurity`, `banner-grabbing`, `sqlite`, `websocket`.

## Resumen

- Escaneo TCP, UDP, ICMP y SCTP.
- Banner grabbing con reglas y probes por servicio.
- Persistencia local en SQLite.
- API HTTP y WebSocket.
- Frontend opcional en Vue 3 + Vuetify.
- Documentacion publica en GitHub Pages.

## Documentacion

- Sitio publico: [porthound.jorgelsc.dev](https://porthound.jorgelsc.dev)
- El sitio se genera con MkDocs Material desde `mkdocs.yml` y `docs/`.
- `.github/workflows/docs-pages.yml` compila y publica el sitio en GitHub Pages.
- `docs/CNAME` fija el dominio custom y `docs/404.html` redirige enlaces heredados.
- Este README sigue siendo la fuente de verdad para instalacion y uso rapido.

## Flujo de ramas

- `main`: rama estable y publica.
- `feature/*`: nuevas funciones o cambios grandes.
- `fix/*`: correcciones.
- `docs/*`: cambios de documentacion.
- `chore/*`: mantenimiento.

Reglas:

1. El trabajo normal entra por ramas auxiliares.
2. Las PRs normales apuntan a `main`.
3. `main` queda para releases y estado estable.
4. Los paquetes se publican desde `main` o desde un release tag.

## Requisitos

- Python 3.12 o superior.
- `wsbuilder>=0.18.0`.
- Acceso local al puerto HTTP configurado (por defecto `127.0.0.1:45678`).

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

### Entorno local

```bash
python3 -m venv env
env/bin/python -m pip install --upgrade pip
env/bin/python manage.py
```

## Inicio rapido

### 1. Arrancar PortHound

```bash
porthound
```

O desde el repo:

```bash
python manage.py --db-path Standalone.db
```

Valores por defecto:

- `host`: `127.0.0.1`
- `port`: `45678`
- `db`: `Standalone.db`

### 2. Usar la interfaz local

- UI/API: `http://127.0.0.1:45678`
- Si tu instancia exige token, abre el chip `Auth` para guardarlo en `sessionStorage` y
  reutilizarlo en peticiones administrativas.

## Ejecucion

- `manage.py` arranca siempre en modo `standalone`.
- El launcher fija `127.0.0.1:45678`; `--host` y `--port` solo se aceptan si coinciden con ese bind.
- Puedes ajustar base de datos y opciones HTTP por CLI o variables de entorno.

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
- La API controla scans y vistas de estado locales.
- El chip `Auth` de la barra superior guarda un token en `sessionStorage` y lo reenvia en
  peticiones administrativas como `Authorization: Bearer`.

Comportamientos comunes:

- Texto: eco.
- Binario: eco con prefijo.
- Mensajes con alias pueden registrarse en SQLite para demo o chat.

## Seguridad

- Sin `PORTHOUND_API_TOKEN`, las acciones administrativas solo aceptan clientes loopback.
- `PORTHOUND_API_TOKEN` se envia por `Authorization: Bearer` o `X-API-Key`.
- `PORTHOUND_API_REQUIRE_TOKEN=1` debe usarse junto con `PORTHOUND_API_TOKEN`.
- `PORTHOUND_CORS_ALLOW_ORIGIN` define el origen permitido para CORS.
- Si el navegador entra por loopback pero el `Origin` no es loopback, el backend tambien bloquea las acciones administrativas.
- `PORTHOUND_TLS_ENABLED=0` es el valor por defecto del launcher standalone.
- La distribucion CA y el enrollment por certificado estan deshabilitados en el flujo actual.

## DNS y registros

PortHound usa DNS para descubrimiento inverso, resolucion de hosts y validacion de dominios. Si no quieres depender de resolvers publicos, puedes apuntarlo a tu propio DNS interno o a un resolvedor local.

### Resolvers soportados

- `udp://1.1.1.1:53`
- `tcp://1.1.1.1:53`
- `dot://dns.example.org:853`
- `doh://dns.example.org/dns-query`

### Configuracion de PortHound

```bash
export PORTHOUND_DNS_RESOLVERS="udp://10.0.0.2:53,tcp://10.0.0.2:53,dot://dns.example.org:853,doh://dns.example.org/dns-query"
export PORTHOUND_DNS_TIMEOUT_SECONDS="1.4"
export PORTHOUND_DNS_USE_SYSTEM_RESOLVER="1"
```

Notas:

- `PORTHOUND_DNS_RESOLVERS` acepta una lista separada por comas.
- PortHound prueba resolvers en orden y se detiene cuando obtiene una respuesta util.
- El cliente DNS de PortHound valida `A`, `PTR`, `CNAME` y `AAAA` segun el transporte y la respuesta obtenida.

### DNS local de PortHound

El servidor DNS embebido que trae `wsbuilder` y que PortHound expone para uso local publica registros `A` y `AAAA`. Es util para laboratorios, homelabs y nombres internos sencillos.

Ejemplo de registros:

```python
from dns import build_local_dns_server

records = {
    "scan.local": ["10.10.0.10"],
    "dashboard.local": ["10.10.0.11", "::1"],
}

dns_server = build_local_dns_server(records=records, host="0.0.0.0", port=5300)
dns_server.start()
```

Nota: el puerto `53` suele requerir privilegios de administrador. En laboratorios suele ser mas practico usar `5300` y redirigir el cliente o el router hacia ese puerto.

### Tipos de registros

Si administras tu DNS real, estos son los tipos mas comunes y como se declaran en una zona BIND, Unbound o CoreDNS equivalente:

```dns
; A: IPv4
scanner.local.      IN A     10.10.0.10

; AAAA: IPv6
scanner.local.      IN AAAA  2001:db8::10

; CNAME: alias
app.local.          IN CNAME scanner.local.

; MX: correo
local.              IN MX 10 mail.local.

; NS: autoridad de zona
local.              IN NS ns1.local.
local.              IN NS ns2.local.

; TXT: metadatos / verificaciones
scanner.local.      IN TXT "porthound=enabled"

; SRV: servicios descubiertos por nombre
_http._tcp.local.   IN SRV 0 5 8080 scanner.local.

; PTR: resolucion inversa
10.0.10.10.in-addr.arpa. IN PTR scanner.local.

; CAA: restriccion de certificados
local.              IN CAA 0 issue "letsencrypt.org"
```

### Como configurarlo en los clientes

La idea es que el cliente use tu DNS interno como resolutor principal. Puedes hacerlo por equipo, por red o por router.

#### Linux

```bash
sudo resolvectl dns eth0 10.10.0.2
sudo resolvectl domain eth0 '~local'
```

Si usas `systemd-resolved`, tambien puedes establecerlo en NetworkManager o en la interfaz del router DHCP.

#### Windows

- Panel de control o Configuracion de red.
- En la tarjeta de red, configura DNS manual:
  - DNS preferido: `10.10.0.2`
  - DNS alternativo: `10.10.0.3`
- Si distribuyes por DHCP, empuja las opciones `6` y `15` desde el router o servidor DHCP.

#### macOS

```bash
networksetup -setdnsservers "Wi-Fi" 10.10.0.2 10.10.0.3
```

#### Router / DHCP

- Configura el DNS entregado por DHCP con tu IP interna.
- Si tienes una zona privada como `local` o `corp`, añade ese sufijo en la opcion de dominio de busqueda.
- Si tu router lo permite, desactiva el DNS del ISP para que los clientes usen solo tu resolver interno.

### Recomendacion operativa

- Usa un resolver autoritativo interno para zonas privadas.
- Usa DoT o DoH si necesitas cifrar consultas entre cliente y resolver.
- Reserva `PTR` para reversa y `SRV` para descubrimiento de servicios.
- No publiques nombres internos sensibles en un resolver expuesto a Internet.

## Datos y persistencia

- Los datos de reglas y mapas viven en `data/`.
- La DB por defecto es `Standalone.db`.
- `data/README.md` documenta los seeds y el flujo de GeoIP.
- `server.py` y `app.py` comparten la misma base SQLite para runtime y vistas.

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

Docs:

```bash
python -m pip install -r requirements-docs.txt
mkdocs serve
```

Validacion local:

```bash
python -m compileall -q .
python -m unittest discover -s tests -q
python -m pip install -r requirements-docs.txt
mkdocs build --strict
```

Checks de frontend:

```bash
cd frontend
npm ci
npm run lint
npm run build
```

## Despliegue

- GitHub Pages publica la documentacion en `https://porthound.jorgelsc.dev`.
- MkDocs Material genera el sitio desde `mkdocs.yml` y `docs/`.
- `docs/index.html` se conserva como landing heredada y queda fuera del build de MkDocs.
- `docs/CNAME` fija el dominio custom.
- `docs/404.html` redirige enlaces viejos al sitio publico.
- `.github/workflows/docs-pages.yml` construye y publica el sitio en GitHub Pages.

## Responsabilidad

PortHound solo debe usarse en sistemas propios o con autorizacion explicita. El uso no autorizado puede violar politicas internas y leyes locales.

## Estructura

- `manage.py`: launcher principal.
- `master.py`: runtime web principal (usado en modo standalone).
- `agent.py`: modulo legado de runtime distribuido.
- `server.py`: API de escaneo.
- `app.py`: aplicacion base.
- `utils.py`: helpers compartidos.
- `views.py`: fachada publica de la capa web.
- `dns.py`: resolucion DNS y utilidades de transporte.
- `data/`: datasets.
- `docs/`: sitio publico.
- `packaging/`: scripts de `.deb` y `.zip`.

## Soporte

- Issues: [https://github.com/jorgelsc-dev/porthound/issues](https://github.com/jorgelsc-dev/porthound/issues)
- Guia de contribucion: [CONTRIBUTING.md](CONTRIBUTING.md)
- Conducta del proyecto: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Reporte privado de seguridad: [SECURITY.md](SECURITY.md)
- Soporte y donacion opcional: [SUPPORT.md](SUPPORT.md)
- Licencia: MIT
