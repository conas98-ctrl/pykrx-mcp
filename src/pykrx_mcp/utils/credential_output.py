"""Keep environment-provided credentials out of dependency output."""

from __future__ import annotations

import os
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from typing import Iterator, TextIO


class _RedactingTextIO:
    """Forward text while replacing exact credential values."""

    def __init__(self, stream: TextIO, secrets: tuple[str, ...]) -> None:
        self._stream = stream
        self._secrets = secrets

    def write(self, text: str) -> int:
        redacted = text
        for secret in self._secrets:
            redacted = redacted.replace(secret, "[REDACTED]")
        self._stream.write(redacted)
        return len(text)

    def flush(self) -> None:
        self._stream.flush()

    def __getattr__(self, name: str):
        return getattr(self._stream, name)


@contextmanager
def safe_dependency_output() -> Iterator[None]:
    """Route dependency output to stderr while redacting KRX credentials."""

    secrets = tuple(
        value
        for name in ("KRX_ID", "KRX_PW")
        if (value := os.getenv(name))
    )
    import sys

    with redirect_stdout(_RedactingTextIO(sys.stderr, secrets)), redirect_stderr(
        _RedactingTextIO(sys.stderr, secrets)
    ):
        yield


# Backward-compatible name for callers added before stdout routing was required.
redact_krx_credentials_from_output = safe_dependency_output
