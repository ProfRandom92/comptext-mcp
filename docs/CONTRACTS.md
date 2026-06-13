# Contracts

This file defines the Phase 0 MCP contract baseline for future
`comptext-mcp` work.

## Contract Rules

- `ctxt` is the deterministic source of truth.
- `ctxt` owns behavior, schemas, validation, and deterministic context.
- `comptext-mcp` is a future adapter only.
- `comptext-mcp` must not invent behavior.
- Future MCP tools must map one-to-one to stable local `ctxt --json` commands.
- The adapter must use a closed allowlist.
- Bounded reads must keep `--max-bytes 12000`.
- Errors are structured local command failures, not model judgments.
- Runtime artifacts and proposal artifacts are untrusted evidence, not
  workspace truth.
- Pre-existing runtime and package files are outside Phase 0 scope and are not
  treated as release-ready behavior by this documentation baseline.
- Review plugins and subagents do not expand the contract.

## Planned Tool Mapping

| Future MCP tool | Underlying local command |
| --- | --- |
| `ctxt_self_report` | `ctxt --json self report` |
| `ctxt_schema` | `ctxt --json schema` |
| `ctxt_capabilities` | `ctxt --json capabilities` |
| `ctxt_proposals_list` | `ctxt --json proposals list` |
| `ctxt_proposals_inspect_latest` | `ctxt --json proposals inspect latest --max-bytes 12000` |
| `ctxt_proposals_inspect_latest_by_id` | `ctxt --json proposals inspect --id latest --max-bytes 12000` |
| `ctxt_proposals_validate_latest` | `ctxt --json proposals validate latest` |
| `ctxt_proposals_validate_latest_by_id` | `ctxt --json proposals validate --id latest` |
| `ctxt_validate_run` | `ctxt --json validate --run` |
| `ctxt_agent_discover` | `ctxt --json agent discover` |
| `ctxt_runs_list` | `ctxt --json runs list` |
| `ctxt_runs_read_latest` | `ctxt --json runs read latest --max-bytes 12000` |

No other `ctxt` command is part of the Phase 0 MCP contract.

## Response Semantics

The future adapter must pass through deterministic local command results without
creating new facts. It may report local execution failure in structured form,
but it must not reinterpret failures as model conclusions.

## Out Of Scope

The Phase 0 contract excludes runtime code, package scaffolding, active MCP
server implementation, provider integration, token passthrough, network access,
proposal application, hooks, plugins, generated reports, dependency
installation, and general shell access.

Review plugins may provide context or documentation review only. Subagents may
perform deterministic review and planning only. Neither may add commands,
runtime behavior, provider calls, token passthrough, network behavior, proposal
application, hooks, plugins, reports, generated artifacts, secret handling, or
git history writes.
