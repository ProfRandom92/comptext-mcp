# Contributing to CompText MCP

Thanks for helping improve CompText MCP.

This project is intended to be friendly to OpenCode users, Rust developers, MCP builders, and people who care about deterministic context tooling.

## Project goals

CompText MCP provides a pip-installable MCP bridge for:

- OpenCode
- Rust workspaces
- CompText CLI / `ctxt`
- deterministic context packs
- replay digests
- safe read-only audits

The MCP server should stay small, inspectable, and deterministic.

## Non-goals

CompText MCP should not become:

- a local LLM runtime
- a model downloader
- an agent framework
- a shell automation bot
- a replacement for the Rust CLI

It should bridge tools safely.

## Development setup

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -e .
.venv/bin/pip install pytest ruff
pytest
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install -e .
.\.venv\Scripts\pip.exe install pytest ruff
.\.venv\Scripts\pytest.exe
```

## Safety rules

All contributions must preserve these rules:

- default mode is read-only
- no local LLM dependency
- no model download in package install
- no secrets in context packs
- no arbitrary shell execution
- every external command must have a timeout
- Rust checks must be safe inspection commands
- write actions must be explicit and easy to audit

## Tool design rules

Good MCP tools should be:

- small
- deterministic
- clearly named
- JSON-friendly
- safe by default
- easy for agents to select correctly

Prefer one focused tool over one large tool with many modes.

## Suggested first contributions

Good first issues:

- improve OpenCode setup docs
- add examples for Windows paths
- add tests for excluded file patterns
- improve Hugging Face Space export docs
- improve error messages when `ctxt` is missing
- add a minimal demo Rust workspace for tests

## Pull request checklist

Before opening a PR:

- run tests
- verify import works
- update README when behavior changes
- add tests for safety-relevant behavior
- keep changes focused

## Communication

Be direct, constructive, and specific. Prefer reproducible examples over vague reports.
