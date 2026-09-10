# WordPress Service

WordPress hosts the public portfolio website for JamesOS Homelab.

## Purpose

The WordPress service provides the public-facing professional site, including portfolio pages, project pages, resume content, contact links, and Google-searchable metadata.

## Current Runtime

Current containers:

- Application container: `wordpress-wordpress-1`
- Database container: `wordpress-db-1`

Current public URL:

```text
https://jamesallendoerfer.com
```

## Health Checks

The JamesOS WordPress provider checks:

- WordPress state through the application container
- public homepage HTTP status
- public sitemap HTTP status
- XML-RPC public blocking status
- `wp-login.php` integrity against the clean Docker image
- unexpected PHP files in the WordPress web root
- search-engine visibility setting
- HTTPS home/site URL behavior
- filesystem hardening constants

Expected healthy output:

```text
✓ WordPress: WordPress core, sitemap, and security checks passed.
```

## Current Hardening Baseline

Current hardening:

- no active WordPress plugins
- `DISALLOW_FILE_EDIT` enabled
- `DISALLOW_FILE_MODS` enabled
- XML-RPC blocked
- Cloudflare rules protect login/admin/XML-RPC paths
- WordPress core refreshed from the official Docker image after the recovery incident
- unexpected root-level PHP files are detected by `jamesos-homelab doctor`
- sitemap and child sitemap return HTTP 200

## Configuration

Environment variables:

```bash
JAMESOS_WORDPRESS_CONTAINER
JAMESOS_WORDPRESS_URL
```

Example:

```bash
JAMESOS_WORDPRESS_URL=https://example.com jamesos-homelab doctor
```

## Public SEO Baseline

The public website currently has:

- published portfolio pages
- private Blog page excluded from the sitemap
- unique page titles
- unique meta descriptions
- working sitemap
- working resume PDF link
- Google Search Console setup completed externally

## Public Documentation Note

This repository is public. Do not commit WordPress salts, database credentials, admin credentials, raw uploads containing private data, or quarantined malware samples.

## Future Work

- Add WordPress Docker compose documentation
- Add restore runbook
- Add public-page SEO regression check to JamesOS Core
- Add backup restore-test verification
- Replace temporary sitemap workaround once WordPress includes the upstream fix
