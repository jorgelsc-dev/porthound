from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


SEMVER_TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
MAIN_DEB_TAG_RE = re.compile(r"^main-deb-[0-9]+\.[0-9]+-[0-9a-f]{7,40}$")
BREAKING_SUBJECT_RE = re.compile(r"^[A-Za-z]+(?:\([^)]+\))?!:")
CONVENTIONAL_SUBJECT_RE = re.compile(r"^([A-Za-z]+)(?:\([^)]+\))?(!)?:")

PATCH_ONLY_PATHS = {
    ".gitignore",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "SUPPORT.md",
    "BRANCHING.md",
    "CITATION.cff",
}
PATCH_ONLY_PREFIXES = (
    ".github/",
    "docs/",
    "packaging/",
    "tests/",
)
RUNTIME_CHANGE_PATHS = {
    "agent.py",
    "app.py",
    "banner_rules.py",
    "country_centroids.py",
    "dns.py",
    "framework.py",
    "geoip_seed.py",
    "getDBNIC.py",
    "getData.py",
    "manage.py",
    "master.py",
    "runtime_paths.py",
    "scan_payloads.py",
    "server.py",
    "settings.py",
    "utils.py",
    "views.py",
    "ws_demo.py",
}
RUNTIME_CHANGE_PREFIXES = (
    "data/",
    "frontend/public/",
    "frontend/src/",
    "porthound/",
)

BUMP_ORDER = {"none": 0, "patch": 1, "minor": 2, "major": 3}


@dataclass(frozen=True)
class CommitChange:
    sha: str
    subject: str
    body: str
    files: tuple[str, ...]
    bump: str


@dataclass(frozen=True)
class VersionResolution:
    version: str
    bump: str
    baseline_version: str
    baseline_ref: str
    tag: str
    commit_count: int
    commits: tuple[CommitChange, ...]
    source: str


def parse_version(text: str) -> tuple[int, int, int]:
    raw = str(text or "").strip()
    match = SEMVER_TAG_RE.match(raw if raw.startswith("v") else f"v{raw}")
    if not match:
        raise ValueError(f"Invalid semantic version: {text!r}")
    return tuple(int(group) for group in match.groups())


def format_version(parts: tuple[int, int, int]) -> str:
    major, minor, patch = parts
    return f"{major}.{minor}.{patch}"


def bump_version(version: str, bump: str) -> str:
    major, minor, patch = parse_version(version)
    normalized = str(bump or "").strip().lower()
    if normalized == "major":
        return format_version((major + 1, 0, 0))
    if normalized == "minor":
        return format_version((major, minor + 1, 0))
    if normalized == "patch":
        return format_version((major, minor, patch + 1))
    return version


def combine_bumps(left: str, right: str) -> str:
    return left if BUMP_ORDER.get(left, 0) >= BUMP_ORDER.get(right, 0) else right


def _is_patch_only_path(path: str) -> bool:
    normalized = str(path or "").strip()
    if not normalized:
        return True
    if normalized in PATCH_ONLY_PATHS:
        return True
    return any(normalized.startswith(prefix) for prefix in PATCH_ONLY_PREFIXES)


def _is_runtime_change_path(path: str) -> bool:
    normalized = str(path or "").strip()
    if not normalized:
        return False
    if normalized in RUNTIME_CHANGE_PATHS:
        return True
    return any(normalized.startswith(prefix) for prefix in RUNTIME_CHANGE_PREFIXES)


def classify_commit_bump(subject: str, body: str, files: tuple[str, ...] | list[str]) -> str:
    normalized_subject = str(subject or "").strip()
    normalized_body = str(body or "").strip()
    normalized_files = tuple(str(path or "").strip() for path in files if str(path or "").strip())

    if BREAKING_SUBJECT_RE.match(normalized_subject):
        return "major"
    if "BREAKING CHANGE:" in normalized_body or "BREAKING-CHANGE:" in normalized_body:
        return "major"

    conventional = CONVENTIONAL_SUBJECT_RE.match(normalized_subject)
    if conventional:
        kind = str(conventional.group(1) or "").strip().lower()
        has_break = bool(conventional.group(2))
        if has_break:
            return "major"
        if kind == "feat":
            return "minor"
        return "patch"

    if normalized_files and all(_is_patch_only_path(path) for path in normalized_files):
        return "patch"
    if any(_is_runtime_change_path(path) for path in normalized_files):
        return "minor"
    return "patch"


def _repo_root(start: str | Path | None = None) -> Path:
    return Path(start or ".").resolve()


def _read_pyproject_version(root: Path) -> str:
    pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    return str(pyproject["project"]["version"]).strip()


def _git_output(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(root),
        check=True,
        capture_output=True,
        text=True,
    )
    return str(completed.stdout or "").strip()


def _git_available(root: Path) -> bool:
    if not (root / ".git").exists():
        return False
    try:
        _git_output(root, "rev-parse", "--git-dir")
    except Exception:
        return False
    return True


def _latest_tag(root: Path, pattern: re.Pattern[str]) -> str:
    try:
        raw = _git_output(root, "tag", "--merged", "HEAD", "--sort=-v:refname")
    except Exception:
        return ""
    for line in raw.splitlines():
        candidate = str(line or "").strip()
        if pattern.match(candidate):
            return candidate
    return ""


def _head_semver_tag(root: Path) -> str:
    try:
        raw = _git_output(root, "tag", "--points-at", "HEAD")
    except Exception:
        return ""
    tags = [
        tag
        for tag in (str(line or "").strip() for line in raw.splitlines())
        if SEMVER_TAG_RE.match(tag)
    ]
    if not tags:
        return ""
    tags.sort(key=parse_version, reverse=True)
    return tags[0]


def _commit_range(root: Path, baseline_ref: str) -> list[str]:
    if not baseline_ref:
        return []
    try:
        raw = _git_output(root, "rev-list", "--reverse", "--no-merges", f"{baseline_ref}..HEAD")
    except Exception:
        raw = ""
    commits = [line.strip() for line in raw.splitlines() if line.strip()]
    if commits:
        return commits
    try:
        raw = _git_output(root, "rev-list", "--reverse", f"{baseline_ref}..HEAD")
    except Exception:
        raw = ""
    return [line.strip() for line in raw.splitlines() if line.strip()]


def _commit_message(root: Path, sha: str) -> tuple[str, str]:
    raw = _git_output(root, "show", "-s", "--format=%s%n%b", sha)
    lines = raw.splitlines()
    subject = lines[0].strip() if lines else ""
    body = "\n".join(lines[1:]).strip()
    return subject, body


def _commit_files(root: Path, sha: str) -> tuple[str, ...]:
    raw = _git_output(root, "diff-tree", "--no-commit-id", "--name-only", "-r", sha)
    return tuple(line.strip() for line in raw.splitlines() if line.strip())


def resolve_version(root: str | Path | None = None) -> VersionResolution:
    repo_root = _repo_root(root)
    baseline_version = _read_pyproject_version(repo_root)

    if not _git_available(repo_root):
        return VersionResolution(
            version=baseline_version,
            bump="none",
            baseline_version=baseline_version,
            baseline_ref="",
            tag=f"v{baseline_version}",
            commit_count=0,
            commits=(),
            source="pyproject",
        )

    head_tag = _head_semver_tag(repo_root)
    if head_tag:
        resolved_version = head_tag[1:]
        return VersionResolution(
            version=resolved_version,
            bump="none",
            baseline_version=resolved_version,
            baseline_ref=head_tag,
            tag=head_tag,
            commit_count=0,
            commits=(),
            source="tag",
        )

    baseline_ref = _latest_tag(repo_root, SEMVER_TAG_RE)
    source = "semver-tag"
    if baseline_ref:
        baseline_version = baseline_ref[1:]
    else:
        baseline_ref = _latest_tag(repo_root, MAIN_DEB_TAG_RE)
        source = "main-deb-tag" if baseline_ref else "pyproject"

    if not baseline_ref:
        return VersionResolution(
            version=baseline_version,
            bump="none",
            baseline_version=baseline_version,
            baseline_ref="",
            tag=f"v{baseline_version}",
            commit_count=0,
            commits=(),
            source=source,
        )

    commits = []
    highest_bump = "none"
    for sha in _commit_range(repo_root, baseline_ref):
        subject, body = _commit_message(repo_root, sha)
        files = _commit_files(repo_root, sha)
        bump = classify_commit_bump(subject, body, files)
        highest_bump = combine_bumps(highest_bump, bump)
        commits.append(
            CommitChange(
                sha=sha,
                subject=subject,
                body=body,
                files=files,
                bump=bump,
            )
        )

    resolved_version = bump_version(baseline_version, highest_bump)
    return VersionResolution(
        version=resolved_version,
        bump=highest_bump,
        baseline_version=baseline_version,
        baseline_ref=baseline_ref,
        tag=f"v{resolved_version}",
        commit_count=len(commits),
        commits=tuple(commits),
        source=source,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve the next PortHound semantic version from Git history.")
    parser.add_argument("--root", default=".", help="Repository root. Defaults to the current directory.")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON instead of the bare version.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    resolved = resolve_version(args.root)
    if args.json:
        print(
            json.dumps(
                {
                    "version": resolved.version,
                    "bump": resolved.bump,
                    "baseline_version": resolved.baseline_version,
                    "baseline_ref": resolved.baseline_ref,
                    "tag": resolved.tag,
                    "commit_count": resolved.commit_count,
                    "source": resolved.source,
                    "commits": [
                        {
                            "sha": commit.sha,
                            "subject": commit.subject,
                            "files": list(commit.files),
                            "bump": commit.bump,
                        }
                        for commit in resolved.commits
                    ],
                },
                ensure_ascii=True,
            )
        )
    else:
        print(resolved.version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
