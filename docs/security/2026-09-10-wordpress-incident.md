# WordPress Recovery - 2026-09-10

## Summary

A compromised WordPress installation was recovered, hardened, and added to JamesOS health monitoring.

This document is intentionally public-safe. It records the operational response and lessons learned without publishing raw malicious payloads, credentials, tokens, or unnecessary attacker detail.

## Impact

Observed impact:

- WordPress login was unavailable because a core login file had been moved or renamed.
- The public sitemap initially returned an incorrect HTTP status that prevented Google Search Console from fetching it.
- Unauthorized PHP files were present in WordPress-controlled paths.
- Logs showed interactive use of a file-management style web shell.

No secrets are stored in this repository, and raw quarantined files are not committed here.

## Indicators

High-level indicators:

- unexpected PHP files in the WordPress web root
- unexpected PHP files in core-owned directories
- missing `wp-login.php`
- web requests to unauthorized PHP files
- file-manager style activity against WordPress paths

## Recovery Actions Completed

- Quarantined suspicious PHP files outside the repository
- Removed unauthorized files from the live WordPress web root
- Restored `wp-login.php` from the official WordPress Docker image
- Rebuilt WordPress core from the official Docker image
- Verified no missing core files
- Verified no modified core files
- Verified no unexpected files in `wp-admin` or `wp-includes`
- Changed the WordPress administrator password to a new unique password
- Disabled XML-RPC
- Enabled `DISALLOW_FILE_EDIT`
- Enabled `DISALLOW_FILE_MODS`
- Restricted filesystem ownership/permissions so core files are not broadly writable
- Configured Cloudflare protections for login, admin, and XML-RPC paths
- Added WordPress checks to `jamesos doctor`
- Added backup and storage visibility checks to JamesOS

## Current Verified Baseline

The expected command is:

```bash
jamesos-homelab doctor
```

Expected result:

```text
✓ WordPress: WordPress core, sitemap, and security checks passed.
Overall: OK
```

The full platform baseline also includes Linux, storage, Pi gateway, Docker, Nextcloud, Open WebUI, and backups.

## Lessons Learned

- Rebuilding from a trusted source is safer than manually repairing a compromised application tree.
- File-manager plugins or file-management endpoints create significant risk if exposed or vulnerable.
- Public services should be protected at the edge before requests reach the origin.
- Recovery work should become automated health checks.
- Public incident documentation should explain what happened without publishing secrets or raw payloads.
- Git should hold runbooks and clean automation, not private evidence.

## Follow-Up Work

- Keep WordPress plugin usage minimal.
- Prefer updates through Docker image refreshes rather than dashboard-driven file changes.
- Add scheduled `jamesos-homelab doctor` reports.
- Add a restore-test process for WordPress and Nextcloud backups.
- Continue moving operational checks into JamesOS providers.
