# Docker Runtime

Docker is the primary application runtime for JamesOS Homelab.

## Current Role

The desktop server runs the current application stack through Docker.

Current monitored containers include:

- WordPress application
- WordPress database
- Nextcloud application
- Nextcloud cron
- Nextcloud database
- Nextcloud Redis
- Open WebUI

## JamesOS Checks

The Docker provider checks:

- Docker engine reachability
- Docker server version
- running container count
- readable container inventory

The service providers then check their own service-specific containers and endpoints.

## Public Documentation Rules

This repository is public. Do not commit:

- `.env` files
- database passwords
- application secrets
- bind-mounted private data
- raw Docker inspect output containing sensitive labels or environment variables

Use `.env.example` files when configuration needs to be documented.

## Future Work

- Add sanitized compose examples
- Add update procedure for Docker images
- Add rollback procedure
- Add immutable/read-only WordPress runtime documentation
- Add Docker image age/update checks to `jamesos-homelab doctor`
