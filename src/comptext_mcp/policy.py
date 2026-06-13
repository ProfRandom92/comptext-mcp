from __future__ import annotations

from pathlib import Path

DEFAULT_EXCLUDES = {
    ".git",
    "target",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
}

SECRET_NAMES = {".env", ".env.local", ".env.production"}
SECRET_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".crt", ".sqlite", ".db"}
FORBIDDEN_CARGO_SUBCOMMANDS = {"run", "install", "publish", "login", "owner"}


def is_secret_path(path: Path) -> bool:
    parts = set(path.parts)
    if parts & DEFAULT_EXCLUDES:
        return True
    name = path.name.lower()
    if name in SECRET_NAMES:
        return True
    if any(name.endswith(suffix) for suffix in SECRET_SUFFIXES):
        return True
    return False


def assert_safe_cargo_args(args: list[str]) -> None:
    if not args or args[0] != "cargo":
        raise ValueError("Only cargo commands are accepted here.")
    if len(args) < 2:
        raise ValueError("Missing cargo subcommand.")

    subcommand = args[1]
    if subcommand in FORBIDDEN_CARGO_SUBCOMMANDS:
        raise ValueError(f"Forbidden cargo subcommand: {subcommand}")
    if subcommand == "test" and "--no-run" not in args:
        raise ValueError("cargo test must include --no-run.")

    forbidden_tokens = [chr(38) + chr(38), chr(124), chr(59)]
    if any(token in arg for arg in args for token in forbidden_tokens):
        raise ValueError("Shell chaining is forbidden.")
