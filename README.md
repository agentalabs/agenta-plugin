# Agenta Plugin

Modular MCP plugin collection for Claude Code. Pick a profile, get a curated set of MCP servers and skills optimized for your workflow.

Built by [Superteam Brasil](https://superteam.fun).

---

## Quick Start

```bash
# Option 1: Interactive installer
bash install.sh /path/to/your/project

# Option 2: Copy a template directly
cp templates/core.mcp.json /path/to/your/project/.mcp.json

# Option 3: Specify profile as argument
bash install.sh /path/to/your/project research
```

---

## Profiles

| Profile | Use Case | MCP Servers | Key Tools |
|---------|----------|-------------|-----------|
| **core** | Any project | 4 | Sandbox, memory, reasoning, HTTP |
| **knowledge-base** | RAG, document management | 12 | Vector search, file ops, scraping, Supabase, Postgres |
| **research** | Analysis, reports | 10 | Multi-engine search, scraping, Notion |
| **web-dev** | Full-stack development | 12 | Browser automation, testing, Supabase, Postgres |
| **blockchain** | Solana development | 10 | Helius, Jupiter docs, Twitter |
| **full** | Everything | 21 | All MCP servers combined |

See [docs/profiles.md](docs/profiles.md) for detailed profile descriptions and [docs/guide.md](docs/guide.md) for end-to-end user flows.

---

## MCP Servers (21)

| Server | Purpose | Profiles |
|--------|---------|----------|
| **e2b** | Cloud sandbox (TS/Python) | all |
| **memorygraph** | Knowledge graph | all |
| **sequential-thinking** | Structured reasoning | all |
| **fetch** | HTTP requests | all |
| **claude-context** | Vector search + code semantics | kb, blockchain |
| **qdrant** | Vector database | kb |
| **filesystem** | File operations | kb |
| **sqlite** | Local database | kb |
| **supabase** | Supabase (DB, auth, storage) | kb, web-dev |
| **postgres** | Direct PostgreSQL access | kb, web-dev |
| **mcpdoc** | llms.txt documentation | kb, research, web-dev, blockchain |
| **crawl4ai** | Web scraping | kb, research |
| **omnisearch** | Tavily/Exa/Perplexity | research, web-dev, blockchain |
| **context7** | Live library docs | research, web-dev |
| **notion** | Notion integration | research |
| **playwright-mcp** | Browser automation | web-dev |
| **puppeteer** | Headless browser | research, web-dev |
| **daytona** | Container sandbox | web-dev, blockchain |
| **helius** | Solana blockchain | blockchain |
| **twitter** | Twitter/X automation | blockchain |
| **clickup** | Task management | full |

See [docs/mcp-catalog.md](docs/mcp-catalog.md) for setup details.

---

## Skills (5)

| Skill | Description | Profiles |
|-------|-------------|----------|
| **autonomous-agent** | Task decomposition, memory, self-correction | all |
| **knowledge-base** | RAG patterns, ingestion workflows | kb |
| **research** | Multi-source search, synthesis | research |
| **web-development** | Framework-agnostic web patterns | web-dev |
| **solana-development** | Anchor, Metaplex, DeFi | blockchain |

---

## Project Structure

```
agenta-plugin/
├── profiles/          # Profile manifests (which MCPs + skills)
├── mcps/              # Individual MCP server configs
├── skills/            # Skill markdown files
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
- `skills/*.md` — Relevant skill files for your profile
- `CLAUDE.md` — Agent instructions (if not already present)

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

- [Superteam Brasil](https://superteam.fun)
- [Claude Code](https://claude.ai/code)
- [MCP Protocol](https://modelcontextprotocol.io)
