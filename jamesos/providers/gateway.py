"""Pi gateway provider.

The gateway provider inspects the Raspberry Pi gateway over SSH.  The Pi is
expected to host gateway/control-plane services such as Cloudflare Tunnel and
the JamesOS home dashboard while the desktop hosts heavier application and
storage workloads.
"""

from __future__ import annotations

import os
import re
import shlex
from typing import Any

from jamesos.core.models import CheckResult
from jamesos.core.shell import run


class GatewayProvider:
    """Inspect the Raspberry Pi gateway host."""

    name = "gateway"

    def __init__(
        self,
        host: str | None = None,
        user: str | None = None,
        services: list[str] | None = None,
    ) -> None:
        self.host = host or os.getenv("JAMESOS_GATEWAY_HOST", "pi-gateway")
        self.user = user or os.getenv("JAMESOS_GATEWAY_USER", os.getenv("USER", "james"))
        configured_services = os.getenv("JAMESOS_GATEWAY_SERVICES", "cloudflared,james-home")
        self.services = services or [
            service.strip()
            for service in configured_services.split(",")
            if service.strip()
        ]

    @property
    def target(self) -> str:
        if self.user:
            return f"{self.user}@{self.host}"
        return self.host

    def health(self) -> CheckResult:
        inventory = self.inventory()

        if not inventory.get("ssh_ok"):
            return CheckResult(
                name="Pi gateway",
                status="warn",
                message="Pi gateway could not be inspected over SSH.",
                details=inventory,
            )

        services = inventory.get("services", {})
        inactive = [
            service
            for service, state in services.items()
            if state != "active"
        ]
        failed_units = inventory.get("failed_units", [])

        if inactive:
            return CheckResult(
                name="Pi gateway",
                status="fail",
                message="gateway service(s) are not active: " + ", ".join(inactive),
                details=inventory,
            )

        if failed_units:
            return CheckResult(
                name="Pi gateway",
                status="warn",
                message=f"gateway has {len(failed_units)} failed systemd unit(s).",
                details=inventory,
            )

        return CheckResult(
            name="Pi gateway",
            status="ok",
            message="Gateway SSH, Cloudflare Tunnel, and dashboard checks passed.",
            details=inventory,
        )

    def inventory(self) -> dict[str, Any]:
        result = self._remote_inventory()
        result.update(
            {
                "host": self.host,
                "user": self.user,
                "target": self.target,
                "configured_services": self.services,
            }
        )
        return result

    def _remote_inventory(self) -> dict[str, Any]:
        services = [service for service in self.services if self._safe_service_name(service)]
        quoted_services = " ".join(shlex.quote(service) for service in services)

        command = f'''
set -u

echo __JAMESOS_HOSTNAME__
hostname 2>/dev/null || true

echo __JAMESOS_UPTIME__
uptime -p 2>/dev/null || uptime 2>/dev/null || true

echo __JAMESOS_SERVICES__
for svc in {quoted_services}; do
    state=$(systemctl is-active "$svc" 2>/dev/null || true)
    if [ -z "$state" ]; then
        state=unknown
    fi
    printf '%s=%s\n' "$svc" "$state"
done

echo __JAMESOS_FAILED_UNITS__
systemctl --failed --no-legend --plain 2>/dev/null || true
'''

        result = run(
            [
                "ssh",
                "-o",
                "BatchMode=yes",
                "-o",
                "ConnectTimeout=5",
                self.target,
                "sh",
                "-lc",
                command,
            ],
            timeout=20,
        )

        if not result.ok:
            return {
                "ssh_ok": False,
                "error": "ssh_failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "hostname": None,
                "uptime": None,
                "services": {},
                "failed_units": [],
            }

        parsed = self._parse_remote_output(result.stdout)
        parsed["ssh_ok"] = True
        parsed["error"] = None
        return parsed

    def _parse_remote_output(self, output: str) -> dict[str, Any]:
        sections: dict[str, list[str]] = {}
        current: str | None = None

        marker_map = {
            "__JAMESOS_HOSTNAME__": "hostname",
            "__JAMESOS_UPTIME__": "uptime",
            "__JAMESOS_SERVICES__": "services",
            "__JAMESOS_FAILED_UNITS__": "failed_units",
        }

        for raw_line in output.splitlines():
            line = raw_line.rstrip("\n")
            if line in marker_map:
                current = marker_map[line]
                sections.setdefault(current, [])
                continue
            if current is not None:
                sections.setdefault(current, []).append(line)

        services: dict[str, str] = {}
        for line in sections.get("services", []):
            if "=" not in line:
                continue
            service, state = line.split("=", 1)
            services[service.strip()] = state.strip()

        failed_units = [
            line.strip()
            for line in sections.get("failed_units", [])
            if line.strip()
        ]

        return {
            "hostname": self._first_value(sections.get("hostname", [])),
            "uptime": self._first_value(sections.get("uptime", [])),
            "services": services,
            "failed_units": failed_units,
        }

    def _first_value(self, values: list[str]) -> str | None:
        for value in values:
            value = value.strip()
            if value:
                return value
        return None

    def _safe_service_name(self, value: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z0-9@_.:-]+", value))
