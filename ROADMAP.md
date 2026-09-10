# JamesOS Homelab Roadmap

This roadmap tracks the evolution of JamesOS Homelab from documented infrastructure into a Python-powered operations platform.

## v0.1.0 - Foundation

Status: Complete

- Repository created
- Initial documentation structure
- Architecture overview
- Security incident documentation
- Initial Architecture Decision Records
- Site audit and WordPress integrity scripts added

## v0.2.x - Core Operations Platform

Status: Complete through **0.2.9**

The v0.2 line established JamesOS Core, the installable CLI, and the first operational providers.

Implemented:

- Python package: `jamesos-homelab`
- Console command inside the virtual environment: `jamesos`
- Desktop wrapper command: `jamesos-homelab`
- Core application object
- Provider registry
- Shared health and inventory models
- CLI commands:
  - `jamesos version`
  - `jamesos doctor`
  - `jamesos inventory`
- Providers:
  - Linux host
  - Storage
  - Raspberry Pi gateway
  - Docker
  - WordPress
  - Nextcloud
  - Open WebUI
  - Backups
- Basic pytest coverage for versioning, provider registration, status rollups, and CLI execution

Current expected baseline:

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

## v0.3.0 - Private Dashboard

Status: Next

Goal: deploy a private dashboard for the running JamesOS environment.

Planned:

- Homepage dashboard service
- Private dashboard hostname
- Service cards for WordPress, Nextcloud, Open WebUI, backups, storage, Docker, and gateway
- Dashboard documentation
- Status output backed by `jamesos-homelab doctor`
- Links to runbooks and service docs

## v0.4.0 - Daily Health Reports

Status: Planned

Planned:

- Scheduled `jamesos-homelab doctor` run
- JSON report output
- Markdown report output
- Daily health report stored in Nextcloud or local storage
- Optional email or dashboard notification
- Backup age and service-state alerting

## v0.5.0 - Monitoring and Metrics

Status: Planned

Planned:

- SMART disk health provider
- Docker image/update provider
- Cloudflare Tunnel/public-edge provider
- Latency checks for public and local endpoints
- Grafana/Prometheus evaluation
- Historical storage and backup trends

## v0.6.0 - Reverse Proxy and Service Routing

Status: Planned

Planned:

- Evaluate Traefik or Caddy
- Standardize local routing
- Document service exposure patterns
- Separate public and private services clearly
- Add security middleware documentation

## v1.0.0 - Reproducible Platform

Status: Target

Goal: a documented, testable, recoverable JamesOS Homelab baseline.

Required:

- Documented install path
- Documented restore path
- Security baseline
- Backup baseline
- Service inventory
- Platform health command
- Dashboard baseline
- At least one tested restore procedure
- No known public documentation drift
