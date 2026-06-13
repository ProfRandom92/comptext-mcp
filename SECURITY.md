# Security Policy

CompText MCP is a bridge between an MCP client, a local workspace, and external command-line tools such as `ctxt` and Rust tooling.

Security and determinism are core project goals.

## Supported versions

The initial supported version is:

| Version | Supported |
| --- | --- |
| 0.1.x | yes |

## Report a vulnerability

Please use GitHub private vulnerability reporting if available. If not, contact the repository owner through GitHub.

Include:

- affected version or commit
- operating system
- OpenCode version if relevant
- minimal reproduction steps
- expected behavior
- actual behavior

## Security boundaries

The project should not:

- execute arbitrary shell strings
- include secrets in context packs
- download model weights during install
- require local LLM services
- run write actions by default
- publish, upload, or push without explicit user action

## Secret handling

Context packing must exclude common secret and build directories, including:

- `.env`
- `.env.*`
- private keys and certs
- `.git/`
- `target/`
- `node_modules/`
- `dist/`
- `build/`

## Safe default

`CTXT_MCP_READ_ONLY=1` is the recommended default for OpenCode and collaborator setups.
