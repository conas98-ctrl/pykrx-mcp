"""Explicit MCP tools for pykrx."""

from pykrx_mcp.utils.credential_output import redact_krx_credentials_from_output

# pykrx 1.2.8 authenticates while its modules are imported and prints the
# environment-provided login ID.  Keep dependency diagnostics visible while
# redacting exact credential values before they can reach MCP stdio or logs.
with redact_krx_credentials_from_output():
    from . import _imports

globals().update(_imports.EXPORTED_TOOLS)
__all__ = list(_imports.EXPORTED_TOOL_NAMES)

del _imports
