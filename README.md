# JamesOS Homelab

JamesOS Homelab is the infrastructure and operations platform for JamesOS.

This repository documents and implements the personal cloud platform that runs the public portfolio site, private cloud services, AI tools, gateway services, backups, and operational health checks.

The project is intentionally moving away from one-off shell scripts and toward a Python-powered core platform. The CLI is the first interface; future interfaces can include a private dashboard, REST API, scheduled health reports, and AI assistant tools.

## Current Operational Baseline

Current version: **0.2.9**

Current daily health command:

```bash
jamesos-homelab doctor
```

Current provider stack:

- Linux host
- Storage
- Raspberry Pi gateway
- Docker
- WordPress
- Nextcloud
- Open WebUI
- Backups

Expected healthy baseline:

```text
✓ Linux host
✓ Storage
✓ Pi gateway
✓ Docker
✓ WordPress
✓ Nextcloud
✓ Open WebUI
✓ Backups

Overall: OK
```

## Current Services

| Service | Role | Status |
| --- | --- | --- |
| WordPress | Public portfolio website | Hardened and monitored |
| Nextcloud | Private cloud storage | Monitored |
| Open WebUI | Local AI interface | Monitored |
| Cloudflare Tunnel | Public edge / remote access | Monitored through Pi gateway checks |
| Raspberry Pi Gateway | Lightweight gateway appliance | Monitored |
| Desktop Server | Primary application and storage server | Monitored |
| Backups | WordPress, Nextcloud, and Pi gateway backups | Monitored |

## Install for Local Development

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Inside the virtual environment:

```bash
jamesos version
jamesos doctor
jamesos inventory
pytest
```

On the desktop host, use the wrapper command to avoid conflicts with the separate `thedorfer/JamesOS` application CLI:

```bash
jamesos-homelab version
jamesos-homelab doctor
jamesos-homelab inventory
```

## Environment Defaults

Common local overrides:

```bash
export JAMESOS_GATEWAY_HOST=pi-gateway.local
export JAMESOS_GATEWAY_USER=james
```

Other providers also support environment-variable overrides. See the service documents under `docs/services/`.

## Repository Structure

```text
jamesos/              Python core platform, providers, and CLI
docs/                 Architecture, security, recovery, service, and decision docs
cloudflare/           DNS, Tunnel, WAF, and Zero Trust documentation
docker/               Docker compose stacks and service deployment notes
scripts/              Transitional scripts and operational utilities
services/             Service-specific implementation artifacts
assets/               Diagrams and screenshots
tests/                Python tests
```

## Design Principles

- Infrastructure as Code
- Security by default
- Rebuild over repair
- Documentation first
- Python business logic over shell-script sprawl
- Providers isolate operating-system and service integrations
- Git is the source of truth
- No secrets in Git

## Relationship to JamesOS

`thedorfer/JamesOS` is the application and AI platform.

`thedorfer/JamesOS-Homelab` is the infrastructure, operations, and future operating environment that runs and protects it.
