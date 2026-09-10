# Backups Service

JamesOS uses scheduled host-level backups to protect the public portfolio, private cloud, and Raspberry Pi gateway.

## Current Backup Sets

Current monitored backup sets:

- WordPress
- Nextcloud
- Raspberry Pi gateway

## Current Backup Root

Default path:

```text
/mnt/storage/Storage/backups
```

The path can be overridden for local testing with:

```bash
JAMESOS_BACKUP_ROOT=/path/to/backups jamesos-homelab doctor
```

## Health Checks

The JamesOS Backups provider checks:

- backup root exists
- backup root is accessible
- latest WordPress backup exists
- latest Nextcloud backup exists
- latest Raspberry Pi gateway backup exists
- latest backup age is within the configured threshold
- related systemd timers are visible and active
- related systemd services do not report a failed last result

Expected healthy output:

```text
✓ Backups: Backup timers and latest backup artifacts look healthy.
```

## Backup Visibility

Backup directories are intentionally restricted, but the `jamesos-homelab` health check needs permission to inspect the `latest` symlinks and timestamps.

Grant read/traverse access to the `james` user without making backup contents broadly public:

```bash
sudo setfacl -R -m u:james:rx /mnt/storage/Storage/backups
sudo setfacl -R -m d:u:james:rx /mnt/storage/Storage/backups
```

This gives the JamesOS CLI enough access to verify backup presence and age while preserving the root-owned backup structure.

## Age Threshold

By default, a latest backup older than 48 hours creates a warning.

Override with:

```bash
JAMESOS_BACKUP_MAX_AGE_HOURS=72 jamesos-homelab doctor
```

## Commands

```bash
jamesos-homelab doctor
jamesos-homelab inventory
```

## Public Documentation Note

This repository is public. Do not commit backup archives, database dumps, raw service configuration containing credentials, or private Nextcloud data.

## Future Work

- Add backup size trend checks
- Add backup restore-test status
- Add automatic daily report output
- Add alerting when backups are stale or missing
- Add separate checks for offsite backup coverage
