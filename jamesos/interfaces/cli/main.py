"""JamesOS command line interface."""

from __future__ import annotations

import argparse
import json
import platform
from dataclasses import asdict, is_dataclass
from typing import Any

from jamesos import __version__
from jamesos.core.app import JamesOS


def _json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _print_check(status: str, name: str, message: str) -> None:
    icon = {
        "ok": "✓",
        "warn": "!",
        "fail": "✗",
        "unknown": "?",
    }.get(status, "?")
    print(f"{icon} {name}: {message}")


def cmd_version(args: argparse.Namespace) -> int:
    data = {
        "name": "JamesOS",
        "package": "jamesos-homelab",
        "version": __version__,
        "python": platform.python_version(),
        "platform": platform.platform(),
    }

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print("JamesOS")
        print(f"Version: {__version__}")
        print(f"Python:  {data['python']}")
        print(f"Host:    {data['platform']}")

    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    app = JamesOS()
    report = app.doctor()

    if args.json:
        print(json.dumps(report, indent=2, default=_json_default))
    else:
        print("JamesOS Doctor")
        print()
        for check in report.checks:
            _print_check(check.status, check.name, check.message)
        print()
        print(f"Overall: {report.status.upper()}")

    return 0 if report.status in {"ok", "warn"} else 2


def cmd_inventory(args: argparse.Namespace) -> int:
    app = JamesOS()
    report = app.inventory()

    if args.json:
        print(json.dumps(report, indent=2, default=_json_default))
        return 0

    print("JamesOS Inventory")
    print()
    for section, values in report.sections.items():
        print(f"## {section}")
        for key, value in values.items():
            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key}: {value}")
        print()

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jamesos",
        description="JamesOS Homelab operations platform",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    version = sub.add_parser("version", help="show JamesOS version")
    version.add_argument("--json", action="store_true", help="print JSON")
    version.set_defaults(func=cmd_version)

    doctor = sub.add_parser("doctor", help="run platform health checks")
    doctor.add_argument("--json", action="store_true", help="print JSON")
    doctor.set_defaults(func=cmd_doctor)

    inventory = sub.add_parser("inventory", help="show platform inventory")
    inventory.add_argument("--json", action="store_true", help="print JSON")
    inventory.set_defaults(func=cmd_inventory)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
