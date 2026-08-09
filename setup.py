from __future__ import annotations

from distutils.errors import DistutilsFileError
import shutil
import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = ROOT / "frontend"
FRONTEND_SOURCE_DIR = FRONTEND_DIR / "dist"
PACKAGE_FRONTEND_DIR = ("porthound", "_frontend_dist")


def _build_frontend_if_needed() -> None:
    if FRONTEND_SOURCE_DIR.exists():
        return
    if not FRONTEND_DIR.exists():
        raise DistutilsFileError(
            "frontend/ is missing from the source tree. Rebuild the source distribution with "
            "frontend sources included, or restore frontend/ before packaging PortHound."
        )

    npm = shutil.which("npm")
    if npm is None:
        raise DistutilsFileError(
            "frontend/dist is missing and npm is unavailable. Install Node.js 20 LTS or newer, then run "
            "'npm ci && npm run build' in frontend/ before packaging PortHound."
        )

    try:
        subprocess.run([npm, "ci"], cwd=FRONTEND_DIR, check=True)
        subprocess.run([npm, "run", "build"], cwd=FRONTEND_DIR, check=True)
    except subprocess.CalledProcessError as exc:
        raise DistutilsFileError(
            "PortHound could not build the frontend automatically. Run 'npm ci && npm run build' "
            "in frontend/ and try again."
        ) from exc


class build_py(_build_py):
    def _frontend_output_pairs(self) -> list[tuple[str, str]]:
        _build_frontend_if_needed()
        if getattr(self, "editable_mode", False):
            return []
        if not FRONTEND_SOURCE_DIR.exists():
            return []

        target_root = Path(self.build_lib).joinpath(*PACKAGE_FRONTEND_DIR)
        pairs: list[tuple[str, str]] = []
        for source in FRONTEND_SOURCE_DIR.rglob("*"):
            if not source.is_file():
                continue
            target = target_root / source.relative_to(FRONTEND_SOURCE_DIR)
            pairs.append((str(target), str(source)))
        return pairs

    def build_package_data(self) -> None:
        super().build_package_data()

        for target, source in self._frontend_output_pairs():
            target_path = Path(target)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            self.copy_file(source, target)

    def get_output_mapping(self) -> dict[str, str]:
        mapping = super().get_output_mapping()
        for target, source in self._frontend_output_pairs():
            mapping[target] = source
        return mapping


setup(cmdclass={"build_py": build_py})
