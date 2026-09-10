"""JamesOS Core application object."""

from __future__ import annotations

from pathlib import Path

from jamesos.core.config import JamesOSConfig
from jamesos.core.models import DoctorReport, InventoryReport
from jamesos.core.registry import Registry
from jamesos.providers.backups import BackupsProvider
from jamesos.providers.docker import DockerProvider
from jamesos.providers.gateway import GatewayProvider
from jamesos.providers.linux import LinuxProvider
from jamesos.providers.nextcloud import NextcloudProvider
from jamesos.providers.open_webui import OpenWebUIProvider
from jamesos.providers.storage import StorageProvider
from jamesos.providers.wordpress import WordPressProvider


class JamesOS:
    """Core runtime for the JamesOS platform.

    The core owns configuration, provider registration, and high-level
    operations.  Interfaces such as the CLI, a future REST API, Homepage, or AI
    assistants should call this object instead of calling system tools directly.
    """

    def __init__(self, config: JamesOSConfig | None = None) -> None:
        self.config = config or JamesOSConfig.from_repo_root(Path.cwd())
        self.registry = Registry()
        self._register_builtin_providers()

    def _register_builtin_providers(self) -> None:
        self.registry.register_provider(LinuxProvider())
        self.registry.register_provider(StorageProvider())
        self.registry.register_provider(GatewayProvider())
        self.registry.register_provider(DockerProvider())
        self.registry.register_provider(WordPressProvider())
        self.registry.register_provider(NextcloudProvider())
        self.registry.register_provider(OpenWebUIProvider())
        self.registry.register_provider(BackupsProvider())

    def doctor(self) -> DoctorReport:
        report = DoctorReport()
        for provider in self.registry.providers.values():
            report.add(provider.health())
        return report

    def inventory(self) -> InventoryReport:
        report = InventoryReport()
        for name, provider in self.registry.providers.items():
            report.add_section(name, provider.inventory())
        return report
