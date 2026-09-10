"""Provider and plugin registry for JamesOS."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jamesos.core.provider import Provider


@dataclass(slots=True)
class Registry:
    """Runtime registry for providers and future plugins."""

    providers: dict[str, Provider] = field(default_factory=dict)
    plugins: dict[str, Any] = field(default_factory=dict)

    def register_provider(self, provider: Provider) -> None:
        self.providers[provider.name] = provider

    def get_provider(self, name: str) -> Provider:
        return self.providers[name]

    def register_plugin(self, name: str, plugin: Any) -> None:
        self.plugins[name] = plugin

    def provider_names(self) -> list[str]:
        return sorted(self.providers)
