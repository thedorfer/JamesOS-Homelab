# JamesOS Vision

JamesOS is a personal operating environment for infrastructure, automation, AI, documentation, monitoring, and private cloud services.

The repository is named **JamesOS-Homelab** because it documents and implements the homelab infrastructure. The running platform is simply **JamesOS**.

## What JamesOS Is

JamesOS is not just a server and it is not just a CLI.

It is a platform made of:

- Linux host infrastructure
- Docker services
- Cloudflare edge access
- Raspberry Pi gateway services
- personal cloud storage
- public portfolio hosting
- local AI tooling
- backups and recovery
- health checks and automation
- documentation that explains why the system works the way it does

## Current Direction

The first interface is a Python CLI:

```bash
jamesos-homelab doctor
```

That command now checks the real environment: Linux, storage, Pi gateway, Docker, WordPress, Nextcloud, Open WebUI, and backups.

Future interfaces should call the same JamesOS Core logic instead of reimplementing operational checks.

Potential future interfaces:

- private dashboard
- REST API
- daily health reports
- AI assistant tools
- mobile or TV interfaces

## Long-Term Goal

If every piece of hardware disappeared tomorrow, the platform should be recoverable from Git, backups, and documented operational procedures.

The desired end state is not a perfect homelab. The desired end state is a reproducible personal infrastructure platform that is understandable, testable, secure, and recoverable.

## Guiding Rules

- Git is the source of truth.
- Rebuild over repair.
- Automate repeated work.
- Keep secrets out of the repository.
- Prefer Python business logic over shell-script sprawl.
- Treat incidents as documentation and automation opportunities.
- Keep the Raspberry Pi gateway lightweight.
- Keep persistent application data on the desktop storage server.
