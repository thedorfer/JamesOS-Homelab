# ADR-0001
# Desktop is the Primary Application Server

Status: Accepted

Date: 2026-09-10

## Context

The JamesOS Homelab consists of a Raspberry Pi 5 and a high-performance desktop.

The desktop provides:

- 13 TB of storage
- 1 TB NVMe SSD
- 64 GB RAM
- Multi-core CPU
- Docker host

The Raspberry Pi provides:

- Low power consumption
- Always-on operation
- Cloudflare Tunnel endpoint
- Gateway services

## Decision

The desktop is the primary application server.

The Raspberry Pi is the gateway appliance.

## Consequences

Applications run on the desktop.

Persistent storage lives on the desktop.

The Pi should remain as stateless as practical.

If the Pi fails, replacing it should require minimal configuration.

If the desktop fails, backups should allow complete recovery.

