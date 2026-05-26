from __future__ import annotations

import os
import sys
import sysconfig
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_ENV_VAR = "PORTHOUND_DATA_DIR"


def _candidate_data_dirs():
    env_value = str(os.environ.get(DATA_ENV_VAR, "") or "").strip()
    if env_value:
        yield Path(env_value).expanduser()

    try:
        data_root = sysconfig.get_paths().get("data")
    except Exception:
        data_root = None
    if data_root:
        yield Path(data_root) / "porthound" / "data"

    if getattr(sys, "prefix", ""):
        prefix = Path(sys.prefix)
        yield prefix / "porthound" / "data"
        yield prefix / "share" / "porthound" / "data"

    yield PROJECT_ROOT / "data"


def resolve_data_dir() -> Path:
    for candidate in _candidate_data_dirs():
        if candidate.exists():
            return candidate
    return PROJECT_ROOT / "data"


def resolve_data_file(name: str) -> Path:
    return resolve_data_dir() / name
