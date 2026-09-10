# JamesOS Homelab

JamesOS Homelab is the infrastructure and operations platform for JamesOS.

It is not just a folder of shell scripts.  It is being built as a Python-powered core platform with a CLI first, and future interfaces for dashboards, APIs, and AI automation.

## Current State

- Public portfolio site: WordPress
- Private cloud: Nextcloud
- Local AI interface: Open WebUI
- Public edge: Cloudflare DNS, Tunnel, and WAF rules
- Gateway appliance: Raspberry Pi 5
- Application server: Linux desktop with Docker and 13 TB storage

## JamesOS Core

The package name is `jamesos` and the command is `jamesos`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]

jamesos version
jamesos doctor
jamesos inventory
```

The CLI is only the first interface.  The core is designed so future clients can use the same logic:

- CLI
- Homepage dashboard
- REST API
- AI assistant tools
- scheduled health reports

## Design Principles

- Infrastructure as Code
- Security by default
- Rebuild over repair
- Documentation first
- Python business logic over shell script sprawl
- Providers isolate operating-system and service integrations
- Git is the source of truth

## Repository Structure

```text
jamesos/              Python core platform and CLI
docs/                 Architecture, security, recovery, and decisions
cloudflare/           DNS, Tunnel, WAF, and Zero Trust documentation
docker/               Docker compose stacks and service deployment notes
scripts/              Transitional scripts and operational utilities
services/             Service-specific runbooks
inventory/            Generated/local infrastructure inventory
assets/               Diagrams and screenshots
tests/                Python tests
```

## Current Commands

```bash
jamesos version
jamesos doctor
jamesos inventory
```

## Relationship to JamesOS

`thedorfer/JamesOS` is the application and AI platform.

`thedorfer/JamesOS-Homelab` is the infrastructure, operations, and eventual operating environment that runs it.
