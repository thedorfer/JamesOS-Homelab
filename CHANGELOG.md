# Changelog

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
