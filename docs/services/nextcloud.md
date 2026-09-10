# Nextcloud Service

Nextcloud provides the private cloud storage layer for JamesOS.

## Purpose

Nextcloud is used for private file storage, document access, synchronization, and future integration with JamesOS knowledge and automation workflows.

## Current Runtime

Current containers:

- Application container: `nextcloud-app-1`
- Cron container: `nextcloud-cron-1`
- Database container: `nextcloud-db-1`
- Redis container: `nextcloud-redis-1`

The provider checks the local endpoint configured by `JAMESOS_NEXTCLOUD_URL`. The current desktop environment uses the LAN-bound Nextcloud endpoint.

## Configuration

Environment variables:

```bash
JAMESOS_NEXTCLOUD_APP_CONTAINER
JAMESOS_NEXTCLOUD_CRON_CONTAINER
JAMESOS_NEXTCLOUD_DB_CONTAINER
JAMESOS_NEXTCLOUD_REDIS_CONTAINER
JAMESOS_NEXTCLOUD_URL
```

Example:

```bash
JAMESOS_NEXTCLOUD_URL=http://HOST_OR_IP:PORT jamesos-homelab doctor
```

## Health Checks

`jamesos-homelab doctor` checks:

- app container is running
- database container is running
- Redis container is running
- cron container is running
- Docker health status where available
- `occ status --output=json`
- installed state
- maintenance mode
- pending database upgrade flag
- local HTTP endpoint status

Expected healthy output:

```text
✓ Nextcloud: Nextcloud containers, occ status, and local endpoint checks passed.
```

## Operational Notes

The cron container should remain running so scheduled Nextcloud background jobs can execute reliably.

If `jamesos-homelab doctor` reports that maintenance mode is enabled, confirm whether a backup or upgrade is in progress before disabling it.

If `needsDbUpgrade` is true, run the upgrade intentionally rather than allowing it to happen unexpectedly during normal traffic.

## Public Documentation Note

This repository is public. Do not commit Nextcloud admin credentials, database credentials, private documents, sync tokens, or raw config files that contain secrets.

## Future Work

- Add backup restore-test verification
- Add trusted domain inspection
- Add version/update checks
- Add app inventory
- Add storage quota checks
- Add public/private exposure validation
