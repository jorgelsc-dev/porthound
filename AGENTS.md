# Repository Guidelines

## Project Structure & Module Organization
PortHound is a Python 3.12 standalone network scanner with an optional Vue 3 + Vuetify frontend. Core Python modules live at the repo root (`app.py`, `server.py`, `manage.py`, `utils.py`, `scan_payloads.py`, `geoip_seed.py`, and related helpers). Tests live in `tests/`, with the main suite currently in `tests/test_core_hardening.py`. Frontend code lives in `frontend/src/`: page views in `views/`, shared UI in `components/`, routing in `router/`, and app state in `state/`. Docs live in `docs/` with config in `mkdocs.yml`; `docs/index.html` is a legacy landing page kept out of the MkDocs build by `exclude_docs`. Static assets are in `frontend/public/`, versioned seed/data files are in `data/`, and release helpers are in `packaging/`.

## Build, Test, and Development Commands
- `python manage.py` starts the standalone backend on `127.0.0.1:45678`.
- `python -m compileall -q .` checks Python syntax across the repo.
- `python -m unittest discover -s tests -q` runs the backend test suite.
- `cd frontend && npm ci` installs frontend dependencies from `package-lock.json`.
- `cd frontend && npm run lint` runs ESLint over `.js` and `.vue` files.
- `cd frontend && npm run build` creates the production frontend bundle.
- `cd frontend && npm run serve` runs the local frontend dev server.
- `python -m pip install -r requirements-docs.txt && mkdocs build --strict` validates the MkDocs site.

## Coding Style & Naming Conventions
Use 4-space indentation in Python. Keep module and function names `snake_case`, classes `PascalCase`, and constants `UPPER_SNAKE_CASE`. For Vue and JavaScript, follow the existing ESLint flat config, use 2-space indentation, and prefer descriptive filenames such as `AppTopBar.vue` or `PortsView.vue`. No formatter is enforced, so match nearby code and keep changes small.

## Testing Guidelines
Add or extend `unittest` cases under `tests/` using `Test*` classes and `test_*` methods. Prefer focused tests that cover input validation, protocol handling, and serialization behavior. Before opening a PR, run the Python syntax check, backend tests, and frontend lint/build steps above.

## Commit & Pull Request Guidelines
History uses short, imperative subjects with prefixes like `fix:`, `docs:`, `refactor:`, `test:`, and `chore(deps):`. Keep each commit to one logical change. Branch from `main` using `feature/*`, `fix/*`, `docs/*`, or `chore/*`. Pull requests should target `main`, fill out `.github/pull_request_template.md`, include validation output, and add screenshots for UI changes.

## Security & Configuration Tips
Treat scans as authorized-only work. Do not commit generated artifacts, virtual environments, or local databases such as `Standalone.db`. Keep secrets in environment variables, and document any new configuration keys in `README.md` or `SECURITY.md` when needed.
