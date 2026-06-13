from pathlib import Path

import pytest

from comptext_mcp.policy import assert_safe_cargo_args, is_secret_path


def test_secret_paths_are_excluded() -> None:
    for value in [".env", "x.pem", "x.key", "target/debug/app", ".git/config"]:
        assert is_secret_path(Path(value))


def test_safe_cargo_test_requires_no_run() -> None:
    assert_safe_cargo_args(["cargo", "test", "--workspace", "--no-run"])
    with pytest.raises(ValueError):
        assert_safe_cargo_args(["cargo", "test", "--workspace"])


def test_forbidden_cargo_run() -> None:
    with pytest.raises(ValueError):
        assert_safe_cargo_args(["cargo", "run"])
