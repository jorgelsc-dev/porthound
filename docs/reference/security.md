# Seguridad

PortHound asume un modelo de uso autorizado. La superficie administrativa no esta pensada para exponerse sin control, y la mayoria de acciones de escritura requieren autenticar o venir desde loopback.

## Acceso administrativo

`require_admin_access()` aplica esta secuencia:

1. Si `PORTHOUND_API_TOKEN` esta configurado, la peticion debe enviar el token.
2. Si `PORTHOUND_API_REQUIRE_TOKEN=1`, el token es obligatorio aunque el cliente sea local.
3. Si no hay token, solo se permite acceso desde loopback.
4. Si el cliente es loopback pero el `Origin` no es loopback, la peticion se deniega.
5. La UI valida el token contra `/api/ws/clients` antes de marcarlo como autenticado.

El token se acepta en:

- `Authorization: Bearer <token>`
- `X-API-Key: <token>`

## UI y navegador

- La UI guarda el token en `sessionStorage`.
- La base de la API se guarda en `localStorage`.
- Si el backend responde `401`, el dialogo de autenticacion se abre de nuevo.

## TLS y CA

- `PORTHOUND_TLS_ENABLED` esta desactivado por defecto en la rama publica.
- La distribucion de CA y el enrollment por certificado estan deshabilitados en la ruta publica actual.
- `/api/cluster/ca`, `/api/cluster/ca/raw`, `/api/cluster/ca/oneline` y `/api/cluster/agent/enroll` devuelven `410 Gone`.

## Claves de agente

Los tokens de cluster se guardan como hash SHA-256 en SQLite, no como texto plano. Las rutas de registro, heartbeat y tareas usan ese token para validar al agente.

## Recomendaciones

- No expongas el backend sin token si no es estrictamente local.
- Si necesitas exponerlo, usa TLS externo o un reverse proxy controlado.
- Mantén `PORTHOUND_API_TOKEN` en un gestor de secretos, no en el repo.
- Revisa el `Origin` cuando habilites integraciones web.

!!! warning
    PortHound solo debe usarse en sistemas, redes y rangos donde tengas autorizacion explicita.
