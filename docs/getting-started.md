# Primeros pasos

PortHound se distribuye como paquete Debian y tambien puede ejecutarse directamente desde el repositorio durante desarrollo. La ruta normal es simple: instalar el `.deb`, arrancar la app, abrir la UI local y empezar con un target.

## Requisitos

- Python 3.12 o superior.
- `wsbuilder>=0.18.4,<0.19.0`.

## Instalacion

### Recomendado para usuario final: paquete Debian

El workflow `.github/workflows/deb-package.yml` genera el `.deb` y lo publica en **GitHub Releases**. Tambien puedes construirlo localmente:

```bash
mkdir -p /tmp/porthound-release
gh release download --repo jorgelsc-dev/porthound --pattern '*.deb' --dir /tmp/porthound-release
sudo apt install /tmp/porthound-release/*.deb
porthound
```

La pagina de la ultima release es:

```text
https://github.com/jorgelsc-dev/porthound/releases/latest
```

Build local:

```bash
./packaging/deb/build.sh
sudo apt install ./dist/deb/porthound_<version>-1_<arquitectura>.deb
porthound
```

Notas:

- Si `frontend/dist` no existe, el build Debian ejecuta `npm ci && npm run build`.
- El paquete incluye el codigo Python de PortHound y vendorea sus dependencias.
- La pestaña `Packages` de GitHub puede seguir vacia; el `.deb` se distribuye desde `Releases`.

### Desde el repositorio

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
porthound
```

Tambien puedes arrancar con:

```bash
python -m porthound
```

Esta ruta es la adecuada para desarrollo local y contribucion. Para distribucion binaria, usa el paquete Debian.

## Arranque

El launcher local arranca en:

- host: `127.0.0.1`
- port: `45678`
- base de datos: `Standalone.db`

Si abres la UI desde otro origen o detras de un reverse proxy, usa el campo `API base URL` de la portada. El frontend tambien lee `VUE_APP_API_BASE` cuando se construye por separado.

Tambien puedes fijar la base de datos:

```bash
python -m porthound --db-path Standalone.db
```

## Primer uso

1. Abre `http://127.0.0.1:45678`.
2. Copia el codigo de seguridad que PortHound imprime en la terminal y guardalo en el chip `Auth`.
3. Crea un `Target` con una red CIDR.
4. Revisa `Ports` y `Banners`.
5. Usa `API` cuando quieras integrar o automatizar.

## Codigo de seguridad

Cuando `PORTHOUND_API_TOKEN` esta configurado, la UI envia el codigo como `Authorization: Bearer` o `X-API-Key`. El valor se conserva solo en memoria del tab actual y tambien se adjunta al handshake de WebSocket.

Si el backend responde `401`, el dialogo de autenticacion se abre de nuevo para que puedas corregir o limpiar el codigo.

## Comandos utiles

Backend:

```bash
python -m porthound
```

Frontend en desarrollo:

```bash
cd frontend
npm ci
npm run serve
```

Frontend de produccion:

```bash
cd frontend
npm run build
```

Validacion basica:

```bash
python -m compileall -q .
python -m unittest discover -s tests -q
```

!!! warning
    Usa PortHound solo en sistemas, redes y rangos donde tengas autorizacion explicita.
