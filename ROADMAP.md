# JamesOS Homelab Roadmap

## v0.1.0 - Foundation

- Repository created
- Initial documentation structure
- Architecture overview
- Security incident documentation
- Initial ADRs

## v0.2.0 - JamesOS Core

- Python package: `jamesos`
- CLI entrypoint: `jamesos`
- Core application object
- Provider registry
- Linux provider
- Docker provider
- `jamesos version`
- `jamesos doctor`
- `jamesos inventory`

## v0.3.0 - WordPress Operations Provider

- WordPress core integrity check as a provider
- Sitemap / SEO audit as a provider
- XML-RPC and hardening verification
- Web root PHP-shell detection
- Recovery runbook integration

## v0.4.0 - Backups and Daily Health

- Backup status provider
- WordPress backup verification
- Nextcloud backup verification
- Pi snapshot verification
- Daily health report

## v0.5.0 - Dashboard Integration

- Homepage dashboard service
- JSON output from JamesOS Core
- Status widgets backed by `jamesos doctor`

## v1.0.0 - Reproducible Platform

- Documented install path
- Documented restore path
- Security baseline
- Monitoring baseline
- Backup baseline
- Service inventory
- Platform health command
