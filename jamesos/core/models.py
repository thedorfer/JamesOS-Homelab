"""Shared data models for JamesOS."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

Status = Literal["ok", "warn", "fail", "unknown"]


@dataclass(slots=True)
class CheckResult:
    """Result of a single health or doctor check."""

    name: str
    status: Status
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.status == "ok"


@dataclass(slots=True)
class DoctorReport:
    """Aggregated health report for the platform."""

    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    checks: list[CheckResult] = field(default_factory=list)

    def add(self, result: CheckResult) -> None:
        self.checks.append(result)

    @property
    def status(self) -> Status:
        if any(check.status == "fail" for check in self.checks):
            return "fail"
        if any(check.status == "warn" for check in self.checks):
            return "warn"
        if self.checks and all(check.status == "ok" for check in self.checks):
            return "ok"
        return "unknown"


@dataclass(slots=True)
class InventoryReport:
    """Structured inventory returned by providers."""

    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    sections: dict[str, dict[str, Any]] = field(default_factory=dict)

    def add_section(self, name: str, values: dict[str, Any]) -> None:
        self.sections[name] = values
