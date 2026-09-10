# Security Policy

JamesOS-Homelab assumes compromise is possible and designs for recovery.

## Security Principles

- Rebuild over repair
- Git is the source of truth
- No secrets in Git
- Least privilege where practical
- Cloudflare protects public entry points
- WordPress core should be replaced from trusted sources when integrity is uncertain
- Operational checks should be automated through JamesOS Core

## Current WordPress Baseline

- WordPress core rebuilt from the official Docker image
- No active plugins
- XML-RPC blocked
- WordPress file editor disabled
- Cloudflare Browser Integrity Check enabled
- Cloudflare Bot Fight Mode enabled
- Cloudflare WAF rules protect `/wp-login.php`, `/wp-admin`, and `/xmlrpc.php`
- Site audit and core integrity checks are stored under `scripts/security`

## Secret Handling

Never commit:

- `.env` files
- Cloudflare tokens
- database passwords
- SSH private keys
- WordPress salts
- backup archives
- raw incident evidence containing secrets

Use `.env.example` files for documentation.

## Reporting / Tracking

Security findings should become:

- an incident document under `docs/security`
- an ADR if the recovery changes architecture
- a JamesOS health check if the finding can be automated
