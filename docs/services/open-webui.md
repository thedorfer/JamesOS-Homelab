# Open WebUI Service

Open WebUI is the local AI interface for JamesOS.

## Purpose

Open WebUI provides a browser-based interface for local AI and model experimentation.

In the JamesOS architecture it is the first visible AI application, but it should eventually become one client of JamesOS Core rather than a standalone operational silo.

## Current Deployment

- Container: `open-webui`
- Image family: `ghcr.io/open-webui/open-webui:ollama`
- Default local endpoint: `http://127.0.0.1:3000`
- Host port: `3000`

## JamesOS Checks

The `OpenWebUIProvider` checks:

- Docker container state
- Docker health status, when available
- local HTTP endpoint status

Accepted local endpoint responses are:

- `200` - reachable
- `302` - reachable with redirect
- `401` / `403` - protected but reachable

Expected healthy output:

```text
✓ Open WebUI: Open WebUI container and local endpoint checks passed.
```

## Configuration

Environment variables:

```bash
JAMESOS_OPENWEBUI_CONTAINER
JAMESOS_OPENWEBUI_URL
```

Example:

```bash
JAMESOS_OPENWEBUI_URL=http://HOST_OR_IP:3000 jamesos-homelab doctor
```

## Public Documentation Note

This repository is public. Do not commit model credentials, API keys, private prompts, local document indexes, or user data from Open WebUI.

## Future Work

- Add model runtime inspection
- Add local model inventory
- Add endpoint latency checks
- Add private/public exposure validation
- Integrate AI health into the daily JamesOS report
- Connect Open WebUI to a future JamesOS REST API or tool interface
