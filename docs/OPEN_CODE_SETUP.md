# OpenCode Setup

This guide shows how to connect CompText MCP to OpenCode.

## 1. Install the package

From the repository root:

Windows PowerShell:

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

## 2. Locate `ctxt`

CompText MCP expects the CompText Rust CLI to be available either as `ctxt` in PATH or through `CTXT_BIN`.

Example Windows path:

```text
C:/Users/YOU/Desktop/comptext-cli/target/release/ctxt.exe
```

Example Linux path:

```text
/usr/local/bin/ctxt
```

## 3. Configure OpenCode

Use the Windows example from `examples/opencode.windows.json` or the Unix example from `examples/opencode.unix.json`.

Important fields:

```json
{
  "CTXT_WORKDIR": "C:/path/to/your/rust-project",
  "CTXT_BIN": "C:/path/to/ctxt.exe",
  "CTXT_MCP_READ_ONLY": "1",
  "CTXT_TIMEOUT_SECS": "30"
}
```

## 4. Verify

In OpenCode, the MCP server should expose these tools:

- `comptext_status`
- `comptext_pack_context`
- `comptext_rust_audit`
- `comptext_replay_digest`
- `comptext_contract_check`
- `comptext_github_pack`
- `comptext_hf_export_pack`

## Troubleshooting

### OpenCode cannot start the server

Check that the `command` path points to the virtual environment executable.

Windows:

```text
C:/path/to/comptext-mcp/.venv/Scripts/comptext-mcp.exe
```

Linux/macOS:

```text
/path/to/comptext-mcp/.venv/bin/comptext-mcp
```

### `ctxt` not found

Set `CTXT_BIN` to the absolute path of the binary.

### Wrong project analyzed

Set `CTXT_WORKDIR` to the target project, not to the CompText MCP repository.
