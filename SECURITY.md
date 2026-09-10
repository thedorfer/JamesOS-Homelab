# Security Policy

JamesOS-Homelab assumes compromise is possible and designs for prevention, detection, and recovery.

## Security Principles

- Rebuild over repair
- No secrets in Git
- Git is the source of truth
- Least privilege where practical
- Public services should be protected at the edge
- Application core files should be replaced from trusted sources when integrity is uncertain
- Operational checks should be automated through JamesOS Core
- Findings that can recur should become health checks

## Current WordPress Baseline

Current WordPress hardening state:

- WordPress core refreshed from the official Docker image
- No active WordPress plugins
- WordPress file editor disabled with `DISALLOW_FILE_EDIT`
- WordPress dashboard file modifications disabled with `DISALLOW_FILE_MODS`
- XML-RPC blocked
- Public sitemap returns HTTP 200
- Public homepage returns HTTP 200
- `wp-login.php` integrity is checked against the clean Docker image
- Unexpected root-level PHP files are detected by the WordPress provider
- Cloudflare Browser Integrity Check enabled
- Cloudflare Bot Fight Mode enabled
- Cloudflare rules protect `/wp-login.php`, `/wp-admin`, and `/xmlrpc.php`

## Current Operations Baseline

The primary health command is:

```bash
jamesos-homelab doctor
```

The expected secure baseline is:

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

## Secret Handling

Never commit:

- `.env` files
- Cloudflare tokens
- database passwords
- SSH private keys
- WordPress salts
- backup archives
- raw incident evidence containing credentials or tokens
- personal documents or private family data

Use `.env.example` files for documentation.

## Public Documentation Rules

This repository is public. Documentation should avoid publishing:

- public IPs that are not already intentionally exposed
- Cloudflare tunnel tokens or IDs
- database credentials
- WordPress salts
- SSH keys
- raw malicious payloads from incidents
- sensitive family or private data

Internal RFC1918 addresses may appear in examples when useful, but prefer environment-variable examples when possible.

## Reporting / Tracking

Security findings should become:

- an incident document under `docs/security`
- an Architecture Decision Record if the recovery changes architecture
- a JamesOS health check if the finding can be automated
- a runbook if the response may need to be repeated

## Recovery Philosophy

If core application integrity is questionable, rebuild from trusted sources and then verify.

Manual cleanup is acceptable for triage, but the end state should be:

1. trusted source restored
2. suspicious artifacts removed or quarantined
3. secrets rotated when exposure is possible
4. public attack surface reduced
5. a repeatable health check added
