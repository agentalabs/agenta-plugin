# Agenta - Complete Solana Development Stack for Claude Code

> **One plugin. Everything you need for Solana development.**

Agenta bundles 9 MCP servers, 8 plugins, 3 llms.txt endpoints, specialized skills, and agents into a single installable package for Claude Code. Built by [Superteam Brasil](https://superteam.fun).

---

## 🚀 Quick Start

```bash
# Add the marketplace
/plugin marketplace add superteam-brasil/agenta

# Install Agenta
/plugin install agenta@superteam-brasil

# Run setup wizard
/agenta:setup
```

---

## 📦 What's Included

### MCP Servers (9)

| Server | Purpose | Free Tier |
|--------|---------|-----------|
| **E2B** | Cloud sandbox (TS/Python) | ✅ |
| **Daytona** | Sandbox (Rust/full env) | ✅ |
| **Omnisearch** | Unified search (Tavily, Exa, Perplexity) | ⚠️ Mixed |
| **Helius** | Solana blockchain data | ✅ 1M credits |
| **MemoryGraph** | Knowledge graph (SQLite/Neo4j) | ✅ |
| **Twitter/X** | Social media automation | ❌ Paid |
| **Crawl4AI** | Web scraping (self-hosted) | ✅ FREE |
| **mcpdoc** | llms.txt docs (Solana, Helius, Jupiter) | ✅ |
| **Claude Context** | Vector search + code semantics | ✅ |

### Plugins (8)

| Plugin | Source | Purpose |
|--------|--------|---------|
| **Context7** | anthropics/claude-plugins-official | Live docs lookup |
| **GitHub** | anthropics/claude-plugins-official | Repo management |
| **Chrome DevTools** | anthropics/claude-plugins-official | Browser debugging |
| **Playwright** | anthropics/claude-plugins-official | Browser automation |
| **Firecrawl** | anthropics/claude-plugins-official | AI web scraping |
| **Trail of Bits** | trailofbits/skills | Security auditing |
| **Compound Engineering** | EveryInc/compound-engineering-plugin | 29 agents |
| **ClickUp** | pvoo/clickup-mcp (ClawHub) | Task management |

### Documentation Endpoints

- `https://solana.com/llms.txt` - Core Solana docs
- `https://www.helius.dev/llms.txt` - Helius RPC/APIs
- `https://dev.jup.ag/llms.txt` - Jupiter DEX

---

## 🛠️ Commands

| Command | Description |
|---------|-------------|
| `/agenta:setup` | Interactive setup wizard for API keys |
| `/agenta:status` | Check MCP server connections |
| `/agenta:audit` | Run security audit on Solana programs |
| `/agenta:index` | Index codebase with Claude Context |
| `/agenta:docs <topic>` | Fetch documentation via mcpdoc |

---

## 📋 Skills

### `solana-development`
Best practices for Anchor, Metaplex, DeFi development. Auto-applies to `.rs`, `Anchor.toml`, `.ts` files.

### `blockchain-security`
Security checklist integration with Trail of Bits scanners. Covers integer overflow, signer validation, PDA security.

---

## 🤖 Agents

### `solana-auditor`
Specialized security agent that:
- Runs Trail of Bits Solana scanner
- Checks for common vulnerabilities
- Generates audit reports

### `project-scaffolder`
Creates new Solana projects with:
- Anchor boilerplate
- TypeScript client setup
- Testing configuration
- CI/CD templates

---

## ⚙️ Configuration

After installation, configure API keys in `~/.claude/.credentials.json` or via environment variables:

```bash
export E2B_API_KEY="..."
export HELIUS_API_KEY="..."
export TAVILY_API_KEY="..."
export OPENAI_API_KEY="..."  # For Claude Context embeddings
export ZILLIZ_API_KEY="..."  # For vector storage
```

Or run `/agenta:setup` for guided configuration.

---

## 🔒 Permissions

Agenta requests these permissions:

```
Allow: anchor *, cargo *, solana *, npm run *, pnpm *, git *, docker *
Deny: .env, .env.*, secrets/**, *key*.json
```

---

## 📊 Stack Summary

| Category | Count |
|----------|-------|
| MCP Servers | 9 |
| Plugins | 8 |
| llms.txt Endpoints | 3 |
| Skills | 2 |
| Agents | 2 |
| Commands | 5 |
| **Total Components** | **29** |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Submit PR with tests

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🔗 Links

- [Superteam Brasil](https://superteam.fun)
- [Claude Code Docs](https://code.claude.com)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Solana Docs](https://solana.com/docs)
