# Guia de la documentacion

PortHound usa MkDocs Material para publicar la documentacion del proyecto en GitHub Pages. Esta pagina explica como esta organizado el sitio y que archivo tocar cuando agregas contenido.

## Piezas del sitio

- `mkdocs.yml` define la navegacion, el tema, el idioma, los atajos visuales y las extensiones Markdown.
- `docs/` contiene las paginas Markdown, assets y archivos legacy del sitio.
- `docs/index.html` queda como landing heredada, pero `exclude_docs` la saca del build de MkDocs.
- `docs/.nojekyll` evita que GitHub Pages procese el sitio como contenido de Jekyll.
- `.github/workflows/docs-pages.yml` construye `site/` y publica el resultado en GitHub Pages.
- `docs/CNAME` fija el dominio personalizado.
- `docs/404.html` redirige URLs antiguas terminadas en `.md` hacia la ruta publica.

## Estructura recomendada

- `index.md` como portada del producto.
- `getting-started.md` para instalacion y arranque.
- `architecture.md` para explicar el runtime, scanners y flujo de datos.
- `reference/` para API, WebSocket, configuracion, seguridad, persistencia y catalogos.

## Como extenderlo

1. Crea una pagina nueva en `docs/`.
2. Añade la ruta en `mkdocs.yml` dentro de `nav`.
3. Si la pagina cambia el uso de la app, actualiza tambien `README.md`.
4. Mantén los enlaces relativos dentro de `docs/` para que GitHub Pages los resuelva bien.

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
- Si el contenido cambia, revisa tambien `README.md` y los links de soporte.
