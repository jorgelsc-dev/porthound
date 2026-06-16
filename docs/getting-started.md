# Primeros pasos

PortHound puede ejecutarse como binario instalado desde PyPI o como checkout local. La experiencia principal es la misma: levantar el launcher, abrir la UI local y operar targets o consultas desde el navegador.

## Requisitos

- Python 3.12 o superior.
- `wsbuilder>=0.18.0`.
- Acceso local al puerto HTTP configurado, por defecto `127.0.0.1:45678`.

## Instalacion rapida

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

## Arranque local

El launcher local usa estos valores por defecto:

- host: `127.0.0.1`
- port: `45678`
- base de datos: `Standalone.db`

Si abres la UI desde otro origen o detras de un reverse proxy, usa el campo `API base URL` de la portada para apuntar al backend correcto. El frontend tambien lee `VUE_APP_API_BASE` cuando se construye por separado.

Tambien puedes fijar la base de datos explicitamente:

```bash
python manage.py --db-path Standalone.db
```

## Uso inicial

1. Abre `http://127.0.0.1:45678`.
2. Revisa el chip de `Auth` en la barra superior.
3. Si el backend exige token, guarda el valor en el dialogo de acceso.
4. Trabaja con `Targets`, `Ports`, `Banners` y `API` desde la navegacion principal.
5. Si necesitas la UI separada del backend, ajusta la base de API antes de empezar.

## Token de acceso

Cuando `PORTHOUND_API_TOKEN` esta configurado, la UI envia el token como `Authorization: Bearer` o `X-API-Key` segun el cliente. El valor se conserva en `sessionStorage` para la sesion actual del navegador.

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

Documentacion local:

```bash
python -m pip install -r requirements-docs.txt
mkdocs serve
```

Validacion basica:

```bash
python -m compileall -q .
python -m unittest discover -s tests -q
```

!!! warning
    Usa PortHound solo en sistemas, redes y rangos donde tengas autorizacion explicita.
