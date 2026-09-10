"""Nextcloud provider.

This provider checks the Nextcloud application stack that backs the private
personal cloud portion of JamesOS. It inspects Docker container state, runs the
Nextcloud `occ status` command, and verifies the local HTTP endpoint.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from jamesos.core.models import CheckResult
from jamesos.core.shell import run


class NextcloudProvider:
    """Inspect and health-check the Nextcloud service."""

    name = "nextcloud"

    def __init__(
        self,
        app_container: str | None = None,
        cron_container: str | None = None,
        db_container: str | None = None,
        redis_container: str | None = None,
        local_url: str | None = None,
    ) -> None:
        self.app_container = app_container or os.getenv(
            "JAMESOS_NEXTCLOUD_APP_CONTAINER",
            "nextcloud-app-1",
        )
        self.cron_container = cron_container or os.getenv(
            "JAMESOS_NEXTCLOUD_CRON_CONTAINER",
            "nextcloud-cron-1",
        )
        self.db_container = db_container or os.getenv(
            "JAMESOS_NEXTCLOUD_DB_CONTAINER",
            "nextcloud-db-1",
        )
        self.redis_container = redis_container or os.getenv(
            "JAMESOS_NEXTCLOUD_REDIS_CONTAINER",
            "nextcloud-redis-1",
        )
        self.local_url = (
            local_url
            or os.getenv("JAMESOS_NEXTCLOUD_URL", "http://192.168.5.105:8081")
        ).rstrip("/")

    def health(self) -> CheckResult:
        containers = self._container_states()
        occ_status = self._occ_status()
        http_status = self._http_status(self.local_url)

        details: dict[str, Any] = {
            "containers": containers,
            "occ_status": occ_status,
            "local_url": self.local_url,
            "local_http_status": http_status,
        }

        failures: list[str] = []
        warnings: list[str] = []

        for role in ("app", "db", "redis"):
            state = containers.get(role, {})
            if not state.get("running"):
                failures.append(f"Nextcloud {role} container is not running")

        cron_state = containers.get("cron", {})
        if not cron_state.get("running"):
            warnings.append("Nextcloud cron container is not running")

        for role, state in containers.items():
            health = state.get("health")
            if health and health not in {"healthy", "none"}:
                warnings.append(f"Nextcloud {role} container health is {health}")

        if occ_status.get("error"):
            failures.append("Nextcloud occ status could not be read")
        else:
            if occ_status.get("installed") is not True:
                failures.append("Nextcloud is not reporting as installed")
            if occ_status.get("maintenance") is True:
                warnings.append("Nextcloud maintenance mode is enabled")
            if occ_status.get("needsDbUpgrade") is True:
                warnings.append("Nextcloud reports that a database upgrade is needed")

        if http_status not in {200, 301, 302, 303}:
            warnings.append(f"Nextcloud local HTTP endpoint returned {http_status}")

        if failures:
            return CheckResult(
                name="Nextcloud",
                status="fail",
                message="; ".join(failures),
                details=details,
            )

        if warnings:
            return CheckResult(
                name="Nextcloud",
                status="warn",
                message="; ".join(warnings),
                details=details,
            )

        return CheckResult(
            name="Nextcloud",
            status="ok",
            message="Nextcloud containers, occ status, and local endpoint checks passed.",
            details=details,
        )

    def inventory(self) -> dict[str, object]:
        return {
            "containers": self._container_states(),
            "occ_status": self._occ_status(),
            "local_url": self.local_url,
            "local_http_status": self._http_status(self.local_url),
        }

    def _container_states(self) -> dict[str, dict[str, object]]:
        return {
            "app": self._container_state(self.app_container),
            "cron": self._container_state(self.cron_container),
            "db": self._container_state(self.db_container),
            "redis": self._container_state(self.redis_container),
        }

    def _container_state(self, container: str) -> dict[str, object]:
        result = run(["docker", "inspect", "--format", "{{json .State}}", container], timeout=20)
        if not result.ok:
            return {
                "container": container,
                "running": False,
                "error": result.stderr or result.stdout,
            }

        try:
            state = json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "container": container,
                "running": False,
                "error": "invalid docker inspect json",
                "raw": result.stdout,
            }

        health = "none"
        if isinstance(state.get("Health"), dict):
            health = str(state["Health"].get("Status", "unknown"))

        return {
            "container": container,
            "running": bool(state.get("Running")),
            "status": state.get("Status"),
            "health": health,
            "started_at": state.get("StartedAt"),
        }

    def _occ_status(self) -> dict[str, object]:
        result = run(
            [
                "docker",
                "exec",
                "-u",
                "www-data",
                self.app_container,
                "php",
                "occ",
                "status",
                "--output=json",
            ],
            timeout=30,
        )
        if not result.ok:
            return {
                "error": "occ_status_failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "error": "invalid_occ_json",
                "stdout": result.stdout,
            }

        return data

    def _http_status(self, url: str) -> int:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "JamesOS/0.2 NextcloudProvider"},
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return int(response.status)
        except urllib.error.HTTPError as exc:
            return int(exc.code)
        except Exception:
            return 0
