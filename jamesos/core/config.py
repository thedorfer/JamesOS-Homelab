"""Configuration loading for JamesOS."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class JamesOSConfig:
    """Runtime configuration for JamesOS.

    v0 keeps configuration intentionally small.  Later versions can load TOML
    from /etc/jamesos, ~/.config/jamesos, or the repository root.
    """

    repo_root: Path
    domain: str = "jamesallendoerfer.com"
    desktop_host: str = "desktop"
    pi_gateway_host: str = "pi-gateway"

    @classmethod
    def from_repo_root(cls, repo_root: Path | None = None) -> "JamesOSConfig":
        if repo_root is None:
            repo_root = Path.cwd()
        return cls(repo_root=repo_root.resolve())
