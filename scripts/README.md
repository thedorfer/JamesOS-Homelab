# Scripts

The `scripts/` directory contains transitional operational utilities.

JamesOS-Homelab is being re-architected around Python providers and `jamesos-homelab doctor`, so long-term business logic should move into the `jamesos/` package rather than remain as standalone shell scripts.

## Current Script Categories

- `scripts/security/` - security and audit utilities created during WordPress recovery

## Current Security Scripts

- `audit-james-site-v2.py`
- `check-wordpress-core-integrity.sh`

These scripts remain useful, but their most important checks are being moved into JamesOS providers.

## Rule

If a script becomes operationally important, decide whether it should become:

1. a JamesOS provider check
2. a JamesOS command
3. a documented one-time runbook step

Avoid creating a large collection of unrelated scripts.
