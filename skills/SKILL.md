# Skills Index

Single source of truth for all available skills — internal and external (submodule-based).

## Internal Skills

These are maintained directly in this repository.

| Skill Name | File | Description |
|------------|------|-------------|
| `autonomous-agent` | [./autonomous-agent.md](./autonomous-agent.md) | Task decomposition, memory, self-correction, multi-step workflows |
| `knowledge-base` | [./knowledge-base.md](./knowledge-base.md) | RAG pipelines, ingestion, vector search, source registry, automated sync |
| `research` | [./research.md](./research.md) | Multi-source search, synthesis, academic papers, cross-session memory |

## External Skills (Submodules)

These are tracked as git submodules. Update with `git submodule update --remote`.

### Solana Foundation (`solana-foundation`)

Comprehensive Solana development skill covering @solana/kit v5.x, Anchor, Pinocchio, LiteSVM, Mollusk, Surfpool, Codama, and security patterns.

| Module | Path |
|--------|------|
| Main Skill | [./solana-foundation/skill/SKILL.md](./solana-foundation/skill/SKILL.md) |
| Reference Modules | [./solana-foundation/skill/references/](./solana-foundation/skill/references/) |

**Profile mapping**: `solana-foundation` skill name maps to the `skills/solana-foundation/` directory.

### SendAI — Solana Ecosystem (`sendai`)

DeFi protocol integrations for Jupiter, Drift, Raydium, Orca, Meteora, and 30+ other Solana ecosystem tools.

| Module | Path |
|--------|------|
| Skills Directory | [./sendai/skills/](./sendai/skills/) |

Key integrations: Jupiter, Drift, Raydium, Orca, Meteora, Helius, Phantom, Metaplex, PumpFun, Sanctum, Squads, and more.

**Profile mapping**: `solana-ecosystem` skill name maps to the `skills/sendai/` directory.

### Trail of Bits — Security (`trailofbits`)

Security audit skills: static analysis, Semgrep rules, supply chain risk, property-based testing, YARA authoring, and more.

| Module | Path |
|--------|------|
| Plugins Directory | [./trailofbits/plugins/](./trailofbits/plugins/) |

Key skills: `building-secure-contracts`, `semgrep-rule-creator`, `supply-chain-risk-auditor`, `static-analysis`, `variant-analysis`, `property-based-testing`, `yara-authoring`.

**Profile mapping**: `security` skill name maps to the `skills/trailofbits/` directory.

### Cloudflare (`cloudflare`)

Cloudflare Workers, Durable Objects, Wrangler, Agents SDK, and web performance patterns.

| Module | Path |
|--------|------|
| Skills Directory | [./cloudflare/skills/](./cloudflare/skills/) |

Key skills: `workers-best-practices`, `durable-objects`, `wrangler`, `agents-sdk`, `building-mcp-server-on-cloudflare`, `web-perf`.

**Profile mapping**: `cloudflare` skill name maps to the `skills/cloudflare/` directory.

### Superpowers (`superpowers`)

Methodology-focused development skill covering TDD, systematic debugging, code review, planning, git worktrees, subagent-driven development, and verification workflows.

| Module | Path |
|--------|------|
| Repository | [./superpowers/](./superpowers/) |

Key topics: test-driven development, systematic debugging, code review methodology, planning, git worktrees, subagent patterns, verification.

**Profile mapping**: `superpowers` skill name maps to the `skills/superpowers/` directory.

## Profile → Skill Mapping

| Profile | Skills |
|---------|--------|
| core | `autonomous-agent` |
| knowledge-base | `autonomous-agent`, `knowledge-base` |
| research | `autonomous-agent`, `research` |
| web-dev | `autonomous-agent`, `superpowers`, `cloudflare` |
| blockchain | `autonomous-agent`, `solana-foundation`, `solana-ecosystem`, `security` |
| full | All of the above |
