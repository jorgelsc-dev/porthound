"""Compatibility shim for PortHound.

The new generation of PortHound uses the external `wsbuilder` package
instead of carrying a local copy of the framework internals.
"""

from wsbuilder.framework import *  # noqa: F401,F403
from wsbuilder.framework import __all__ as _WSBUILDER_FRAMEWORK_ALL

__all__ = list(_WSBUILDER_FRAMEWORK_ALL)
