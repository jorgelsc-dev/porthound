# Guia de la documentacion

La marca `Made with Material for MkDocs` no se escribe en el contenido: la añade el tema. En PortHound se activa con `theme: name: material` en `mkdocs.yml`.

## Piezas del sitio

- `mkdocs.yml` define la navegacion, el tema, el idioma, los atajos visuales y las extensiones Markdown.
- `docs/` contiene las paginas Markdown y los assets del sitio.
- `docs/index.html` queda como landing heredada, pero `exclude_docs` la saca del build de MkDocs.
- `.github/workflows/docs-pages.yml` construye `site/` y publica el resultado en GitHub Pages.
- `docs/CNAME` fija el dominio personalizado.
- `docs/404.html` redirige URLs antiguas terminadas en `.md` hacia la ruta publica.
- `docs/reference/persistence.md` documenta el equivalente local al patron ORM del proyecto: la capa SQLite que vive en `server.py` y `app.py`.

## Como se copia a otro repo

1. Crea una estructura similar:
   - `docs/` para el contenido.
   - `mkdocs.yml` para la configuracion.
   - `.github/workflows/docs-pages.yml` para el despliegue.
   - `docs/CNAME` si tienes dominio propio.
2. Ajusta `site_name`, `site_description` y `site_author`.
3. Define `nav` con rutas relativas a `docs/`.
4. Usa `theme: name: material` y añade `markdown_extensions` para tabs, TOC y bloques de codigo.
5. Añade `repo_url` y `edit_uri` si quieres boton del repo y enlaces de edicion.

## Workflow recomendado

El flujo de publicación hace esto:

- se dispara en `push` a `main` y en `workflow_dispatch`;
- instala Python y las dependencias de docs;
- ejecuta `mkdocs build --strict`;
- sube `site/` como artifact de Pages;
- despliega con `actions/deploy-pages`.

Eso es preferible a `mkdocs gh-deploy` cuando quieres build reproducible y separacion clara entre construccion y despliegue.

## Puntos delicados

- En `nav`, las rutas son relativas a `docs/`, no al repo.
- Si el sitio vive en un subpath, ajusta `site_url` con la URL canonica completa.
- Si cambias URLs publicas, mantén `docs/404.html` para las rutas heredadas.
- Si el contenido cambia, actualiza tambien `README.md` y los links de soporte.
