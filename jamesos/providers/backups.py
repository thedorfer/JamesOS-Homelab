"""Backup provider for JamesOS.

This provider verifies that the core JamesOS backup jobs are configured and
that recent backup artifacts exist on the desktop storage volume.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jamesos.core.models import CheckResult
from jamesos.core.shell import run


class BackupsProvider:
    """Inspect JamesOS backup jobs and latest backup artifacts."""

    name = "backups"

    def __init__(self, backup_root: str | None = None) -> None:
        self.backup_root = Path(
            backup_root
            or os.getenv("JAMESOS_BACKUP_ROOT", "/mnt/storage/Storage/backups")
        )
        self.max_age_hours = float(os.getenv("JAMESOS_BACKUP_MAX_AGE_HOURS", "48"))
        self.backup_sets = {
            "wordpress": {
                "latest": self.backup_root / "wordpress" / "latest",
                "timer": "wordpress-backup.timer",
                "service": "wordpress-backup.service",
            },
            "nextcloud": {
                "latest": self.backup_root / "nextcloud" / "latest",
                "timer": "nextcloud-backup.timer",
                "service": "nextcloud-backup.service",
            },
            "pi-gateway": {
                "latest": self.backup_root / "pi-gateway" / "latest",
                "timer": "pi-gateway-backup.timer",
                "service": "pi-gateway-backup.service",
            },
        }

    def health(self) -> CheckResult:
        inventory = self.inventory()

        failures: list[str] = []
        warnings: list[str] = []

        if not inventory["backup_root_exists"]:
            failures.append(f"backup root is missing: {self.backup_root}")

        for name, values in inventory["backup_sets"].items():
            latest = values["latest"]
            timer = values["timer"]
            service = values["service"]

            if not latest["exists"]:
                failures.append(f"{name} latest backup is missing")
            elif latest.get("age_hours") is not None and latest["age_hours"] > self.max_age_hours:
                warnings.append(
                    f"{name} latest backup is {latest['age_hours']:.1f} hours old"
                )

            if timer.get("active") not in {"active", "inactive"}:
                warnings.append(f"{name} timer state could not be determined")
            elif timer.get("active") != "active":
                warnings.append(f"{name} timer is not active")

            if service.get("result") not in {"success", "", None}:
                warnings.append(
                    f"{name} backup service last result is {service.get('result')}"
                )

        if failures:
            return CheckResult(
                name="Backups",
                status="fail",
                message="; ".join(failures),
                details=inventory,
            )

        if warnings:
            return CheckResult(
                name="Backups",
                status="warn",
                message="; ".join(warnings),
                details=inventory,
            )

        return CheckResult(
            name="Backups",
            status="ok",
            message="Backup timers and latest backup artifacts look healthy.",
            details=inventory,
        )

    def inventory(self) -> dict[str, Any]:
        return {
            "backup_root": str(self.backup_root),
            "backup_root_exists": self.backup_root.exists(),
            "max_age_hours": self.max_age_hours,
            "backup_sets": {
                name: {
                    "latest": self._latest_info(values["latest"]),
                    "timer": self._systemd_info(values["timer"]),
                    "service": self._systemd_info(values["service"]),
                }
                for name, values in self.backup_sets.items()
            },
        }

    def _latest_info(self, path: Path) -> dict[str, Any]:
        exists = path.exists()
        info: dict[str, Any] = {
            "path": str(path),
            "exists": exists,
            "is_symlink": path.is_symlink(),
            "target": None,
            "age_hours": None,
            "modified_at": None,
        }

        if not exists:
            return info

        try:
            target = Path(os.path.realpath(path))
            stat = target.stat()
            modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
            age = datetime.now(timezone.utc) - modified
            info.update(
                {
                    "target": str(target),
                    "modified_at": modified.isoformat(),
                    "age_hours": round(age.total_seconds() / 3600, 2),
                }
            )
        except OSError as exc:
            info["error"] = str(exc)

        return info

    def _systemd_info(self, unit: str) -> dict[str, Any]:
        result = run(
            [
                "systemctl",
                "show",
                unit,
                "--no-pager",
                "-p",
                "LoadState",
                "-p",
                "ActiveState",
                "-p",
                "SubState",
                "-p",
                "UnitFileState",
                "-p",
                "Result",
                "-p",
                "LastTriggerUSec",
                "-p",
                "NextElapseUSecRealtime",
            ],
            timeout=10,
        )

        info: dict[str, Any] = {"unit": unit}
        if not result.ok:
            info.update(
                {
                    "error": "systemctl_failed",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            )
            return info

        for line in result.stdout.splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            normalized = key.removesuffix("State").lower()
            if key == "ActiveState":
                normalized = "active"
            elif key == "LoadState":
                normalized = "load"
            elif key == "UnitFileState":
                normalized = "unit_file"
            elif key == "SubState":
                normalized = "sub"
            elif key == "LastTriggerUSec":
                normalized = "last_trigger"
            elif key == "NextElapseUSecRealtime":
                normalized = "next_elapse"
            info[normalized] = value

        return info
