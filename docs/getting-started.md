# Primeros pasos

PortHound puede ejecutarse instalado desde PyPI o desde el repositorio. La ruta normal es simple: arrancar la app, abrir la UI local y empezar con un target.

## Requisitos

- Python 3.12 o superior.
- `wsbuilder>=0.18.0,<0.19.0`.

## Instalacion

### Desde PyPI

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install porthound4
porthound
```

Fallbacks if your shell has not refreshed the entry point yet:

```bash
porthound4
python -m porthound
```

### Sin `venv`

CLI aislado sin gestionar entornos manualmente:

```bash
python -m pip install --user pipx
python -m pipx ensurepath
pipx install porthound4
porthound
```

Instalacion en el usuario actual con `pip`:

```bash
python -m pip install --user porthound4
porthound
```

Instalacion desde el repositorio, tambien sin `venv`:

```bash
python -m pip install --user .
porthound
```

Notas:

- `pipx` usa un entorno aislado interno, pero evita que tengas que crear o activar uno.
- `pip install --user` suele dejar el ejecutable en `~/.local/bin`.
- En sistemas con Python externamente gestionado, evita instalar globalmente si `pip` te lo bloquea.

### Desde el repositorio

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
porthound
```

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
python -m pip download --dest wheelhouse "wsbuilder>=0.18.0,<0.19.0"
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
