# Roadmap

## Phase 0: Documentation Baseline

Status: current scope.

Phase 0 establishes the documentation and contract baseline only.

Deliverables:

- project identity and autonomy boundaries in `PROJEKT.md`
- Phase 0 overview in `README.md`
- security boundaries in `SECURITY.md`
- architecture rules in `docs/ARCHITECTURE.md`
- future MCP mapping contract in `docs/CONTRACTS.md`
- phase roadmap in `docs/ROADMAP.md`

Phase 0 does not create runtime code, package scaffolding, server
implementation, generated reports, hooks, plugins, dependencies, provider
integration, token passthrough, proposal application, network access, or
external-agent invocation.

Pre-existing runtime and package files may already be present in the
repository. They remain outside Phase 0 scope and are not treated as
release-ready behavior by this documentation baseline.

Review plugins may provide context or documentation review only. Subagents may
perform deterministic review and planning only, limited to Phase 0 docs,
security boundaries, future tool mappings, and internal consistency.

## Future Phase 1: Adapter Design Review

Future work may design an MCP adapter that maps one-to-one to the documented
stable local `ctxt --json` command surface.

Entry criteria:

- Phase 0 contract remains internally consistent.
- Every proposed MCP tool maps to exactly one allowlisted local command.
- Bounded reads preserve `--max-bytes 12000`.
- Failure handling is structured local command failure.
- `ctxt` remains the deterministic source of truth.

## Future Phase 2: Implementation Review

Future implementation work, if authorized by a later phase, must remain inside
the reviewed contract. It must not add unsupported commands, provider calls,
token passthrough, proposal application, network behavior, general shell
access, hooks, plugins, or external-agent invocation without a new reviewed
contract.

## Future Phase 3: Client Integration Review

Future client integration work may document client configuration only after an
adapter exists and has been reviewed. Client docs must not imply capabilities
that are not implemented by the reviewed adapter contract.
