# Python CLI Development

JamesOS-Homelab now uses a Python application core with a CLI as the first interface.

## Install locally

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Run

```bash
jamesos version
jamesos doctor
jamesos inventory
```

You can also run it without installing the console script:

```bash
python -m jamesos version
```

## Test

```bash
pytest
```

## Architecture rule

Business logic belongs in Python.

Shell commands are allowed only behind provider boundaries such as `jamesos.providers.linux` and `jamesos.providers.docker`.
