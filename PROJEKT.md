# PROJEKT.md - comptext-mcp Phase 0 Autonomy Contract

## Project Identity

Repository: `ProfRandom92/comptext-mcp`

`comptext-mcp` is the planned MCP contract layer for exposing deterministic local `ctxt --json` results to MCP clients.

Core principle:

> Models are providers. Context is the product.

Architecture rules:

- `ctxt` is the deterministic source of truth.
- `comptext-mcp` must not invent behavior.
- Future MCP tools must map one-to-one to stable local `ctxt --json` commands.
- Phase 0 is documentation-only.

## Phase 0 Scope

Phase 0 exists to create a documentation and contract baseline only.

Allowed Phase 0 file tree:

```text
PROJEKT.md
README.md
.gitignore
SECURITY.md
docs/ARCHITECTURE.md
docs/CONTRACTS.md
docs/ROADMAP.md
```

No other files or directories are in scope for autonomous Phase 0 work.

Existing runtime and package files may already be present in the repository.
They are outside Phase 0 scope. Phase 0 documentation must not treat those
pre-existing files as complete, release ready, supported runtime behavior, or a
reason to broaden the documentation contract.

## Autonomy Boundaries

An agent may autonomously:

- Create and edit only the allowed Phase 0 documentation files.
- Create the `docs/` directory if it is missing.
- Keep documentation internally consistent.
- Fix wording that contradicts the safety boundaries in this file.
- Run local sanity checks listed in this file.

An agent must preserve these rules across all docs:

- `ctxt` owns behavior, schemas, validation, and deterministic context.
- `comptext-mcp` is a future adapter only.
- Future MCP tools are allowlisted one-to-one mappings to stable local `ctxt --json` commands.
- Local MCP servers and tool bridges are a security boundary.
- Runtime artifacts and proposal artifacts are untrusted evidence, not workspace truth.

## Plugin Policy

This repository may use the following plugins as review and context tools
during Phase 0:

- `@github`
- `@codex-security`
- `@openai-developers`

Plugin use does not expand Phase 0 permissions.

Allowed plugin roles:

- `@github` may provide repository, file, and status awareness only.
- `@codex-security` may review Phase 0 documentation for risky claims, token
  handling, broad tool permissions, hidden execution paths, and MCP security
  boundary issues.
- `@openai-developers` may help align documentation with Codex and OpenAI
  developer guidance without changing the Phase 0 boundary.

Plugins must not be treated as permission to:

- Create runtime code.
- Create package scaffolding.
- Create an MCP server implementation.
- Use network.
- Call providers.
- Add token passthrough.
- Read, print, pack, or create secrets.
- Invoke Codex CLI.
- Invoke Antigravity CLI.
- Invoke external agents.
- Apply proposals.
- Create hooks.
- Create plugins.
- Create `reports/`.
- Create generated artifacts.
- Run `git add`.
- Run `git commit`.
- Run `git push`.
- Run `git pull`.

## Subagent Policy

Subagents may be used only for deterministic review and planning within the
Phase 0 documentation boundary.

Subagents may inspect:

- Phase 0 documentation files.
- Security boundaries.
- Future MCP tool mappings.
- Internal consistency across the allowed docs.

Subagents must not:

- Create runtime code.
- Create package scaffolding.
- Create an MCP server implementation.
- Use network.
- Call providers.
- Add token passthrough.
- Read, print, pack, or create secrets.
- Invoke Codex CLI.
- Invoke Antigravity CLI.
- Invoke external agents.
- Apply proposals.
- Create hooks.
- Create plugins.
- Create `reports/`.
- Create generated artifacts.
- Run `git add`.
- Run `git commit`.
- Run `git push`.
- Run `git pull`.

## Forbidden Actions

An agent must not:

- Create runtime code.
- Create package scaffolding.
- Create an MCP server implementation.
- Create `reports/`.
- Create generated artifacts.
- Install dependencies.
- Use network.
- Call providers.
- Add token passthrough.
- Read, print, pack, or create secrets.
- Invoke Codex CLI.
- Invoke Antigravity CLI.
- Invoke external agents.
- Apply proposals.
- Create hooks.
- Create plugins.
- Run `git add`.
- Run `git commit`.
- Run `git push`.
- Run `git pull`.
- Execute arbitrary shell commands beyond the local sanity checks in this file.

## Trusted Local `ctxt` Command Surface

These are the only local `ctxt` commands Phase 0 documentation may reference as the trusted future command surface:

```text
ctxt --json self report
ctxt --json schema
ctxt --json capabilities
ctxt --json proposals list
ctxt --json proposals inspect latest --max-bytes 12000
ctxt --json proposals inspect --id latest --max-bytes 12000
ctxt --json proposals validate latest
ctxt --json proposals validate --id latest
ctxt --json validate --run
ctxt --json agent discover
ctxt --json runs list
ctxt --json runs read latest --max-bytes 12000
```

Do not document unsupported `ctxt` commands as part of the Phase 0 MCP contract.

## Planned MCP Tool Mapping

Future MCP tools must map exactly as follows:

| MCP tool | Underlying local command |
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

Mapping rules:

- Each MCP tool maps to exactly one local command.
- The future adapter must use a closed allowlist.
- Bounded reads must keep `--max-bytes 12000`.
- Errors are structured local command failures, not model judgments.
- The adapter must not reinterpret, summarize into new facts, or synthesize behavior beyond `ctxt`.

## Validation And Sanity Checks

Allowed local sanity checks:

```powershell
git --no-pager status --short --branch
Get-ChildItem -Recurse
Select-String
```

Use `Select-String` to search documentation for forbidden claims that imply active runtime capability:

```text
production ready
executes agents
applies proposals
provider integration enabled
token passthrough enabled
network enabled
MCP server implemented
arbitrary shell execution
```

If a forbidden claim appears in Phase 0 docs, fix the wording so it clearly states the capability is not implemented or is out of scope.

## Stop Conditions

Stop and ask the user before:

- Adding code.
- Adding dependencies.
- Creating server implementation.
- Enabling network.
- Adding provider integration.
- Adding token passthrough.
- Adding proposal apply.
- Invoking external agents.
- Running git write commands.
- Changing repository scope beyond Phase 0 docs.
- Creating files or directories outside the allowed Phase 0 file tree.

## Return Requirements

When completing autonomous Phase 0 documentation work, return:

- Created or changed files.
- Summary.
- Sanity checks run.
- Git status.
- Limitations.

If local command execution fails with `CreateProcessAsUserW failed: 5`, report that limitation and rely on user-run external PowerShell validation.
