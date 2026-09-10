# Pi Gateway Service

The Raspberry Pi gateway is the lightweight control-plane host for JamesOS Homelab.

## Purpose

The gateway should remain small, reliable, and easy to rebuild.

It currently provides:

- Cloudflare Tunnel endpoint
- JamesOS home dashboard service
- future reverse-proxy/control-plane responsibilities

The desktop remains the primary application and storage server.

## Default Host

```text
pi-gateway
```

Override for testing:

```bash
JAMESOS_GATEWAY_HOST=192.168.4.XX jamesos doctor
```

Override the SSH user:

```bash
JAMESOS_GATEWAY_USER=james jamesos doctor
```

## Health Checks

The JamesOS Gateway provider checks:

- SSH reachability from the desktop
- remote hostname
- remote uptime
- `cloudflared` systemd service state
- `james-home` systemd service state
- failed systemd units on the gateway

## Configured Services

By default the provider checks:

```text
cloudflared,james-home
```

Override with:

```bash
JAMESOS_GATEWAY_SERVICES=cloudflared,james-home,other-service jamesos doctor
```

## Design Rule

The gateway should be as stateless as practical.

If the Raspberry Pi fails, the recovery path should be:

1. flash a new Pi image
2. install required packages
3. restore tunnel/service configuration
4. resume gateway duties

Persistent application data should stay on the desktop server.

## Future Work

- Add cloudflared tunnel endpoint checks
- Add gateway package/update inventory
- Add gateway backup freshness check
- Add reverse proxy status once deployed
- Add temperature and power diagnostics
