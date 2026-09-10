"""Linux host provider."""

from __future__ import annotations

import platform
import shutil
from pathlib import Path

from jamesos.core.models import CheckResult
from jamesos.core.shell import run


class LinuxProvider:
    name = "linux"

    def health(self) -> CheckResult:
        root = shutil.disk_usage("/")
        used_percent = round((root.used / root.total) * 100, 1)
        status = "ok" if used_percent < 85 else "warn"
        return CheckResult(
            name="Linux host",
            status=status,
            message=f"Root filesystem is {used_percent}% used.",
            details={
                "system": platform.system(),
                "release": platform.release(),
                "root_used_percent": used_percent,
            },
        )

    def inventory(self) -> dict[str, object]:
        os_release = self._os_release()
        hostname = run(["hostname"]).stdout
        uptime = run(["uptime", "-p"]).stdout
        lsblk = run(["lsblk", "-o", "NAME,MODEL,SIZE,FSTYPE,MOUNTPOINTS"]).stdout
        memory = run(["free", "-h"]).stdout

        return {
            "hostname": hostname,
            "platform": platform.platform(),
            "python": platform.python_version(),
            "os": os_release.get("PRETTY_NAME", "unknown"),
            "uptime": uptime,
            "memory": memory,
            "block_devices": lsblk,
        }

    def _os_release(self) -> dict[str, str]:
        path = Path("/etc/os-release")
        if not path.exists():
            return {}
        values: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key] = value.strip().strip('"')
        return values
