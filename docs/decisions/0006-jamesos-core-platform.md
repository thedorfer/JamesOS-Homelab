# ADR-0006
# JamesOS is a Core Platform, Not a Script Collection

Status: Accepted

Date: 2026-09-10

## Context

JamesOS-Homelab began as infrastructure documentation and shell scripts for a self-hosted homelab.

That approach would not scale well. A growing collection of scripts would make it harder to share logic between the command line, dashboards, future APIs, and AI assistants.

JamesOS may eventually grow beyond a normal homelab into a curated operating environment or appliance. The project should not depend on one specific Linux distribution or on manual shell scripts as its primary architecture.

## Decision

JamesOS-Homelab will be implemented around **JamesOS Core**, a Python application layer.

The repository will provide:

- a Python package named `jamesos`
- a command line interface named `jamesos`
- provider modules for Linux, Docker, Cloudflare, WordPress, Nextcloud, backups, storage, and future services
- shared data models for health, inventory, backup, and recovery results
- future interfaces such as a REST API, Homepage integration, and AI tool bindings

Shell scripts may exist as thin wrappers only. Business logic belongs in Python.

## Consequences

The CLI becomes the first interface, not the platform itself.

Future interfaces can reuse the same core logic:

- CLI
- Homepage dashboard
- REST API
- AI assistant tools
- scheduled health reports

Linux is the first supported host operating system, but the core should remain portable where practical.

If JamesOS later becomes a custom Linux distribution or appliance image, the distribution should package JamesOS Core rather than replace it.
