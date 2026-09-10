# JamesOS Homelab Architecture

## Purpose

JamesOS Homelab provides the infrastructure powering JamesOS.

The guiding philosophy is:

- Infrastructure as Code
- Security by Default
- Rebuild over Repair
- Documentation First
- Automation over Manual Administration

---

## Physical Infrastructure

Internet
    │
Cloudflare DNS
    │
Cloudflare Tunnel
    │
────────────────────────────
Raspberry Pi 5
Gateway Appliance
────────────────────────────
    │
Local Network
    │
Desktop Server
────────────────────────────
Docker
────────────────────────────

Persistent Storage

- 13 TB HDD
- 1 TB NVMe
- Automated Backups

---

## Current Services

WordPress
Public Portfolio

Nextcloud
Private Cloud

Open WebUI
Local AI

Cloudflare Tunnel
Remote Access

---

## Current Principles

The Raspberry Pi is a gateway appliance.

The Desktop is the application server.

Persistent data lives on the Desktop.

Infrastructure is documented in Git.

Every service must be recoverable.

