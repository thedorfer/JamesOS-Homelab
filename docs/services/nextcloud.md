# Nextcloud Service

Nextcloud provides the private cloud storage layer for JamesOS.

## Purpose

Nextcloud is used for private file storage, document access, synchronization, and future integration with JamesOS knowledge and automation workflows.

## Current Runtime

- Application container: `nextcloud-app-1`
- Cron container: `nextcloud-cron-1`
- Database container: `nextcloud-db-1`
- Redis container: `nextcloud-redis-1`
- Local endpoint: `http://192.168.5.105:8081`

The endpoint and container names can be overridden with environment variables:

```bash
JAMESOS_NEXTCLOUD_APP_CONTAINER
JAMESOS_NEXTCLOUD_CRON_CONTAINER
JAMESOS_NEXTCLOUD_DB_CONTAINER
JAMESOS_NEXTCLOUD_REDIS_CONTAINER
JAMESOS_NEXTCLOUD_URL
```

## Health Checks

`jamesos doctor` checks:

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

## Operational Notes

The cron container should remain running so scheduled Nextcloud background jobs can execute reliably.

If `jamesos doctor` reports that maintenance mode is enabled, confirm whether a backup or upgrade is in progress before disabling it.

If `needsDbUpgrade` is true, run the upgrade intentionally rather than allowing it to happen unexpectedly during normal traffic.
