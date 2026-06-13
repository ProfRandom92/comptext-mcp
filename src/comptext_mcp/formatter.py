from __future__ import annotations

import hashlib
from pathlib import Path


def normalize_text(data: bytes) -> str:
    return data.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()
