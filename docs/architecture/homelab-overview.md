# JamesOS Homelab Architecture

## Purpose

JamesOS Homelab provides the infrastructure powering the JamesOS platform.

The current design separates the platform into three layers:

1. public edge and gateway
2. desktop application and storage server
3. Python-based JamesOS Core for health, inventory, and future automation

## Current Architecture

```text
Internet
  |
  v
Cloudflare DNS / WAF / Tunnel
  |
  v
Raspberry Pi 5 Gateway
  |  - cloudflared
  |  - james-home dashboard service
  |  - future reverse-proxy/control-plane services
  |
  v
Local Network
  |
  v
Desktop Application Server
  |  - Linux Mint host
  |  - Docker
  |  - 1 TB NVMe system disk
  |  - 13 TB storage disk
  |
  +--> WordPress public portfolio
  +--> Nextcloud private cloud
  +--> Open WebUI local AI interface
  +--> backup jobs and storage
  +--> JamesOS-Homelab CLI
```

## Current Health Baseline

The baseline command is:

```bash
jamesos-homelab doctor
```

Expected healthy result:

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

## Physical Roles

### Raspberry Pi Gateway

The Raspberry Pi is treated as a lightweight gateway appliance.

Current responsibilities:

- Cloudflare Tunnel endpoint
- gateway dashboard service
- remote health inspection over SSH

Future responsibilities may include:

- reverse proxy
- lightweight control-plane services
- gateway-level monitoring

### Desktop Server

The desktop is the primary application and storage server.

Current responsibilities:

- Docker host
- WordPress runtime
- Nextcloud runtime
- Open WebUI runtime
- persistent storage
- scheduled backups
- JamesOS-Homelab CLI and operational checks

## Design Principles

- Infrastructure as Code
- Security by default
- Rebuild over repair
- Documentation first
- Automation over manual administration
- Python business logic over shell-script sprawl
- Keep the gateway as stateless as practical
- Keep persistent application data on the desktop server

## Current Service Inventory

| Service | Host | Purpose | Monitored By |
| --- | --- | --- | --- |
| WordPress | Desktop Docker | Public portfolio site | `WordPressProvider` |
| Nextcloud | Desktop Docker | Private cloud | `NextcloudProvider` |
| Open WebUI | Desktop Docker | Local AI interface | `OpenWebUIProvider` |
| Backups | Desktop systemd/storage | Service and gateway backups | `BackupsProvider` |
| Storage | Desktop filesystems | System and data disks | `StorageProvider` |
| Gateway | Raspberry Pi | Tunnel and dashboard | `GatewayProvider` |
| Docker | Desktop | Container runtime | `DockerProvider` |
| Linux host | Desktop | Base operating system | `LinuxProvider` |

## Recovery Direction

The long-term recovery goal is:

1. rebuild or replace hardware
2. clone this repository
3. restore secrets from a secure source outside Git
4. restore persistent data from backups
5. run `jamesos-homelab doctor`
6. verify the platform returns `Overall: OK`
