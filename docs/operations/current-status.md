# Current Operational Status

Last documented baseline: **2026-09-10**

Current JamesOS-Homelab version: **0.2.9**

## Primary Health Command

Use the wrapper command from the desktop host:

```bash
jamesos-homelab doctor
```

The wrapper exists because the separate `thedorfer/JamesOS` application project may also provide a command named `jamesos`.

Inside the Homelab virtual environment, the package command is still:

```bash
jamesos doctor
```

## Expected Baseline

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

## Current Providers

| Provider | Current Responsibility |
| --- | --- |
| Linux | Host OS inventory and root filesystem health |
| Storage | Filesystem availability and usage thresholds |
| Gateway | Raspberry Pi SSH, `cloudflared`, `james-home`, and failed units |
| Docker | Docker daemon reachability and running container inventory |
| WordPress | Public website, sitemap, XML-RPC block, hardening, and core integrity |
| Nextcloud | Containers, `occ status`, maintenance mode, database upgrade state, and local endpoint |
| Open WebUI | Container health and local endpoint |
| Backups | Backup root, latest backup artifacts, age, timers, and last service result |

## Current Services

- WordPress public portfolio site
- Nextcloud private cloud
- Open WebUI local AI interface
- Cloudflare Tunnel through Raspberry Pi gateway
- `james-home` gateway dashboard service
- scheduled backups for WordPress, Nextcloud, and Pi gateway

## Current Known Caveats

- The repository is public; secrets and raw incident evidence must remain outside Git.
- `jamesos-homelab` is the recommended desktop command because another local project also uses `jamesos`.
- Gateway discovery currently relies on `pi-gateway.local` resolving from the desktop.
- Backup health checks require read/traverse ACL access for the `james` user to inspect latest-backup metadata.
- WordPress 7.1 required a temporary sitemap status workaround; remove it only after confirming the upstream fix is present and the sitemap still returns HTTP 200.

## Next Milestone

**v0.3.0 - Private Dashboard**

Planned goal: deploy a private dashboard that links to services and displays JamesOS health information backed by `jamesos-homelab doctor`.
