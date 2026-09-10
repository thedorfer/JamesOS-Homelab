# ADR-0002
# Cloudflare Tunnel is the External Entry Point

Status: Accepted

Date: 2026-09-10

## Context

JamesOS services require secure remote access without exposing inbound ports.

## Decision

Cloudflare Tunnel is the only public entry point.

No direct inbound ports are exposed to the Internet.

## Consequences

Remote access depends on Cloudflare.

DNS is centrally managed.

The firewall remains closed.

Attack surface is significantly reduced.

