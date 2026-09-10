# Cloudflare Configuration

Cloudflare provides the public edge for JamesOS Homelab.

## Current Role

Cloudflare is used for:

- DNS for public hostnames
- Cloudflare Tunnel access to internal services
- WAF/security rules for sensitive WordPress paths
- bot and browser-integrity protections

## Current Baseline

Current public WordPress protections:

- Browser Integrity Check enabled
- Bot Fight Mode enabled
- login/admin paths challenged when appropriate
- XML-RPC blocked at the edge and origin

## Documentation Rules

This repository is public. Do not commit:

- Cloudflare API tokens
- tunnel credentials
- tunnel JSON credential files
- origin certificates or private keys
- account IDs unless intentionally public
- screenshots that expose sensitive IDs or tokens

Use sanitized examples and environment-variable names instead.

## Related Docs

- `cloudflare/waf/current-rules.md`
- `docs/services/gateway.md`
- `docs/security/2026-09-10-wordpress-incident.md`
