# Storage Service

JamesOS uses local desktop storage as the primary persistence layer for the homelab platform.

## Current Storage Paths

Default monitored paths:

```text
/
/mnt/storage
```

These can be overridden with:

```bash
JAMESOS_STORAGE_PATHS=/,/mnt/storage,/other/path jamesos doctor
```

## Health Checks

The JamesOS Storage provider checks:

- configured paths exist
- configured paths are accessible
- filesystem usage is below the warning threshold
- filesystem usage is below the failure threshold

## Thresholds

Default warning threshold:

```text
85%
```

Default failure threshold:

```text
95%
```

Override with:

```bash
JAMESOS_STORAGE_WARN_PERCENT=80 JAMESOS_STORAGE_FAIL_PERCENT=90 jamesos doctor
```

## Current Role

The desktop remains the primary storage and application server.

The Raspberry Pi is treated as a gateway appliance and should remain as stateless as practical.

## Future Work

- Add SMART health checks after configuring safe read-only sudo access for `smartctl`
- Add disk temperature checks
- Add storage growth trend checks
- Add backup-size trend checks
- Add alerting when free space drops below threshold
