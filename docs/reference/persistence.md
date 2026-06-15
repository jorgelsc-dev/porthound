# Persistencia SQLite

PortHound no usa un ORM estilo Django. Su capa de datos vive en `server.py` y `app.py`, donde se comparten constantes, validaciones y el acceso a SQLite que alimenta la UI.

## Que documenta esta capa

- `server.py` concentra el modelo operacional: rangos, protocolos, normalizacion y helpers de base de datos.
- `app.py` expone esos datos por HTTP y WebSocket.
- `Standalone.db` sigue siendo la base por defecto del runtime local.
- `data/` contiene seeds y catálogos que complementan la persistencia.

## Cuando cambiarla

Si agregas campos, tablas o reglas nuevas:

1. actualiza el esquema y los helpers de normalizacion;
2. revisa los tests que dependen de `Standalone.db` o de datos temporales;
3. añade una nota en la documentacion publica si el cambio afecta al flujo de usuario.

## Regla practica

Si buscas el punto de entrada para entender la persistencia, empieza por `server.py` y sigue el flujo hacia `app.py`. Ese par sustituye aqui al estilo `orm.py` de otros proyectos.
