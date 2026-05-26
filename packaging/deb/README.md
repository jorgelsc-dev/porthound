# Debian packaging

Build a local `.deb` package:

```bash
./packaging/deb/build.sh
```

Custom output dir:

```bash
./packaging/deb/build.sh --output-dir /tmp/deb
```

Install using `apt`:

```bash
sudo apt install ./dist/deb/porthound_<version>-1_all.deb
```

Runtime paths after install:

- App code: `/opt/porthound`
- CLI: `/usr/bin/porthound`

Run in terminal (interactive):

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

If you are upgrading from an older service-based package, stop and disable legacy service mode once:

```bash
sudo systemctl disable --now porthound.service
```
