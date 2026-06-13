<div align="center">

# 🧩 comptext-mcp

### The deterministic **MCP contract layer** for exposing local `ctxt --json` results to MCP clients.

> **Models are providers. Context is the product.**

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.10-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](pyproject.toml)
[![Protocol: MCP](https://img.shields.io/badge/protocol-MCP-8A2BE2.svg?style=for-the-badge)](https://modelcontextprotocol.io)
[![Phase 0](https://img.shields.io/badge/phase-0%20·%20docs%20baseline-orange.svg?style=for-the-badge)](docs/ROADMAP.md)

[![CI](https://github.com/ProfRandom92/comptext-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ProfRandom92/comptext-mcp/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/badge/lint-ruff-D7FF64.svg?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![pydantic v2](https://img.shields.io/badge/pydantic-v2-E92063.svg?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Read-only default](https://img.shields.io/badge/default-read--only-success.svg)](SECURITY.md)
[![Deterministic](https://img.shields.io/badge/output-deterministic-1f6feb.svg)](#-cryptographic-determinism)
[![Hashing: SHA-256](https://img.shields.io/badge/hashing-SHA--256-000000.svg)](#-cryptographic-determinism)
[![No local LLM](https://img.shields.io/badge/local%20LLM-not%20required-blueviolet.svg)](ROADMAP.md)

</div>

---

> [!IMPORTANT]
> **Phase 0 is documentation-only.** This repository baseline does **not** implement a
> released MCP server, package runtime, provider integration, token passthrough, proposal
> application, network access, external-agent invocation, or general shell access.
> Pre-existing runtime and package files may be present, but they are **outside Phase 0
> scope** and are **not** treated as release-ready behavior by this documentation baseline.

---

## 📚 Table of Contents

- [Why comptext-mcp?](#-why-comptext-mcp)
- [Architecture at a Glance](#-architecture-at-a-glance)
- [Request Lifecycle](#-request-lifecycle-sequence)
- [Phase State Machine](#-phase-state-machine)
- [Cryptographic Determinism](#-cryptographic-determinism)
- [Tool ↔ Command Mapping Matrix](#-tool--command-mapping-matrix)
- [Capability Matrix](#-capability-matrix)
- [Trusted Command Surface](#-trusted-command-surface)
- [Security Boundaries](#-security-boundaries)
- [Configuration Matrix](#-configuration-matrix)
- [Repository Map](#-repository-map)
- [Roadmap](#-roadmap)
- [Quick Start (future adapter)](#-quick-start-future-adapter)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Why comptext-mcp?

`comptext-mcp` is the **planned adapter** that lets MCP-aware agents (e.g. OpenCode) read
**deterministic, hash-verified context** produced by the CompText Rust CLI (`ctxt`) — without
ever letting the model invent facts, touch secrets, or run arbitrary shells.

```mermaid
mindmap
  root(("comptext-mcp"))
    Deterministic
      Stable file ordering
      SHA-256 manifests
      Reproducible packs
    Safe by default
      Read-only mode
      Secret-path exclusion
      Command timeouts
    Bridged
      ctxt is source of truth
      One-to-one tool mapping
      Closed allowlist
    Phase 0
      Docs baseline
      Contract first
      No runtime claims
```

**Design pillars**

| Pillar | What it means |
| :-- | :-- |
| 🧱 **`ctxt` is truth** | `ctxt` owns behavior, schemas, validation, and deterministic context. |
| 🔌 **Adapter, not author** | `comptext-mcp` must **not** invent behavior or synthesize new facts. |
| 🎯 **One-to-one mapping** | Every future MCP tool maps to exactly one stable `ctxt --json` command. |
| 🔒 **Closed allowlist** | Only documented commands are reachable. No general shell access. |
| 🧾 **Untrusted evidence** | Runtime & proposal artifacts are evidence — never workspace truth. |

---

## 🏛 Architecture at a Glance

```mermaid
flowchart LR
    subgraph CLIENT["🤖 MCP Client (OpenCode / agent)"]
        A["Tool call<br/>e.g. ctxt_self_report"]
    end

    subgraph ADAPTER["🧩 comptext-mcp (future adapter)"]
        direction TB
        B{"Closed<br/>allowlist?"}
        C["Map tool → 1 local command"]
        D["Enforce bounds<br/>--max-bytes 12000"]
        E["Structured result<br/>or structured failure"]
    end

    subgraph TRUTH["⚙️ ctxt — deterministic source of truth"]
        F["ctxt --json &lt;command&gt;"]
        G[("Schemas · Validation<br/>Deterministic context")]
    end

    A -->|MCP stdio| B
    B -- "denied" --> X["❌ Reject<br/>(not in contract)"]
    B -- "allowed" --> C --> D --> F
    F --> G --> E
    E -->|MCP response| A

    classDef truth fill:#0b3d2e,stroke:#1f6feb,color:#fff;
    classDef adapter fill:#1b1f3a,stroke:#8A2BE2,color:#fff;
    class TRUTH,F,G truth;
    class ADAPTER,B,C,D,E adapter;
```

The adapter is a **thin, auditable bridge**. It never reinterprets `ctxt` output, never
summarizes results into new facts, and never reaches outside the allowlist.

---

## 🔁 Request Lifecycle (Sequence)

```mermaid
sequenceDiagram
    autonumber
    participant U as 🤖 Agent
    participant M as 🧩 comptext-mcp
    participant P as 🛡 Policy / Allowlist
    participant C as ⚙️ ctxt CLI
    participant FS as 📁 Workspace

    U->>M: invoke tool (ctxt_proposals_inspect_latest)
    M->>P: validate against closed allowlist
    alt not allowlisted
        P-->>M: reject
        M-->>U: structured error (out of contract)
    else allowlisted
        P-->>M: ok + bounded args (--max-bytes 12000)
        M->>C: ctxt --json proposals inspect latest --max-bytes 12000
        C->>FS: read (read-only, secrets excluded)
        FS-->>C: bytes
        C-->>M: deterministic JSON (or structured failure)
        M-->>U: pass-through result (no new facts)
    end
```

---

## 🔀 Phase State Machine

```mermaid
stateDiagram-v2
    direction LR
    [*] --> Phase0
    Phase0: 📄 Phase 0 — Docs baseline
    Phase1: 🧪 Phase 1 — Adapter design review
    Phase2: 🛠 Phase 2 — Implementation review
    Phase3: 🔗 Phase 3 — Client integration review

    Phase0 --> Phase1: contract internally consistent
    Phase1 --> Phase2: every tool maps 1:1 to allowlist
    Phase2 --> Phase3: failures structured · ctxt stays truth
    Phase3 --> [*]: reviewed adapter exists

    note right of Phase0
        Current scope.
        No runtime claims.
    end note
```

---

## 🔐 Cryptographic Determinism

CompText context packs and replay digests are **content-addressed** with **SHA-256**. The
same workspace bytes always produce the same per-file digest and the same `manifest_sha256`,
giving you a tamper-evident, reproducible fingerprint of exactly what an agent saw.

```mermaid
flowchart TD
    A["📁 Walk workspace<br/>(recursive)"] --> B["🔤 Sort by stable<br/>relative POSIX path"]
    B --> C{"🚫 Secret-like<br/>or excluded path?"}
    C -- yes --> S["Skip<br/>(.env · *.pem · *.key · target/ · .git/ …)"]
    C -- no --> D["📏 Within byte budget?"]
    D -- no --> S
    D -- yes --> E["🔑 sha256(file_bytes)"]
    E --> F["📝 Append record<br/>{path, bytes, sha256}"]
    F --> G["📦 Canonical JSON manifest<br/>(sorted keys, compact)"]
    G --> H["🔒 manifest_sha256 = sha256(manifest)"]
    H --> I(["✅ Deterministic, verifiable pack"])

    classDef hash fill:#000,stroke:#39d353,color:#39d353;
    class E,H hash;
```

**Per-file digest**

$$\text{digest}_i = \mathrm{SHA\text{-}256}\big(\,\text{bytes}(file_i)\,\big)$$

**Manifest commitment** — over the canonical, sorted, compact JSON of every record:

$$\text{manifest\_sha256} = \mathrm{SHA\text{-}256}\Big(\;\mathrm{JSON}_{\text{sorted,compact}}\big(\{(path_i,\;bytes_i,\;digest_i)\}\big)\;\Big)$$

| Property | Guarantee |
| :-- | :-- |
| **Reproducibility** | Identical bytes → identical `manifest_sha256` across machines & runs. |
| **Tamper-evidence** | Any change to any file flips its digest and the manifest commitment. |
| **Stable ordering** | Files are sorted by relative POSIX path before hashing. |
| **Normalization** | `CRLF`/`CR` → `LF` for stable text payloads. |
| **Secret hygiene** | Secret-like paths are excluded *before* hashing (never enter the pack). |

> [!NOTE]
> SHA-256 here provides **integrity & reproducibility**, not confidentiality. It is a content
> fingerprint, not encryption.

---

## 🧮 Tool ↔ Command Mapping Matrix

Future MCP tools map **one-to-one** to a closed allowlist of stable local commands:

| 🧩 Future MCP tool | ⚙️ Underlying local command |
| :-- | :-- |
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

**Mapping rules**

- Each MCP tool maps to **exactly one** local command.
- The future adapter uses a **closed allowlist**.
- Bounded reads keep `--max-bytes 12000`.
- Errors are **structured local command failures**, not model judgments.

```mermaid
quadrantChart
    title Tool surface — determinism vs. read sensitivity
    x-axis "Lightweight read" --> "Bounded heavy read"
    y-axis "Inspect" --> "Validate"
    quadrant-1 "Bounded · Validate"
    quadrant-2 "Light · Validate"
    quadrant-3 "Light · Inspect"
    quadrant-4 "Bounded · Inspect"
    "self_report": [0.18, 0.30]
    "schema": [0.22, 0.20]
    "capabilities": [0.25, 0.25]
    "proposals_list": [0.30, 0.35]
    "proposals_inspect": [0.78, 0.30]
    "proposals_validate": [0.40, 0.80]
    "validate_run": [0.35, 0.88]
    "agent_discover": [0.28, 0.40]
    "runs_list": [0.32, 0.38]
    "runs_read_latest": [0.80, 0.34]
```

---

## ✅ Capability Matrix

| Capability | Phase 0 status |
| :-- | :--: |
| Documentation & contract baseline | ✅ In scope |
| Closed-allowlist tool **design** | ✅ In scope |
| Released MCP server runtime | ❌ Out of scope |
| Provider integration | ❌ Out of scope |
| Token passthrough | ❌ Out of scope |
| Network access | ❌ Out of scope |
| Proposal application | ❌ Out of scope |
| External-agent invocation | ❌ Out of scope |
| General shell access | ❌ Out of scope |
| Dependency installation by the baseline | ❌ Out of scope |
| Generated reports / artifacts | ❌ Out of scope |

---

## 📜 Trusted Command Surface

Future MCP tools may **only** wrap these stable local commands:

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

Unsupported `ctxt` commands are **not** part of the Phase 0 MCP contract.

---

## 🛡 Security Boundaries

```mermaid
graph TD
    subgraph SAFE["🟢 Inside the boundary"]
        A1["Read-only by default"]
        A2["Closed allowlist of commands"]
        A3["Bounded reads (--max-bytes 12000)"]
        A4["Secret-like paths excluded"]
        A5["Every external command has a timeout"]
    end
    subgraph DENY["🔴 Never crosses the boundary"]
        B1["Provider calls / network"]
        B2["Token passthrough / secrets"]
        B3["Proposal application"]
        B4["Arbitrary shell / chaining"]
        B5["External-agent invocation"]
    end
    SAFE -. "enforced by policy + contract" .-> DENY

    classDef ok fill:#0b3d2e,stroke:#39d353,color:#fff;
    classDef no fill:#3d0b0b,stroke:#ff6b6b,color:#fff;
    class SAFE,A1,A2,A3,A4,A5 ok;
    class DENY,B1,B2,B3,B4,B5 no;
```

- `ctxt` owns behavior, schemas, validation, and deterministic context.
- Local MCP servers and tool bridges are **security boundaries**, not general shell access.
- Runtime & proposal artifacts are **untrusted evidence**, not workspace truth.
- See [`SECURITY.md`](SECURITY.md) for the full policy and reporting process.

---

## ⚙️ Configuration Matrix

Environment variables that the future adapter is designed to honor:

| Variable | Default | Purpose |
| :-- | :-- | :-- |
| `CTXT_WORKDIR` | current dir | Target workspace to analyze (the Rust project, **not** this repo). |
| `CTXT_BIN` | `ctxt` | Path to the CompText Rust CLI (or rely on `PATH`). |
| `CTXT_MCP_READ_ONLY` | `1` | `1` = read-only (recommended). `0` enables write-capable mode. |
| `CTXT_TIMEOUT_SECS` | `30` | Per-command timeout, clamped to `1..=300`. |

Example OpenCode stdio config lives in
[`examples/opencode.windows.json`](examples/opencode.windows.json) and
[`examples/opencode.unix.json`](examples/opencode.unix.json).

---

## 🗂 Repository Map

```text
comptext-mcp/
├── 📄 README.md            ← you are here
├── 📄 PROJEKT.md           ← Phase 0 autonomy contract
├── 📄 SECURITY.md          ← security boundaries & reporting
├── 📄 ROADMAP.md           ← product roadmap
├── 📄 CONTRIBUTING.md      ← contributor guide
├── 📁 docs/
│   ├── ARCHITECTURE.md     ← adapter role & trust boundaries
│   ├── CONTRACTS.md        ← future MCP mapping contract
│   ├── ROADMAP.md          ← phased roadmap
│   └── OPEN_CODE_SETUP.md  ← OpenCode connection guide
├── 📁 examples/            ← OpenCode stdio config samples
├── 📁 scripts/             ← wheel build / install helpers
├── 📁 src/comptext_mcp/    ← runtime files (⚠ outside Phase 0 scope)
└── 📁 tests/               ← import & policy smoke tests
```

```mermaid
pie showData
    title Documentation-first repository
    "Docs & contracts" : 7
    "Runtime (out of scope)" : 6
    "Examples & scripts" : 5
    "Tests" : 3
```

---

## 🗺 Roadmap

```mermaid
timeline
    title comptext-mcp delivery phases
    section Now
        Phase 0 · Docs baseline : PROJEKT.md : README : SECURITY : docs/*
    section Next
        Phase 1 · Adapter design review : 1:1 tool mapping : bounded reads : structured failures
    section Later
        Phase 2 · Implementation review : stays inside reviewed contract
        Phase 3 · Client integration review : documented client config only
```

Product milestones (see [`ROADMAP.md`](ROADMAP.md)):

```mermaid
gitGraph
    commit id: "v0 docs"
    branch v0.1.0
    checkout v0.1.0
    commit id: "OpenCode bridge"
    commit id: "context pack + replay"
    checkout main
    merge v0.1.0 tag: "v0.1.0"
    branch v0.2.0
    commit id: "Rust workspace support"
    checkout main
    merge v0.2.0 tag: "v0.2.0"
    branch v0.3.0
    commit id: "release bundle + checksums"
    checkout main
    merge v0.3.0 tag: "v0.3.0"
```

**Every roadmap item must preserve:** no local LLM requirement · no model downloads ·
read-only default · deterministic output where practical · clear audit trail.

---

## 🚀 Quick Start (future adapter)

> [!WARNING]
> The steps below describe the **intended** future adapter workflow. Phase 0 does not ship a
> released runtime — treat this as design documentation. See [`docs/OPEN_CODE_SETUP.md`](docs/OPEN_CODE_SETUP.md).

**1. Install (from repo root)**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install .
```

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install .
```

**2. Point at `ctxt` and your workspace**

```json
{
  "CTXT_WORKDIR": "C:/path/to/your/rust-project",
  "CTXT_BIN": "C:/path/to/ctxt.exe",
  "CTXT_MCP_READ_ONLY": "1",
  "CTXT_TIMEOUT_SECS": "30"
}
```

**3. Verify in OpenCode** — the server is designed to expose deterministic, read-only tools
that bridge to `ctxt`. See the setup guide for troubleshooting.

---

## 🤝 Contributing

Contributions are welcome — please keep the bridge **small, inspectable, and deterministic**.

- Default mode stays **read-only**.
- **No** local LLM dependency, model downloads, secrets in packs, or arbitrary shell execution.
- Every external command must have a **timeout**.
- Prefer one focused tool over one large multi-mode tool.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
before opening a PR.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE).

<div align="center">
<br/>

**`ctxt` is the deterministic source of truth — `comptext-mcp` is the bridge.**

<sub>Models are providers. Context is the product.</sub>

</div>
