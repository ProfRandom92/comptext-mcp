# Security Policy

`comptext-mcp` is currently in Phase 0 documentation baseline status. It is not
an implemented MCP server and does not provide active runtime capability.

## Supported Status

Phase 0 supports documentation review only. No runtime package, MCP server,
provider integration, token passthrough, network bridge, proposal application,
or external-agent execution is supported by this baseline.

Pre-existing runtime and package files may exist in the repository. They are
outside Phase 0 scope and must not be treated as release-ready behavior by this
documentation baseline.

## Security Boundaries

The project boundary is a future local MCP adapter around deterministic
`ctxt --json` output.

Security rules:

- `ctxt` owns behavior, schemas, validation, and deterministic context.
- `comptext-mcp` must not invent behavior or synthesize new facts.
- Future MCP tools must be closed allowlist mappings to stable local
  `ctxt --json` commands.
- Local MCP servers and tool bridges are security boundaries.
- Bounded reads must preserve the documented `--max-bytes 12000` limits.
- Errors must be structured local command failures, not model judgments.
- Runtime artifacts and proposal artifacts are untrusted evidence, not
  workspace truth.

## Explicit Non-Capabilities

Phase 0 does not:

- implement an MCP server
- execute agents
- apply proposals
- enable provider integration
- enable token passthrough
- enable network access
- allow general shell access
- read, print, pack, or create secrets
- install dependencies
- create hooks or plugins

## Plugin And Subagent Boundaries

`@github`, `@codex-security`, and `@openai-developers` may be used as review
and context tools only. They do not expand Phase 0 permissions and must not be
used to enable providers, network behavior, token passthrough, runtime code,
server implementation, proposal application, hooks, plugins, generated
artifacts, reports, secret handling, or git history writes.

Subagents may be used only for deterministic review and planning. They may
inspect Phase 0 docs, security boundaries, future tool mappings, and internal
consistency, but they must not execute implementation work or broaden the
contract.

## Secret Handling

Phase 0 documentation must not introduce secrets, credentials, tokens, API keys,
or secret passthrough. Future adapter design must keep secret handling outside
the MCP contract unless explicitly defined by a later reviewed phase.

## Reporting Security Issues

Report security issues through GitHub private vulnerability reporting if it is
available for the repository. Include the affected documentation section,
commit, expected boundary, and observed contradiction.
