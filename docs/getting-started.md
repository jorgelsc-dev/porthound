# Primeros pasos

PortHound puede ejecutarse instalado desde PyPI o desde el repositorio. La ruta normal es simple: arrancar la app, abrir la UI local y empezar con un target.

## Requisitos

- Python 3.12 o superior.
- `wsbuilder>=0.18.0`.

## Instalacion

### Desde PyPI

```bash
python -m pip install --upgrade pip
python -m pip install porthound4
porthound
```

### Desde el repositorio

```bash
python3 -m venv env
env/bin/python -m pip install --upgrade pip
env/bin/python manage.py
```

## Arranque

El launcher local arranca en:

- host: `127.0.0.1`
- port: `45678`
- base de datos: `Standalone.db`

Si abres la UI desde otro origen o detras de un reverse proxy, usa el campo `API base URL` de la portada. El frontend tambien lee `VUE_APP_API_BASE` cuando se construye por separado.

Tambien puedes fijar la base de datos:

```bash
python manage.py --db-path Standalone.db
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
python manage.py
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
