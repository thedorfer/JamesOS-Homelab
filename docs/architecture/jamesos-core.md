# JamesOS Core Architecture

JamesOS Core is the Python software layer that manages the homelab platform.

The command line interface is the first client of the core, but it is not the core itself. Future clients should call the same core logic instead of duplicating operational checks.

```text
CLI / Dashboard / REST API / AI Tools
  |
  v
JamesOS Core
  |
  v
Provider Registry
  |
  v
Providers
  |
  +--> Linux host
  +--> Storage
  +--> Pi gateway
  +--> Docker
  +--> WordPress
  +--> Nextcloud
  +--> Open WebUI
  +--> Backups
```

## Interfaces

Interfaces are ways humans or applications interact with JamesOS.

Current interfaces:

- `jamesos` console command inside the Python virtual environment
- `jamesos-homelab` desktop wrapper command

Planned interfaces:

- private Homepage dashboard
- REST API
- scheduled health reports
- AI assistant tool calls

## Core

The core owns:

- configuration
- provider registration
- shared data models
- high-level operations such as `doctor` and `inventory`

Current high-level operations:

```bash
jamesos version
jamesos doctor
jamesos inventory
```

## Providers

Providers are adapters to external systems. They hide operating-system commands, Docker calls, HTTP checks, and SSH inspection behind structured Python objects.

Current providers:

| Provider | Purpose |
| --- | --- |
| `LinuxProvider` | Base host inventory and root filesystem health |
| `StorageProvider` | Filesystem usage, mount/accessibility checks, and thresholds |
| `GatewayProvider` | SSH-based Raspberry Pi gateway checks |
| `DockerProvider` | Docker daemon and running container inventory |
| `WordPressProvider` | Public site, sitemap, XML-RPC, hardening, and core integrity checks |
| `NextcloudProvider` | Nextcloud containers, `occ status`, maintenance mode, and local endpoint checks |
| `OpenWebUIProvider` | Local AI interface container and endpoint checks |
| `BackupsProvider` | Backup root, latest artifacts, age, timers, and service results |

## Plugins

Plugins will define higher-level features built on providers.

Possible plugins:

- daily health report
- backup restore test
- Cloudflare WAF audit
- WordPress recovery workflow
- Google TV provisioning
- AI-assisted operations summary

## Design Rules

- Business logic belongs in Python modules.
- Shell commands are allowed only behind provider boundaries.
- Providers should return structured data.
- Interfaces should format results, not perform system logic.
- Public documentation must avoid secrets and raw incident payloads.

This keeps JamesOS testable, reusable, and ready for future interfaces.
