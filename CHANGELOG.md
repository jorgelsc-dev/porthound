# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [Unreleased]
- Prepare `1.0.3` for the Debian-only package flow after removing the legacy PyPI layout.
- Restore `FrontendSecurityPolicy` compatibility with the `wsbuilder` response hook contract.
- Update `wsbuilder` requirement to `>=0.25.7,<0.26.0`.
- Package the `porthound` module entry point and frontend bundle for normal PyPI installs.
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
