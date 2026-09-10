"""Docker provider."""

from __future__ import annotations

from jamesos.core.models import CheckResult
from jamesos.core.shell import run


class DockerProvider:
    name = "docker"

    def health(self) -> CheckResult:
        version = run(["docker", "version", "--format", "{{.Server.Version}}"])
        if not version.ok:
            return CheckResult(
                name="Docker",
                status="fail",
                message="Docker is not reachable.",
                details={"stderr": version.stderr, "stdout": version.stdout},
            )

        ps = run(["docker", "ps", "--format", "{{.Names}}"])
        if not ps.ok:
            return CheckResult(
                name="Docker",
                status="warn",
                message="Docker engine is reachable, but containers could not be listed.",
                details={"version": version.stdout, "stderr": ps.stderr},
            )

        containers = [line for line in ps.stdout.splitlines() if line.strip()]
        return CheckResult(
            name="Docker",
            status="ok",
            message=f"Docker is reachable with {len(containers)} running container(s).",
            details={"version": version.stdout, "running_containers": len(containers)},
        )

    def inventory(self) -> dict[str, object]:
        version = run(["docker", "version", "--format", "{{.Server.Version}}"])
        ps = run(
            [
                "docker",
                "ps",
                "--format",
                "{{.Names}}|{{.Image}}|{{.Status}}|{{.Ports}}",
            ]
        )

        containers: list[dict[str, object]] = []
        if ps.ok:
            for line in ps.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|", 3)
                while len(parts) < 4:
                    parts.append("")
                name, image, status, ports = parts
                containers.append(
                    {
                        "name": name,
                        "image": image,
                        "status": status,
                        "ports": ports,
                    }
                )

        return {
            "server_version": version.stdout if version.ok else None,
            "container_count": len(containers),
            "containers": containers,
        }
