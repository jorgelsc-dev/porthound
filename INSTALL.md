# Install

## Requirements
- Python 3.11+
- Node.js 18+ (only for frontend)

If you only want the published package, install it from PyPI:

```bash
python3 -m pip install porthound
```

## Backend
```bash
python3 -m venv env
env/bin/python -m pip install --upgrade pip
env/bin/python manage.py
```

Default run mode is `master` on `0.0.0.0:45678` with role DB (`Master.db` by default).

For distributed mode (`master + agent`), follow `README.md`.

## Frontend
```bash
cd frontend
npm install
npm run serve
```

## Debian / APT package (`.deb`)

Build package:

```bash
./packaging/deb/build.sh
```

Install with `apt`:

```bash
sudo apt install ./dist/deb/porthound_<version>-1_all.deb
```

Run interactively:

```bash
porthound
# stop with Ctrl+C
```

Explicit master example:

```bash
porthound --role master --host 0.0.0.0 --port 45678 --db-path ./Master.db
```

Agent example:

```bash
porthound --role agent --master http://127.0.0.1:45678 --agent-id <id> --agent-token <token>
```

If you are upgrading from an old service-based install:

```bash
sudo systemctl disable --now porthound.service
```

## Portable ZIP package

Build package:

```bash
./packaging/zip/build.sh
```

Extract and run:

```bash
unzip dist/zip/porthound_<version>-1.zip
cd porthound_<version>-1
python3 manage.py
```
