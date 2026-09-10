"""Provider interfaces.

Providers are adapters to the outside world: Linux, Docker, Cloudflare,
WordPress, storage, backups, and future services.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable, Any

from jamesos.core.models import CheckResult


@runtime_checkable
class Provider(Protocol):
    """Base protocol for JamesOS providers."""

    name: str

    def health(self) -> CheckResult:
        """Return the provider's health."""
        ...

    def inventory(self) -> dict[str, Any]:
        """Return provider inventory."""
        ...
