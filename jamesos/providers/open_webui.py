"""Open WebUI provider.

This provider monitors the local AI interface that anchors the JamesOS AI
workspace.  It keeps Open WebUI checks behind the provider boundary so the CLI,
future dashboard, REST API, and AI automation can consume structured status.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from jamesos.core.models import CheckResult
from jamesos.core.shell import run


class OpenWebUIProvider:
    """Inspect and health-check the Open WebUI service."""

    name = "open-webui"

    def __init__(
        self,
        container: str | None = None,
        local_url: str | None = None,
    ) -> None:
        self.container = container or os.getenv("JAMESOS_OPENWEBUI_CONTAINER", "open-webui")
        self.local_url = (
            local_url or os.getenv("JAMESOS_OPENWEBUI_URL", "http://127.0.0.1:3000")
        ).rstrip("/")

    def health(self) -> CheckResult:
        container_state = self._container_state()
        endpoint_status = self._http_status(self.local_url)

        details: dict[str, Any] = {
            "container": self.container,
            "local_url": self.local_url,
            "container_state": container_state,
            "local_http_status": endpoint_status,
        }

        if container_state.get("error"):
            return CheckResult(
                name="Open WebUI",
                status="fail",
                message="Open WebUI container state could not be read.",
                details=details,
            )

        if not container_state.get("running"):
            return CheckResult(
                name="Open WebUI",
                status="fail",
                message="Open WebUI container is not running.",
                details=details,
            )

        health = str(container_state.get("health", "none"))
        if health == "unhealthy":
            return CheckResult(
                name="Open WebUI",
                status="fail",
                message="Open WebUI container reports unhealthy.",
                details=details,
            )

        if endpoint_status not in {200, 302, 401, 403}:
            return CheckResult(
                name="Open WebUI",
                status="warn",
                message="Open WebUI container is running, but the local endpoint check did not return an expected status.",
                details=details,
            )

        return CheckResult(
            name="Open WebUI",
            status="ok",
            message="Open WebUI container and local endpoint checks passed.",
            details=details,
        )

    def inventory(self) -> dict[str, object]:
        return {
            "container": self.container,
            "local_url": self.local_url,
            "container_state": self._container_state(),
            "local_http_status": self._http_status(self.local_url),
        }

    def _container_state(self) -> dict[str, object]:
        command = (
            "docker inspect "
            "--format '{{json .State}}' "
            f"{self.container}"
        )
        result = run(["sh", "-lc", command], timeout=20)
        if not result.ok:
            return {
                "error": "docker_inspect_failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        try:
            state = json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": "invalid_json", "stdout": result.stdout}

        health = "none"
        if isinstance(state.get("Health"), dict):
            health = str(state["Health"].get("Status", "unknown"))

        return {
            "running": bool(state.get("Running")),
            "status": state.get("Status"),
            "health": health,
            "started_at": state.get("StartedAt"),
        }

    def _http_status(self, url: str) -> int:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "JamesOS/0.2 OpenWebUIProvider"},
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return int(response.status)
        except urllib.error.HTTPError as exc:
            return int(exc.code)
        except Exception:
            return 0
