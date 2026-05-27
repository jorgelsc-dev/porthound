"""Public web-stack facade for PortHound.

This module exists to give the HTTP/WebSocket surface a stable, documented
entry point while `app.py` remains the compatibility bootstrap used by older
imports and tests.
"""

from app import *  # noqa: F401,F403

