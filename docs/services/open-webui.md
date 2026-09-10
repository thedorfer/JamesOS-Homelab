# Open WebUI Service

Open WebUI is the local AI interface for JamesOS.

## Purpose

Open WebUI provides a browser-based interface for local AI and model experimentation.  In the JamesOS architecture it is the first visible AI application, but it should eventually become one client of JamesOS Core rather than a standalone service.

## Current Deployment

- Container: `open-webui`
- Image: `ghcr.io/open-webui/open-webui:ollama`
- Local endpoint: `http://127.0.0.1:3000`
- Host port: `3000`

## JamesOS Checks

The `OpenWebUIProvider` checks:

- Docker container state
- Docker health status, when available
- Local HTTP endpoint status

Accepted local endpoint responses are:

- `200` - reachable
- `302` - reachable with redirect
- `401` / `403` - protected but reachable

## Configuration

Environment variables:

- `JAMESOS_OPENWEBUI_CONTAINER` - override the Docker container name
- `JAMESOS_OPENWEBUI_URL` - override the local URL

Example:

```bash
JAMESOS_OPENWEBUI_URL=http://192.168.5.105:3000 jamesos doctor
```

## Future Work

- Add model runtime inspection.
- Add local model inventory.
- Add endpoint latency checks.
- Integrate AI health into the daily JamesOS report.
- Connect Open WebUI to the future JamesOS REST API.
