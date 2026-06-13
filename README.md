# CompText MCP

Pip-installable MCP bridge for OpenCode, Rust workspaces, CompText CLI, replay digests, and deterministic context packs.

This package does **not** run a local LLM and does **not** download models. It exposes safe tools that call the existing Rust CLI (`ctxt`) and Rust/Cargo commands.

## Install

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install .
```

Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install .
```

## Requirements

You need `ctxt` available either in `PATH` or through `CTXT_BIN`.

Windows:

```powershell
$env:CTXT_BIN="C:\path\to\ctxt.exe"
$env:CTXT_WORKDIR="C:\path\to\rust-project"
$env:CTXT_MCP_READ_ONLY="1"
```

Linux/macOS:

```bash
export CTXT_BIN="/usr/local/bin/ctxt"
export CTXT_WORKDIR="/path/to/rust-project"
export CTXT_MCP_READ_ONLY=1
```

## OpenCode config

Windows example:

```json
{
  "mcpServers": {
    "comptext": {
      "type": "stdio",
      "command": "C:/path/to/comptext-mcp/.venv/Scripts/comptext-mcp.exe",
      "env": {
        "CTXT_WORKDIR": "C:/path/to/rust-project",
        "CTXT_BIN": "C:/path/to/ctxt.exe",
        "CTXT_MCP_READ_ONLY": "1",
        "CTXT_TIMEOUT_SECS": "30"
      }
    }
  }
}
```

## Tools

- `comptext_status`
- `comptext_pack_context`
- `comptext_rust_audit`
- `comptext_replay_digest`
- `comptext_contract_check`
- `comptext_github_pack`
- `comptext_hf_export_pack`

## Safety defaults

- read-only by default
- no `shell=True`
- no `cargo run`
- no `cargo install`
- no `cargo publish`
- `cargo test` is only allowed with `--no-run`
- excludes `.env`, keys, certs, `.git`, `target`, `node_modules`, `dist`, `build`

## Build wheel

```bash
python -m pip install --upgrade build
python -m build
```

Result:

```text
dist/comptext_mcp-0.1.0-py3-none-any.whl
```
