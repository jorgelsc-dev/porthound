#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${ROOT_DIR}"

PACKAGE_NAME="${PACKAGE_NAME:-porthound}"
REVISION="${REVISION:-1}"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

require_command python3
require_command dpkg-deb
require_command sha256sum
python3 -m pip --version >/dev/null

ARCHITECTURE="${DEB_ARCHITECTURE:-$(dpkg --print-architecture)}"
VERSION="$(python3 - <<'PY'
import tomllib
from pathlib import Path

pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
print(pyproject["project"]["version"])
PY
)"
DESCRIPTION="$(python3 - <<'PY'
import tomllib
from pathlib import Path

pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
print(pyproject["project"]["description"])
PY
)"

DIST_DIR="${ROOT_DIR}/dist/deb"
WORK_DIR="${DIST_DIR}/.build"
PACKAGE_BASENAME="${PACKAGE_NAME}_${VERSION}-${REVISION}_${ARCHITECTURE}"
STAGE_DIR="${WORK_DIR}/${PACKAGE_BASENAME}"
PKGROOT="${STAGE_DIR}/pkgroot"
APP_ROOT="${PKGROOT}/usr/lib/${PACKAGE_NAME}/app"
WHEELHOUSE_ROOT="${PKGROOT}/usr/lib/${PACKAGE_NAME}/wheels"
BIN_DIR="${PKGROOT}/usr/bin"
DOC_DIR="${PKGROOT}/usr/share/doc/${PACKAGE_NAME}"
CONTROL_DIR="${PKGROOT}/DEBIAN"
DEB_FILE="${DIST_DIR}/${PACKAGE_BASENAME}.deb"
CHECKSUM_FILE="${DEB_FILE}.sha256"

if [[ ! -d "${ROOT_DIR}/frontend/dist" ]]; then
  require_command npm
  (
    cd "${ROOT_DIR}/frontend"
    npm ci
    npm run build
  )
fi

rm -rf "${STAGE_DIR}" "${DEB_FILE}" "${CHECKSUM_FILE}"
mkdir -p "${APP_ROOT}" "${WHEELHOUSE_ROOT}" "${BIN_DIR}" "${DOC_DIR}" "${CONTROL_DIR}"

python3 - <<'PY' "${ROOT_DIR}" "${APP_ROOT}"
from __future__ import annotations

import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1])
app_root = Path(sys.argv[2])

ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")

for source in sorted(root.glob("*.py")):
    shutil.copy2(source, app_root / source.name)

for relative in ("porthound", "data"):
    shutil.copytree(root / relative, app_root / relative, ignore=ignore)

frontend_dist = root / "frontend" / "dist"
target_frontend_dist = app_root / "frontend" / "dist"
target_frontend_dist.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(frontend_dist, target_frontend_dist, ignore=ignore)

for relative in ("README.md", "LICENSE", "CHANGELOG.md", "requirements.txt"):
    source = root / relative
    if source.exists():
        shutil.copy2(source, app_root / relative)
PY

mapfile -t PROJECT_DEPENDENCIES < <(
  awk '
    /^[[:space:]]*#/ { next }
    /^[[:space:]]*$/ { next }
    { print }
  ' requirements.txt
)

if (( ${#PROJECT_DEPENDENCIES[@]} > 0 )); then
  python3 -m pip wheel --no-cache-dir --wheel-dir "${WHEELHOUSE_ROOT}" "${PROJECT_DEPENDENCIES[@]}"
fi

cat > "${BIN_DIR}/porthound" <<EOF
#!/bin/sh
set -eu
VENV_PYTHON="/usr/lib/${PACKAGE_NAME}/venv/bin/python"
if [ ! -x "\${VENV_PYTHON}" ]; then
  printf '%s\n' "PortHound runtime venv is missing. Reinstall with: sudo apt install --reinstall ${PACKAGE_NAME}" >&2
  exit 1
fi
export PYTHONPATH="/usr/lib/${PACKAGE_NAME}/app\${PYTHONPATH:+:\$PYTHONPATH}"
exec "\${VENV_PYTHON}" /usr/lib/${PACKAGE_NAME}/app/manage.py "\$@"
EOF
chmod 0755 "${BIN_DIR}/porthound"

cp README.md "${DOC_DIR}/README.md"
cp CHANGELOG.md "${DOC_DIR}/CHANGELOG.md"
cp LICENSE "${DOC_DIR}/copyright"
chmod 0644 "${DOC_DIR}/README.md" "${DOC_DIR}/CHANGELOG.md" "${DOC_DIR}/copyright"

INSTALLED_SIZE="$(du -sk "${PKGROOT}" | cut -f1)"

cat > "${CONTROL_DIR}/control" <<EOF
Package: ${PACKAGE_NAME}
Version: ${VERSION}-${REVISION}
Section: net
Priority: optional
Architecture: ${ARCHITECTURE}
Maintainer: PortHound Authors
Depends: python3 (>= 3.12), python3-venv
Installed-Size: ${INSTALLED_SIZE}
Homepage: https://github.com/jorgelsc-dev/porthound
Description: ${DESCRIPTION}
 Standalone network scanner with local API, WebSocket and frontend bundle.
EOF
chmod 0644 "${CONTROL_DIR}/control"

cat > "${CONTROL_DIR}/postinst" <<EOF
#!/bin/sh
set -eu

APP_ROOT="/usr/lib/${PACKAGE_NAME}/app"
VENV_ROOT="/usr/lib/${PACKAGE_NAME}/venv"
WHEELHOUSE_ROOT="/usr/lib/${PACKAGE_NAME}/wheels"

case "\${1:-configure}" in
  configure)
    rm -rf "\${VENV_ROOT}"
    /usr/bin/python3 -m venv "\${VENV_ROOT}"
    "\${VENV_ROOT}/bin/python" -m pip install \
      --disable-pip-version-check \
      --no-cache-dir \
      --no-index \
      --find-links "\${WHEELHOUSE_ROOT}" \
      --upgrade \
      -r "\${APP_ROOT}/requirements.txt"
    ;;
esac

exit 0
EOF
chmod 0755 "${CONTROL_DIR}/postinst"

cat > "${CONTROL_DIR}/postrm" <<EOF
#!/bin/sh
set -eu

case "\${1:-remove}" in
  remove|purge)
    rm -rf "/usr/lib/${PACKAGE_NAME}/venv"
    ;;
esac

exit 0
EOF
chmod 0755 "${CONTROL_DIR}/postrm"

find "${PKGROOT}" -type d -exec chmod 0755 {} +
find "${PKGROOT}" -type f ! -path "${BIN_DIR}/porthound" -exec chmod 0644 {} +
chmod 0755 "${BIN_DIR}/porthound"
chmod 0755 "${CONTROL_DIR}/postinst" "${CONTROL_DIR}/postrm"

dpkg-deb --root-owner-group --build "${PKGROOT}" "${DEB_FILE}"
sha256sum "${DEB_FILE}" > "${CHECKSUM_FILE}"

echo "Built Debian package: ${DEB_FILE}"
echo "Checksum written to: ${CHECKSUM_FILE}"
