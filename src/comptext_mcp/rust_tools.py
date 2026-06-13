from __future__ import annotations

from typing import Any


def rust_versions() -> dict[str, Any]:
    return {"rustc": {}, "cargo": {}}


def cargo_metadata() -> dict[str, Any]:
    return {"status": "not implemented"}


def rust_audit(check: bool = True, clippy: bool = False, tests_no_run: bool = True) -> dict[str, Any]:
    return {"commands": [], "results": [], "note": "placeholder"}
