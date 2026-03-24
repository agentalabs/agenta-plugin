# Profile Guide

Agenta Plugin organizes MCP servers and skills into **profiles** — curated configurations for different use cases.

## Available Profiles

### Core (`core`)
**For**: Any project needing baseline agent capabilities.
**MCPs**: e2b, memorygraph, sequential-thinking, fetch
**Skills**: autonomous-agent
**Required env**: `E2B_API_KEY`

### Knowledge Base (`knowledge-base`)
**For**: Building RAG pipelines, managing documents, vector search, automated maintenance.
**MCPs**: Core + claude-context, qdrant, filesystem, sqlite, mcpdoc, crawl4ai, supabase, postgres
**Skills**: autonomous-agent, knowledge-base
**Required env**: `E2B_API_KEY` (from core), `OPENAI_API_KEY`
**Optional env**: `ZILLIZ_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `POSTGRES_URL`

### Research (`research`)
**For**: Multi-source research, competitive analysis, report generation.
**MCPs**: Core + mcpdoc, crawl4ai, omnisearch, context7, notion, puppeteer
**Skills**: autonomous-agent, research
**Required env**: `E2B_API_KEY` (from core), `TAVILY_API_KEY`
**Optional env**: `EXA_API_KEY`, `PERPLEXITY_API_KEY`, `NOTION_TOKEN`

### Web Dev (`web-dev`)
**For**: Full-stack web development with testing, browser automation, and databases.
**MCPs**: Core + mcpdoc, omnisearch, context7, playwright-mcp, puppeteer, daytona, supabase, postgres
**Skills**: autonomous-agent, web-development
**Required env**: `E2B_API_KEY` (from core)
**Optional env**: `TAVILY_API_KEY`, `EXA_API_KEY`, `PERPLEXITY_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `POSTGRES_URL`

### Blockchain (`blockchain`)
**For**: Solana development with on-chain data, social media, documentation.
**MCPs**: Core + claude-context, mcpdoc (Solana/Helius/Jupiter), omnisearch, daytona, helius, twitter
**Skills**: autonomous-agent, solana-development
**Required env**: `E2B_API_KEY` (from core), `HELIUS_API_KEY`, `OPENAI_API_KEY`
**Optional env**: `ZILLIZ_API_KEY`, `TAVILY_API_KEY`, `EXA_API_KEY`, `PERPLEXITY_API_KEY`, `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`

### Full (`full`)
**For**: Multi-domain projects needing everything.
**MCPs**: All available MCPs
**Skills**: All available skills
**Required env**: `E2B_API_KEY`, `OPENAI_API_KEY`, `HELIUS_API_KEY`
**Optional env**: All optional vars from all profiles

## How `extends` works

All non-core profiles inherit from core via `"extends": "core"`. This means:
- Core MCPs (e2b, memorygraph, sequential-thinking, fetch) are always included
- Core env vars (`E2B_API_KEY`) are always required
- Core skills (autonomous-agent) are always included

## Using a Profile

### Option 1: Copy a template
```bash
cp templates/research.mcp.json /path/to/your/project/.mcp.json
```

### Option 2: Use the installer
```bash
bash install.sh /path/to/your/project research
```

### Option 3: Manual assembly
Reference `profiles/*.json` to see which MCPs each profile includes, then build your own `.mcp.json` from the `mcps/*.json` fragments.

## Extending Profiles

Create custom profiles by:

1. Copying an existing `profiles/*.json`
2. Adding or removing MCPs from the `mcps` array
3. Updating `env_required` and `env_optional`
4. Creating a matching template in `templates/`
5. Running `install.sh` with your custom profile name
