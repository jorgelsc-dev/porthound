# Primeros pasos

PortHound puede ejecutarse instalado desde PyPI o desde el repositorio. La ruta normal es simple: arrancar la app, abrir la UI local y empezar con un target.

## Requisitos

- Python 3.12 o superior.
- `wsbuilder>=0.25.7,<0.26.0`.

## Instalacion

### Recomendado para usuario final: `pipx`

`pipx` es la mejor opcion cuando quieres PortHound como comando local y no quieres gestionar entornos virtuales a mano:

- instala la app en un entorno aislado
- expone el binario `porthound` en tu `PATH`
- evita conflictos con otros paquetes de tu Python principal

Instalacion:

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
pipx install porthound4
porthound
```

Si necesitas fijar Python 3.12 explicitamente:

```bash
pipx install --python python3.12 porthound4
```

Mantenimiento:

```bash
pipx upgrade porthound4
pipx uninstall porthound4
```

Si `porthound` no se encuentra tras instalar:

- abre una shell nueva despues de `pipx ensurepath`
- o ejecuta `pipx ensurepath --force`
- revisa que `~/.local/bin` este en tu `PATH`

### Alternativa con `venv`

Si no quieres instalar `pipx`, usa un entorno virtual normal:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install porthound4
porthound
```

Instalacion desde el repositorio:

```bash
python -m pip install .
porthound
```

Tambien puedes arrancar con:

```bash
python -m porthound
```

Notas:

- En Kali, Debian y otras distros con PEP 668, `python -m pip install --user ...` puede estar bloqueado.
- `--break-system-packages` existe, pero no se recomienda para instalar PortHound.

### Instalacion directa con `pip`

Usala solo dentro de un `venv` o si controlas ese Python:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install porthound4
porthound
```

En sistemas con Python externamente gestionado, esta ruta puede estar bloqueada.

### Desde el repositorio

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
porthound
```

Esta ruta es la adecuada para desarrollo local y contribucion.

### Bundle offline para `pip`

Si vas a instalar PortHound en una maquina sin internet, genera primero un `wheelhouse` en una maquina compatible con acceso a red.

Compatibilidad recomendada entre maquina de build y maquina destino:

- mismo sistema operativo
- misma arquitectura
- misma version principal/secundaria de Python

Si `frontend/dist` no existe, el build ejecuta `npm ci && npm run build`. Solo la maquina que arma el bundle necesita Node 22 LTS.

Los source tarballs de release incluyen `frontend/dist`, asi que una instalacion desde ese artefacto no deberia requerir Node.

Build del bundle:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel build
python -m build
mkdir -p wheelhouse
cp dist/*.whl wheelhouse/
python -m pip download --dest wheelhouse "wsbuilder>=0.25.7,<0.26.0"
tar -czf porthound-offline-bundle.tar.gz wheelhouse
```

Instalacion offline:

```bash
tar -xzf porthound-offline-bundle.tar.gz
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --no-index --find-links wheelhouse porthound4
porthound
```

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
2. Si hace falta, guarda el token en el chip `Auth`.
3. Crea un `Target` con una red CIDR.
4. Revisa `Ports` y `Banners`.
5. Usa `API` cuando quieras integrar o automatizar.

## Token de acceso

Cuando `PORTHOUND_API_TOKEN` esta configurado, la UI envia el token como `Authorization: Bearer` o `X-API-Key`. El valor se conserva en `sessionStorage` para la sesion actual.

Si el backend responde `401`, el dialogo de autenticacion se abre de nuevo para que puedas corregir o limpiar el token.

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
