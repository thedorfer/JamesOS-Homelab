"""Safe shell execution helpers.

JamesOS business logic should live in Python.  This module is the narrow
boundary where provider modules may call system tools such as docker, df, or
systemctl.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from collections.abc import Sequence


@dataclass(slots=True)
class CommandResult:
    args: Sequence[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def run(args: Sequence[str], timeout: int = 15) -> CommandResult:
    """Run a command without invoking a shell."""

    completed = subprocess.run(
        list(args),
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return CommandResult(
        args=args,
        returncode=completed.returncode,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )
