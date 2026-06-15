# Catalogos

PortHound usa catalogos para separar reglas built-in, seeds versionados y entradas editables por el usuario.

## Tipos de catalogo

| Catalogo | Uso | Archivo seed |
| --- | --- | --- |
| Banner regex rules | Extraer servicio, producto, server, version y metadatos desde banners. | `data/banner_regex_rules.json` |
| Banner probe requests | Definir probes TCP o UDP para banner grabbing. | `data/banner_probe_requests.json` |
| IP presets | Guardar IP o CIDR usados con frecuencia. | `data/ip_presets.json` |

## Versiones de catalogo

- `source = builtin` o `source = file` para entradas seed.
- `source = user` para entradas creadas en la UI o por la API.
- `mutable = 0` indica que no se pueden editar ni borrar.
- `mutable = 1` indica que la entrada es editable.
- `active = 1` habilita la entrada; `active = 0` la deshabilita sin eliminarla.

## Catalogos en DB

Los endpoints de DB viven bajo `/api/catalog/...`:

- `banner-rules`
- `banner-requests`
- `ip-presets`

Estos endpoints mezclan registros built-in con registros custom y admiten `GET`, `POST`, `PUT` y `DELETE` segun el catalogo.

## Catalogos de archivo

Los endpoints bajo `/api/catalog/file/...` trabajan directamente sobre los JSON versionados.

- `GET` lee el fichero y devuelve la lista actual.
- `POST` añade una entrada al fichero y la sincroniza en SQLite.

El flujo file-backed es util cuando quieres versionar el seed junto al repo.

## UI relacionada

El codigo del repositorio incluye dos vistas de gestion:

- `CatalogView.vue` para administrar el catalogo DB-backed.
- `FileCatalogView.vue` para administrar el catalogo file-backed.

## Bootstrap

En el arranque, `server.py` carga los seeds, los inserta si faltan y deja la base lista para la UI. Esto significa que los catalogos built-in aparecen aunque el usuario aun no haya creado entradas personalizadas.
