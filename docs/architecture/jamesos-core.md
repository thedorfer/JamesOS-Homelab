# JamesOS Core Architecture

JamesOS Core is the software layer that manages the homelab platform.

The command line interface is the first client of the core, but it is not the core itself.

```text
CLI
  ↓
JamesOS Core
  ↓
Registry
  ↓
Providers
  ↓
Linux / Docker / Cloudflare / Services
```

## Layers

### Interfaces

Interfaces are ways humans or applications interact with JamesOS.

Current interface:

- CLI: `jamesos`

Future interfaces:

- REST API
- Homepage dashboard integration
- AI assistant tool calls
- scheduled health reports

### Core

The core owns:

- configuration
- provider registration
- shared data models
- high-level operations such as doctor and inventory

### Providers

Providers are adapters to external systems.

Initial providers:

- Linux provider
- Docker provider

Planned providers:

- WordPress
- Nextcloud
- Cloudflare
- SMART/storage
- backup system
- Open WebUI

### Plugins

Plugins will define higher-level features built on providers.

Examples:

- WordPress hardening
- Nextcloud backup verification
- Cloudflare WAF audit
- daily health report
- Google TV provisioning

## Design Rule

Business logic belongs in Python modules.

Shell commands are allowed only behind provider boundaries.

This keeps JamesOS testable, reusable, and ready for future interfaces.
