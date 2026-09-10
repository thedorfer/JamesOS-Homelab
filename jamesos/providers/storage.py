"""Storage provider for JamesOS.

This provider verifies that the primary filesystems used by JamesOS are mounted
and have enough free space for normal operation.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from jamesos.core.models import CheckResult


class StorageProvider:
    """Inspect filesystem capacity for JamesOS storage paths."""

    name = "storage"

    def __init__(self, paths: list[str] | None = None) -> None:
        configured = paths or [
            p.strip()
            for p in os.getenv("JAMESOS_STORAGE_PATHS", "/,/mnt/storage").split(",")
            if p.strip()
        ]
        self.paths = [Path(p) for p in configured]
        self.warn_percent = float(os.getenv("JAMESOS_STORAGE_WARN_PERCENT", "85"))
        self.fail_percent = float(os.getenv("JAMESOS_STORAGE_FAIL_PERCENT", "95"))

    def health(self) -> CheckResult:
        inventory = self.inventory()
        failures: list[str] = []
        warnings: list[str] = []

        for path, info in inventory["paths"].items():
            if not info.get("exists"):
                failures.append(f"{path} is missing")
                continue
            if not info.get("accessible"):
                failures.append(f"{path} is not accessible: {info.get('error')}")
                continue

            used_percent = info.get("used_percent")
            if used_percent is None:
                warnings.append(f"{path} usage could not be determined")
            elif used_percent >= self.fail_percent:
                failures.append(f"{path} is {used_percent:.1f}% used")
            elif used_percent >= self.warn_percent:
                warnings.append(f"{path} is {used_percent:.1f}% used")

        if failures:
            return CheckResult(
                name="Storage",
                status="fail",
                message="; ".join(failures),
                details=inventory,
            )

        if warnings:
            return CheckResult(
                name="Storage",
                status="warn",
                message="; ".join(warnings),
                details=inventory,
            )

        return CheckResult(
            name="Storage",
            status="ok",
            message="Configured storage paths are mounted and have sufficient free space.",
            details=inventory,
        )

    def inventory(self) -> dict[str, Any]:
        return {
            "warn_percent": self.warn_percent,
            "fail_percent": self.fail_percent,
            "paths": {str(path): self._path_info(path) for path in self.paths},
        }

    def _path_info(self, path: Path) -> dict[str, Any]:
        info: dict[str, Any] = {
            "exists": None,
            "accessible": None,
            "error": None,
            "total_bytes": None,
            "used_bytes": None,
            "free_bytes": None,
            "used_percent": None,
        }

        try:
            info["exists"] = path.exists()
            if not info["exists"]:
                info["accessible"] = False
                return info

            usage = shutil.disk_usage(path)
            used_percent = round((usage.used / usage.total) * 100, 1)
            info.update(
                {
                    "accessible": True,
                    "total_bytes": usage.total,
                    "used_bytes": usage.used,
                    "free_bytes": usage.free,
                    "used_percent": used_percent,
                    "total_human": self._human(usage.total),
                    "used_human": self._human(usage.used),
                    "free_human": self._human(usage.free),
                }
            )
        except OSError as exc:
            info["accessible"] = False
            info["error"] = f"{type(exc).__name__}: {exc}"

        return info

    def _human(self, value: int) -> str:
        units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
        n = float(value)
        for unit in units:
            if n < 1024 or unit == units[-1]:
                return f"{n:.1f} {unit}"
            n /= 1024
        return f"{value} B"
