"""JamesOS Core application object."""

from __future__ import annotations

from pathlib import Path

from jamesos.core.config import JamesOSConfig
from jamesos.core.models import DoctorReport, InventoryReport
from jamesos.core.registry import Registry
from jamesos.providers.docker import DockerProvider
from jamesos.providers.linux import LinuxProvider


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
        self.registry.register_provider(DockerProvider())

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
