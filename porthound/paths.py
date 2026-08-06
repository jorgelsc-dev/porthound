from __future__ import annotations

from os import getenv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FRONTEND_DIST_DIR = PROJECT_ROOT / "frontend" / "dist"
PACKAGE_FRONTEND_DIST_DIR = PROJECT_ROOT / "porthound" / "_frontend_dist"


def resolve_frontend_dist_dir() -> Path:
    override = str(getenv("PORTHOUND_FRONTEND_DIST", "")).strip()
    candidates: list[Path] = []
    if override:
        candidates.append(Path(override).expanduser())
    candidates.extend([SOURCE_FRONTEND_DIST_DIR, PACKAGE_FRONTEND_DIST_DIR])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]
