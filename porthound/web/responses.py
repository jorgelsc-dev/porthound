from __future__ import annotations

import mimetypes
from pathlib import Path

from wsbuilder import Response, Route

from porthound.paths import resolve_frontend_dist_dir


SPA_ROUTES = (
    "/map",
    "/charts",
    "/explorer",
    "/agents",
    "/targets",
    "/ports",
    "/banners",
    "/tags",
    "/catalog",
    "/files",
    "/security",
    "/api",
)

STATIC_CONTENT_TYPE_OVERRIDES = {
    ".js": "application/javascript; charset=utf-8",
    ".mjs": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".map": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
}


def dist_file_response(file_path: Path, cache_control="public, max-age=300"):
    try:
        body = file_path.read_bytes()
    except Exception:
        return Response.text("Not Found", status=404)

    suffix = file_path.suffix.lower()
    content_type = STATIC_CONTENT_TYPE_OVERRIDES.get(suffix)
    if not content_type:
        guessed, _ = mimetypes.guess_type(str(file_path))
        content_type = guessed or "application/octet-stream"
        if content_type.startswith("text/") and "charset=" not in content_type:
            content_type += "; charset=utf-8"

    headers = {"Content-Type": content_type}
    if cache_control:
        headers["Cache-Control"] = cache_control
    return Response(status=200, body=body, headers=headers)


def frontend_index_response(frontend_dist_dir=None, fallback_html=""):
    dist_dir = Path(frontend_dist_dir) if frontend_dist_dir else resolve_frontend_dist_dir()
    index_path = dist_dir / "index.html"
    if index_path.is_file():
        return dist_file_response(index_path, cache_control="no-cache")
    return Response.html(fallback_html)


def register_frontend_dist_routes(
    app,
    frontend_dist_dir=None,
    *,
    route_state=None,
    log_missing=True,
):
    state = route_state if route_state is not None else {}
    if state.get("registered"):
        return

    dist_dir = Path(frontend_dist_dir) if frontend_dist_dir else resolve_frontend_dist_dir()
    if not dist_dir.is_dir():
        if log_missing:
            print(f"[frontend] dist not found: {dist_dir}")
        state["registered"] = True
        return

    for file_path in sorted(dist_dir.rglob("*")):
        if not file_path.is_file():
            continue
        route_path = "/" + file_path.relative_to(dist_dir).as_posix()
        if app.router.resolve(route_path, method="GET"):
            continue

        def static_handler(request, _file_path=file_path):
            return dist_file_response(_file_path)

        app.router.add(Route(route_path, ("GET",), static_handler, "plain"))

    state["registered"] = True


def wants_html(request):
    fmt = request.query.get("format")
    if fmt == "html":
        return True
    if fmt == "json":
        return False
    accept = str(request.headers.get("accept", "") or "").lower()
    if "application/json" in accept and "text/html" not in accept:
        return False
    return True


def json_error(message, status=500):
    return Response.json({"status": str(message)}, status=status)
