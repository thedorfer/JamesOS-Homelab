# Python CLI Development

JamesOS-Homelab uses a Python application core with a CLI as the first interface.

## Install Locally

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Run Inside the Virtual Environment

```bash
jamesos version
jamesos doctor
jamesos inventory
```

## Run from the Desktop Host

The desktop host also has a separate `jamesos` command from the `thedorfer/JamesOS` application project. To avoid command-name collisions, the homelab wrapper command is:

```bash
jamesos-homelab version
jamesos-homelab doctor
jamesos-homelab inventory
```

The wrapper activates the Homelab virtual environment and runs the correct CLI.

## Current Gateway Defaults

Recommended shell defaults on the desktop:

```bash
export JAMESOS_GATEWAY_HOST=pi-gateway.local
export JAMESOS_GATEWAY_USER=james
```

## Module Entry Point

You can also run the CLI without using the console script:

```bash
python -m jamesos version
python -m jamesos.interfaces.cli.main doctor
```

## Test

```bash
pytest
```

## Architecture Rule

Business logic belongs in Python.

Shell commands are allowed only behind provider boundaries such as:

- `jamesos.providers.linux`
- `jamesos.providers.storage`
- `jamesos.providers.gateway`
- `jamesos.providers.docker`
- `jamesos.providers.wordpress`
- `jamesos.providers.nextcloud`
- `jamesos.providers.open_webui`
- `jamesos.providers.backups`

Interfaces should format results. Providers should perform integration work. Core should coordinate providers and return structured models.
