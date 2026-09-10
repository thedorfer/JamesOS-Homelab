# Pi Gateway Service

The Raspberry Pi gateway is the lightweight control-plane host for JamesOS Homelab.

## Purpose

The gateway should remain small, reliable, and easy to rebuild.

It currently provides:

- Cloudflare Tunnel endpoint
- `james-home` dashboard service
- SSH-based gateway inspection for JamesOS health checks
- future reverse-proxy/control-plane responsibilities

The desktop remains the primary application and storage server.

## Current Default Host

Current desktop default:

```text
pi-gateway.local
```

Recommended environment variables:

```bash
export JAMESOS_GATEWAY_HOST=pi-gateway.local
export JAMESOS_GATEWAY_USER=james
```

Override for one command:

```bash
JAMESOS_GATEWAY_HOST=pi-gateway.local JAMESOS_GATEWAY_USER=james jamesos-homelab doctor
```

## Health Checks

The JamesOS Gateway provider checks:

- SSH reachability from the desktop
- remote hostname
- remote uptime
- configured systemd service states
- failed systemd units on the gateway

## Configured Services

By default the provider checks:

```text
cloudflared,james-home
```

Override with:

```bash
JAMESOS_GATEWAY_SERVICES=cloudflared,james-home,other-service jamesos-homelab doctor
```

## Expected Healthy Output

```text
✓ Pi gateway: Gateway SSH, Cloudflare Tunnel, and dashboard checks passed.
```

## Design Rule

The gateway should be as stateless as practical.

If the Raspberry Pi fails, the recovery path should be:

1. flash a new Pi image
2. install required packages
3. restore tunnel/service configuration from secure sources outside Git
4. restore or redeploy gateway services
5. run `jamesos-homelab doctor`
6. confirm gateway checks are green

Persistent application data should stay on the desktop server.

## Public Documentation Note

This repository is public. Do not commit Cloudflare tunnel credentials, private keys, or raw service configuration that contains tokens.

## Future Work

- Add cloudflared tunnel endpoint checks
- Add gateway package/update inventory
- Add gateway backup freshness check
- Add reverse proxy status once deployed
- Add temperature and power diagnostics
