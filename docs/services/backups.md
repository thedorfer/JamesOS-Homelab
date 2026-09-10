# Backups Service

JamesOS uses scheduled host-level backups to protect the public portfolio, private cloud, and Raspberry Pi gateway.

## Current Backup Sets

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
JAMESOS_BACKUP_ROOT=/path/to/backups jamesos doctor
```

## Health Checks

The JamesOS Backups provider checks:

- backup root exists
- latest WordPress backup exists
- latest Nextcloud backup exists
- latest Raspberry Pi gateway backup exists
- latest backup age is within the configured threshold
- related systemd timers are visible
- related systemd services do not report a failed last result

## Age Threshold

By default, a latest backup older than 48 hours creates a warning.

Override with:

```bash
JAMESOS_BACKUP_MAX_AGE_HOURS=72 jamesos doctor
```

## Commands

```bash
jamesos doctor
jamesos inventory
```

## Future Work

- Add backup size trend checks
- Add backup restore-test status
- Add automatic daily report output
- Add alerting when backups are stale or missing
