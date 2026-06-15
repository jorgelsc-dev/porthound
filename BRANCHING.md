# Branching Rules

This repository keeps the flow intentionally simple:

- `main`: stable release line, protected, release-ready only.
- `feature/*`: new features and larger changes.
- `fix/*`: bug fixes and hot adjustments.
- `docs/*`: documentation-only work.
- `chore/*`: maintenance and dependency updates.
- `release/*`: optional cut branches when preparing a release candidate.

Rules:

1. Open pull requests into `main` for normal work.
2. Keep `main` green and minimal.
3. Use semantic version tags for releases.
4. Do not commit generated artifacts, virtual environments, or local databases.

Suggested CI flow:

- run tests on `main` and auxiliary branches
- publish packages only from `main` or a tagged release
