# ADR-0004
# Rebuild Over Repair

Status: Accepted

Date: 2026-09-10

## Context

During recovery of the WordPress compromise, rebuilding the WordPress core from the official Docker image proved safer than attempting to repair individual files.

## Decision

Whenever core system integrity is in doubt, prefer rebuilding from trusted sources rather than attempting manual repair.

## Consequences

Known-good state is restored quickly.

Integrity can be verified.

Recovery procedures remain repeatable.

