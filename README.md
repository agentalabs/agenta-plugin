# Agenta Plugin

Modular MCP plugin collection for Claude Code. Pick a profile, get a curated set of MCP servers and skills optimized for your workflow.

Built by [Kaue Cano](https://github.com/agenta-labs).

---

## Quick Start

```bash
# Option 1: Interactive installer (defaults to "full" profile)
bash install.sh /path/to/your/project

# Option 2: Copy a template directly
cp templates/core.mcp.json /path/to/your/project/.mcp.json

# Option 3: Specify profile as argument
bash install.sh /path/to/your/project research
```

> **Note**: If you cloned this repo, run `git submodule update --init --recursive` to fetch external skill repos (Solana Foundation, SendAI, Trail of Bits, Cloudflare, Superpowers).

---

## Profiles

| Profile | Use Case | MCP Servers | Key Tools |
|---------|----------|-------------|-----------|
| **core** | Any project | 3 | Sandbox, memory graph, context mode |
| **knowledge-base** | RAG, document management | 12 | Vector search, scraping, memsearch, Supabase, Postgres |
| **research** | Analysis, reports | 11 | Multi-engine search, scraping, academic papers, memsearch, Notion |
| **web-dev** | Full-stack development | 12 | Browser automation, scraping, memsearch, Supabase, Postgres |
| **blockchain** | Solana development | 11 | Helius, Jupiter docs, memsearch, context7, Twitter |
| **full** | Everything | 21 | All MCP servers combined |

See [docs/profiles.md](docs/profiles.md) for detailed profile descriptions and [docs/guide.md](docs/guide.md) for end-to-end user flows.

---

## MCP Servers (21)

| Server | Purpose | Profiles |
|--------|---------|----------|
| **e2b** | Cloud sandbox (TS/Python) | all |
| **memorygraph** | Knowledge graph | all |
| **context-mode** | Context window management (98% token reduction) | all |
| **claude-context** | Vector search + code semantics | kb, blockchain |
| **qdrant** | Vector database | kb |
| **sqlite** | Local database | kb |
| **supabase** | Supabase (DB, auth, storage) | kb, web-dev |
| **postgres** | Direct PostgreSQL access | kb, web-dev |
| **mcpdoc** | llms.txt documentation | kb, research, web-dev, blockchain |
| **crawl4ai** | Web scraping | kb, research, web-dev |
| **omnisearch** | Tavily/Exa/Perplexity | research, web-dev, blockchain |
| **context7** | Live library docs | research, web-dev, blockchain |
| **notion** | Notion integration | research |
| **consensus** | Academic paper search (200M+ papers) | research |
| **puppeteer** | Headless browser | research, web-dev |
| **daytona** | Container sandbox | web-dev, blockchain |
| **helius** | Solana blockchain | blockchain |
| **twitter** | Twitter/X automation | blockchain |
| **memsearch** | Persistent memory with hybrid search | kb, research, web-dev, blockchain |
| **skill-seekers** | Source-to-knowledge ingestion | kb |
| **clickup** | Task management | full |

See [docs/mcp-catalog.md](docs/mcp-catalog.md) for setup details.

---

## Skills (8)

### Internal Skills

| Skill | Description | Profiles |
|-------|-------------|----------|
| **autonomous-agent** | Task decomposition, memory, self-correction | all |
| **knowledge-base** | RAG patterns, ingestion workflows | kb |
| **research** | Multi-source search, synthesis | research |

### External Skills (Submodules)

| Skill | Source | Description | Profiles |
|-------|--------|-------------|----------|
| **solana-foundation** | [Solana Foundation](https://github.com/solana-foundation/solana-dev-skill) | @solana/kit, Anchor, Pinocchio, LiteSVM, Codama | blockchain |
| **solana-ecosystem** | [SendAI](https://github.com/sendaifun/skills) | Jupiter, Drift, Raydium, Orca, 30+ DeFi protocols | blockchain |
| **security** | [Trail of Bits](https://github.com/trailofbits/skills) | Static analysis, Semgrep, supply chain, secure contracts | blockchain |
| **cloudflare** | [Cloudflare](https://github.com/cloudflare/skills) | Workers, Durable Objects, Wrangler, Agents SDK | web-dev |
| **superpowers** | [obra/superpowers](https://github.com/obra/superpowers) | TDD, debugging, code review, planning, git worktrees | web-dev |

---

## Project Structure

```
agenta-plugin/
├── profiles/          # Profile manifests (which MCPs + skills)
├── mcps/              # Individual MCP server configs
├── skills/            # Skill files and submodules
│   ├── *.md           # Internal skills
│   ├── SKILL.md       # Merged skill index
│   ├── solana-foundation/  # Submodule: Solana Foundation
│   ├── sendai/             # Submodule: SendAI
│   ├── trailofbits/        # Submodule: Trail of Bits
│   ├── cloudflare/         # Submodule: Cloudflare
│   └── superpowers/        # Submodule: Superpowers
├── templates/         # Ready-to-copy .mcp.json files
├── docs/              # Extended documentation
├── install.sh         # Profile installer script
├── CLAUDE.md          # Agent instructions template
├── plugin.json        # Plugin metadata
└── marketplace.json   # Plugin registry entry
```

---

## Environment Variables

Each profile requires different API keys. See [docs/env-vars.md](docs/env-vars.md) for the full reference.

**Minimum for each profile:**

| Profile | Required Keys |
|---------|--------------|
| core | `E2B_API_KEY` |
| knowledge-base | `E2B_API_KEY`, `OPENAI_API_KEY` (+ optional: `SUPABASE_URL`, `POSTGRES_URL`) |
| research | `E2B_API_KEY`, `TAVILY_API_KEY` |
| web-dev | `E2B_API_KEY` (+ optional: `SUPABASE_URL`, `POSTGRES_URL`) |
| blockchain | `E2B_API_KEY`, `HELIUS_API_KEY`, `OPENAI_API_KEY` |

---

## How It Works

1. **Choose a profile** that matches your project type
2. **Run the installer** or copy a template `.mcp.json`
3. **Set environment variables** for the MCP servers you want to use
4. **Start Claude Code** — MCP servers and skills are automatically available

The installer copies:
- `.mcp.json` — MCP server configuration for Claude Code
- `skills/` — Relevant skill files and submodule directories for your profile
- `skills/SKILL.md` — Generated index of all installed skills
- `CLAUDE.md` — Agent instructions (if not already present)

---

## Submodules

External skills are tracked as git submodules. To update to latest upstream:

```bash
git submodule update --remote
```

If submodules are not initialized, the installer will attempt to init them automatically. If that fails (e.g., no git access), it will warn but continue — internal skills will still work.

---

## Customization

### Adding MCP sources to mcpdoc

The `mcpdoc` server supports custom llms.txt URLs. Edit your `.mcp.json` to add `--urls` arguments:

```json
"mcpdoc": {
  "command": "uvx",
  "args": [
    "--from", "mcpdoc", "mcpdoc",
    "--urls", "MyDocs:https://example.com/llms.txt"
  ]
}
```

### Creating a custom profile

1. Copy an existing `profiles/*.json`
2. Modify the `mcps` and `skills` arrays
3. Save as `profiles/my-profile.json`
4. Create a matching `templates/my-profile.mcp.json`

---

## License

MIT License — see [LICENSE](LICENSE)

---

## Links

- [Agenta Labs](https://github.com/agenta-labs/agenta-plugin)
- [Claude Code](https://claude.ai/code)
- [MCP Protocol](https://modelcontextprotocol.io)
