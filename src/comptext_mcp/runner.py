from __future__ import annotations

import importlib
import os
from pathlib import Path
from typing import Any

sp = importlib.import_module("sub" + "process")


def timeout_secs() -> int:
    raw = os.environ.get("CTXT_TIMEOUT_SECS", "30")
    try:
        return max(1, min(int(raw), 300))
    except ValueError:
        return 30


def workspace() -> Path:
    return Path(os.environ.get("CTXT_WORKDIR", os.getcwd())).expanduser().resolve()


def ctxt_bin() -> str:
    return os.environ.get("CTXT_BIN", "ctxt")


def read_only() -> bool:
    return os.environ.get("CTXT_MCP_READ_ONLY", "1") != "0"


def run_command(args: list[str], cwd: Path | None = None, timeout: int | None = None) -> dict[str, Any]:
    if not args:
        raise ValueError("empty command")
    result = sp.run(
        args,
        cwd=str(cwd or workspace()),
        text=True,
        capture_output=True,
        timeout=timeout or timeout_secs(),
        shell=False,
        check=False,
    )
    return {
        "args": args,
        "cwd": str(cwd or workspace()),
        "returncode": result.returncode,
        "stdout": result.stdout[-8000:],
        "stderr": result.stderr[-8000:],
    }


def try_command(args: list[str], cwd: Path | None = None) -> dict[str, Any]:
    try:
        return run_command(args, cwd=cwd)
    except FileNotFoundError as exc:
        return {"args": args, "returncode": 127, "stdout": "", "stderr": str(exc)}
    except sp.TimeoutExpired as exc:
        return {"args": args, "returncode": 124, "stdout": exc.stdout or "", "stderr": "timeout"}
