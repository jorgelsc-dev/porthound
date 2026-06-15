# PortHound Docs

PortHound es un escaner de red para auditorias autorizadas. Esta documentacion recoge el uso del runtime, la arquitectura del sitio y la persistencia SQLite que sostiene la UI local.

## Lo esencial

- `README.md` sigue siendo la fuente de verdad para instalacion y uso rapido.
- `mkdocs.yml` define el sitio publico y el menu.
- `docs/` contiene las paginas Markdown, assets y archivos legacy del sitio.
- `.github/workflows/docs-pages.yml` compila y publica la documentacion en GitHub Pages.

## Accesos rapidos

- [Guia de documentacion](docs-setup.md)
- [Persistencia SQLite](reference/persistence.md)
- [Repositorio](https://github.com/jorgelsc-dev/porthound)

## Desarrollo local

```bash
python -m pip install -r requirements-docs.txt
mkdocs serve
```

!!! warning
    Usa PortHound solo en sistemas, redes y rangos donde tengas autorizacion explicita.
