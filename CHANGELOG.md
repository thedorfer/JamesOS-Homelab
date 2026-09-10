# Changelog

## 0.2.7 - Backup permission handling

- Updated the Backups provider so permission-denied backup directories produce a warning instead of crashing the CLI.
- Added explicit path accessibility metadata to backup inventory output.
- Bumped package metadata and tests to `0.2.7`.

## 0.2.6 - Backups provider

- Added a Backups provider for `jamesos doctor` and `jamesos inventory`.
- Added backup-root, latest-backup, backup-age, systemd timer, and systemd service result checks.
- Added backup service documentation.

## 0.2.5 - Open WebUI provider

- Added an Open WebUI provider for `jamesos doctor` and `jamesos inventory`.
- Added checks for the Open WebUI Docker container, health status, and local endpoint.
- Added Open WebUI service documentation.

## 0.2.4 - CLI module entry point

- Added a `__main__` guard so `python -m jamesos.interfaces.cli.main <command>` executes the CLI correctly.
- Bumped package metadata and tests to `0.2.4`.

## 0.2.3 - Nextcloud provider

- Added a Nextcloud provider for `jamesos doctor` and `jamesos inventory`.
- Added checks for the Nextcloud app, cron, database, and Redis containers.
- Added `occ status --output=json` inspection for installed state, maintenance mode, and database upgrade state.
- Added local Nextcloud endpoint verification.
- Added Nextcloud service documentation.

## 0.2.2 - WordPress HTTPS proxy normalization

- Normalized WordPress provider checks for the HTTPS reverse-proxy context used by Cloudflare Tunnel.
- Added explicit reporting for WordPress `home`/`siteurl` options, `WP_HOME`/`WP_SITEURL` constants, and filesystem hardening constants.
- Kept dashboard/CLI warnings focused on actual public-site misconfiguration instead of CLI-only URL scheme behavior.

## 0.2.1 - WordPress provider

- Added a WordPress provider for `jamesos doctor` and `jamesos inventory`.
- Added checks for WordPress state, public sitemap availability, XML-RPC blocking, `wp-login.php` integrity, and unexpected PHP files in the WordPress web root.
- Simplified Docker inventory output so `jamesos inventory` is readable from the terminal.

## 0.2.0 - JamesOS Core begins

- Added Python packaging with `pyproject.toml`.
- Added installable `jamesos` console command.
- Added JamesOS Core application object.
- Added provider registry and provider protocol.
- Added Linux and Docker providers.
- Added `jamesos version`.
- Added `jamesos doctor`.
- Added `jamesos inventory`.
- Added initial tests.
- Added ADR-0006 documenting JamesOS Core as the platform architecture.
- Added developer guide for the Python CLI.

## 0.1.0 - Repository foundation

- Created repository foundation.
- Added initial README and vision.
- Added architecture overview.
- Added WordPress security incident documentation.
- Added initial ADRs.
- Added site audit and WordPress core integrity scripts.
