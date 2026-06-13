# Architecture

`comptext-mcp` is the planned MCP contract layer for deterministic local
`ctxt --json` results.

Phase 0 is documentation-only. It defines boundaries and future contracts; it
does not create runtime code, package scaffolding, an MCP server, hooks,
plugins, provider integration, token passthrough, network access, or generated
artifacts.

Pre-existing runtime and package files may exist in the repository. They are
outside Phase 0 scope and are not evidence that the Phase 0 contract includes
implemented or release-ready runtime behavior.

## Source Of Truth

`ctxt` is the deterministic source of truth.

`ctxt` owns:

- behavior
- schemas
- validation
- deterministic context
- local command results

`comptext-mcp` must not invent behavior, reinterpret results into new facts, or
create an independent schema. The future adapter may expose only what stable
local `ctxt --json` commands return.

## Adapter Role

`comptext-mcp` is a future adapter only. Its role is to map MCP tool calls to a
closed allowlist of stable local `ctxt --json` commands.

Each future MCP tool must:

- map to exactly one local command
- use the documented command arguments exactly
- keep bounded read limits where documented
- return structured command output or structured command failure
- avoid model judgment as a source of truth

## Trust Boundaries

Local MCP servers and tool bridges are security boundaries. They must not be
treated as general shell access.

Runtime artifacts and proposal artifacts are untrusted evidence. They may be
read through documented bounded commands, but they are not workspace truth and
must not be applied by the Phase 0 contract.

Review plugins and subagents are also bounded by the Phase 0 contract.
`@github`, `@codex-security`, and `@openai-developers` may provide review or
context only. Subagents may review and plan against the docs, security
boundaries, and mappings, but must not create implementation artifacts or expand
the command surface.

## Non-Goals In Phase 0

Phase 0 does not implement:

- MCP server runtime
- package scaffolding
- provider calls
- network operations
- token passthrough
- proposal application
- general shell access
- external-agent invocation
- dependency installation
- generated reports
