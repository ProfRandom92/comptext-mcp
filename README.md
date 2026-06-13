# comptext-mcp

`comptext-mcp` is the planned MCP contract layer for exposing deterministic
local `ctxt --json` results to MCP clients.

Phase 0 is documentation-only. This repository baseline does not implement an
MCP server, package runtime, provider integration, token passthrough, proposal
application, network access, external-agent invocation, or general shell access.
Pre-existing runtime and package files may be present in the repository, but
they are outside Phase 0 scope and are not treated as release-ready behavior by
this documentation baseline.

Core principle:

> Models are providers. Context is the product.

## Architecture Position

- `ctxt` is the deterministic source of truth.
- `ctxt` owns behavior, schemas, validation, and deterministic context.
- `comptext-mcp` must not invent behavior.
- `comptext-mcp` is a future adapter only.
- Future MCP tools must map one-to-one to stable local `ctxt --json` commands.
- Runtime artifacts and proposal artifacts are untrusted evidence, not
  workspace truth.

## Phase 0 Scope

Phase 0 creates the documentation and contract baseline only:

- `PROJEKT.md`
- `README.md`
- `.gitignore`
- `SECURITY.md`
- `docs/ARCHITECTURE.md`
- `docs/CONTRACTS.md`
- `docs/ROADMAP.md`

No runtime code, package scaffolding, server implementation, generated reports,
hooks, plugins, dependencies, provider calls, proposal application, or general
shell access are part of Phase 0.

## Review Tool Policy

`@github`, `@codex-security`, and `@openai-developers` may be used only as
review and context tools for Phase 0 documentation. They do not grant
permission to create runtime code, call providers, enable network behavior,
create server implementation, add token passthrough, create hooks or plugins,
invoke external agents, apply proposals, or write git history.

Subagents, if used, are limited to deterministic review and planning over Phase
0 docs, security boundaries, tool mappings, and consistency.

## Trusted Future Command Surface

Future MCP tools may only wrap these stable local commands:

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

Unsupported `ctxt` commands are not part of the Phase 0 MCP contract.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Contracts](docs/CONTRACTS.md)
- [Roadmap](docs/ROADMAP.md)
- [Security](SECURITY.md)
