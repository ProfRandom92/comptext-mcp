from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from .formatter import normalize_text, sha256_bytes, stable_relative
from .policy import is_secret_path
from .runner import ctxt_bin, read_only, try_command, workspace
from .rust_tools import rust_audit, rust_versions

mcp = FastMCP("comptext-mcp")


def _iter_context_files(root: Path, max_bytes: int) -> tuple[list[dict[str, Any]], str, int]:
    records: list[dict[str, Any]] = []
    chunks: list[str] = []
    total = 0
    candidates = sorted([p for p in root.rglob("*") if p.is_file()], key=lambda p: stable_relative(p, root))
    for path in candidates:
        rel = stable_relative(path, root)
        if is_secret_path(Path(rel)):
            continue
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if total + len(data) > max_bytes:
            continue
        text = normalize_text(data)
        digest = sha256_bytes(data)
        records.append({"path": rel, "bytes": len(data), "sha256": digest})
        chunks.append(f"\n--- FILE: {rel} sha256={digest} ---\n{text}")
        total += len(data)
    return records, "".join(chunks).strip(), total


@mcp.tool()
def comptext_status() -> dict[str, Any]:
    """Return CompText, Rust, Cargo, Git, and workspace status."""
    root = workspace()
    return {
        "workspace": str(root),
        "read_only": read_only(),
        "ctxt_bin": ctxt_bin(),
        "ctxt_version": try_command([ctxt_bin(), "version"], cwd=root),
        "rust": rust_versions(),
        "git_root": try_command(["git", "rev-parse", "--show-toplevel"], cwd=root),
        "cargo_toml_detected": (root / "Cargo.toml").exists(),
    }


@mcp.tool()
def comptext_pack_context(max_bytes: int = 250_000) -> dict[str, Any]:
    """Create a deterministic context pack with stable file order and sha256 hashes."""
    root = workspace()
    files, payload, total = _iter_context_files(root, max(1, max_bytes))
    manifest = json.dumps(files, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "workspace": str(root),
        "file_count": len(files),
        "total_bytes": total,
        "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "files": files,
        "payload": payload,
    }


@mcp.tool()
def comptext_rust_audit(check: bool = True, clippy: bool = False, tests_no_run: bool = True) -> dict[str, Any]:
    """Run safe read-only Rust checks."""
    return rust_audit(check=check, clippy=clippy, tests_no_run=tests_no_run)


@mcp.tool()
def comptext_replay_digest(max_bytes: int = 250_000) -> dict[str, Any]:
    """Create a deterministic replay/evidence digest for the current workspace."""
    root = workspace()
    files, _, total = _iter_context_files(root, max(1, max_bytes))
    manifest = json.dumps(files, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "workspace": str(root),
        "mode": "read-only" if read_only() else "write-enabled",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "ctxt_version": try_command([ctxt_bin(), "version"], cwd=root),
        "rust": rust_versions(),
        "total_bytes": total,
        "files": files,
        "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
    }


@mcp.tool()
def comptext_contract_check() -> dict[str, Any]:
    """Check local safety contracts for OpenCode usage."""
    root = workspace()
    findings = []
    env = {
        "CTXT_BIN": ctxt_bin(),
        "CTXT_WORKDIR": str(root),
        "CTXT_MCP_READ_ONLY": os.environ.get("CTXT_MCP_READ_ONLY", "1"),
    }
    if not env["CTXT_BIN"]:
        findings.append({"level": "error", "message": "CTXT_BIN is empty"})
    if not root.exists():
        findings.append({"level": "error", "message": "CTXT_WORKDIR does not exist"})
    if not read_only():
        findings.append({"level": "warning", "message": "CTXT_MCP_READ_ONLY is disabled"})
    suspicious = [stable_relative(p, root) for p in root.rglob("*") if p.is_file() and is_secret_path(p.relative_to(root))]
    return {
        "workspace": str(root),
        "env": env,
        "findings": findings,
        "secret_like_paths_excluded": suspicious[:200],
        "ok": not any(f["level"] == "error" for f in findings),
    }


@mcp.tool()
def comptext_github_pack() -> dict[str, Any]:
    """Prepare a local GitHub summary pack without network calls."""
    root = workspace()
    files, _, total = _iter_context_files(root, 120_000)
    return {
        "workspace": str(root),
        "summary": "CompText workspace summary generated locally.",
        "file_count": len(files),
        "total_bytes": total,
        "repo_map": [f["path"] for f in files[:200]],
        "release_checklist": ["Run tests", "Build wheel", "Verify OpenCode config", "Attach wheel and README to GitHub release"],
    }


@mcp.tool()
def comptext_hf_export_pack() -> dict[str, Any]:
    """Return Hugging Face Space/Card export text without upload or token usage."""
    return {
        "files": {
            "README.md": "---\ntitle: CompText MCP Bridge\nemoji: 🧩\nsdk: docker\nlicense: mit\n---\n\n# CompText MCP Bridge\n\nDeterministic MCP bridge for OpenCode, Rust workspaces, replay digests, and context packs.\n\nNo model weights. No local LLM.\n",
            "metadata.yaml": "title: CompText MCP Bridge\nlicense: mit\n",
            "usage.md": "Install with pip, configure OpenCode stdio, set CTXT_BIN and CTXT_WORKDIR.\n",
        },
        "upload": False,
        "model_weights": False,
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
