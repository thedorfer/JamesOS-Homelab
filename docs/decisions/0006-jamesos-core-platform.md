# ADR-0006
# JamesOS is a Core Platform, Not a Script Collection

Status: Accepted

Date: 2026-09-10

## Context

JamesOS-Homelab began as infrastructure documentation and operational scripts for a self-hosted homelab.

That approach would not scale well. A growing collection of scripts would make it harder to share logic between the command line, dashboards, future APIs, and AI assistants.

JamesOS may eventually grow beyond a normal homelab into a curated operating environment or appliance. The project should not depend on one specific Linux distribution or on manual shell scripts as its primary architecture.

## Decision

JamesOS-Homelab will be implemented around **JamesOS Core**, a Python application layer.

The repository provides:

- a Python package named `jamesos-homelab`
- a Python import package named `jamesos`
- a console command named `jamesos` inside the project virtual environment
- a desktop wrapper command named `jamesos-homelab` to avoid conflicts with the separate `thedorfer/JamesOS` application project
- provider modules for platform and service integrations
- shared data models for health and inventory results
- future extension points for a dashboard, REST API, AI tool bindings, and scheduled reports

Shell scripts may exist as thin wrappers only. Business logic belongs in Python.

## Current Provider Baseline

As of version 0.2.9, JamesOS Core includes providers for:

- Linux host
- Storage
- Raspberry Pi gateway
- Docker
- WordPress
- Nextcloud
- Open WebUI
- Backups

The expected healthy command is:

```bash
jamesos-homelab doctor
```

with an expected `Overall: OK` result.

## Consequences

The CLI becomes the first interface, not the platform itself.

Future interfaces can reuse the same core logic:

- CLI
- private dashboard
- REST API
- AI assistant tools
- scheduled health reports

Linux is the first supported host operating system, but the core should remain portable where practical.

If JamesOS later becomes a custom Linux distribution or appliance image, the distribution should package JamesOS Core rather than replace it.
