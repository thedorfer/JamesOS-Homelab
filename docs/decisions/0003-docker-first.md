# ADR-0003
# Docker First Deployment

Status: Accepted

Date: 2026-09-10

## Context

Applications require simple deployment, upgrades and recovery.

## Decision

Every service should run inside Docker unless a strong reason exists not to.

## Consequences

Services remain isolated.

Upgrades become predictable.

Configuration is version controlled.

Infrastructure is reproducible.

