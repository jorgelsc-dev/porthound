from __future__ import annotations

from .responses import (
    SPA_ROUTES,
    STATIC_CONTENT_TYPE_OVERRIDES,
    dist_file_response,
    frontend_index_response,
    json_error,
    register_frontend_dist_routes,
    wants_html,
)

__all__ = [
    "SPA_ROUTES",
    "STATIC_CONTENT_TYPE_OVERRIDES",
    "dist_file_response",
    "frontend_index_response",
    "json_error",
    "register_frontend_dist_routes",
    "wants_html",
]
