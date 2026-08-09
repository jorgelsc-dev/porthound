# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [Unreleased]
- Prepare `1.0.4` for the isolated Debian runtime venv flow.
- Create `/usr/lib/porthound/venv` during Debian install and update so PortHound keeps its Python runtime outside the system environment.
- Bundle a local wheelhouse in the `.deb` and install dependencies into the app venv without hitting PyPI during `dpkg` or `apt`.
- Follow the latest published `wsbuilder` release instead of pinning a narrow version range.
- Restore `FrontendSecurityPolicy` compatibility with the `wsbuilder` response hook contract.
- Stop background workers cleanly on the first `Ctrl+C`.
- Expose all Vue views in navigation and add a Security/Agents console.

## [1.0.0] - 2025-04-24
### Added
- TCP/UDP scanning engine with progress tracking.
- Banner grabbing for TCP/UDP services.
- SQLite storage for targets, ports, tags, and banners.
- HTTP API and WebSocket demo server.
- Optional Vue frontend.

[Unreleased]: ./
[1.0.0]: ./
