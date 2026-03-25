# Agenta Plugin — Agent Instructions

This project uses Agenta Plugin. The `.mcp.json` file configures which MCP servers are available as tools.

## Tool Usage Priority

When completing tasks, use the best tool available — native Claude Code tools are often sufficient:

| Need | Best tool | When to escalate |
|------|-----------|-----------------|
| Look up library docs | Context7 or mcpdoc | — |
| Simple web search | WebSearch (native) | Omnisearch for multi-engine research |
| Fetch a URL | WebFetch (native) | Crawl4AI for anti-bot sites, Puppeteer for JS-rendered pages |
| Read/write/edit files | Read, Write, Edit (native) | — |
| Search file contents | Grep, Glob (native) | — |
| Store structured data | SQLite, Supabase, or Postgres | — |
| Store embeddings | Qdrant or Claude Context | — |
| Track entities & relations | MemoryGraph | — |
| Run untrusted code | E2B or Daytona sandbox | — |
| Scrape web pages | Crawl4AI | Puppeteer for JS-rendered pages |
| Search academic papers | Consensus | — |
| Manage context window | Context Mode | — |
| Persistent cross-session memory | Memsearch | — |
| Ingest sources into KB | Skill Seekers | — |

## Important

Always clarify with the user if something is unclear before proceeding.

## Knowledge Base Maintenance

If this project maintains a knowledge base, follow these patterns:

### Source registry

Maintain a source registry in SQLite tracking each data source:
- Source name, type (rss, api, webpage, file, database), URL/path
- Sync schedule (daily, weekly, on-demand)
- Last sync timestamp and content hash
- Status (active, error, disabled)

### Incremental sync

On each maintenance run:
1. Query the source registry for sources due for sync
2. For each source: fetch content, compare hash to last known hash
3. Skip unchanged sources entirely
4. For changed sources: chunk, embed, deduplicate (similarity > 0.95 = skip), upsert
5. Update the registry with new timestamp and hash
6. Log: sources_checked, items_added, items_skipped, errors

### Change detection by source type

- **RSS/API**: Use Last-Modified headers, pagination cursors, or timestamp filters
- **Web pages**: Content hash comparison after scraping
- **Local files**: File modification time + content hash
- **Database tables**: Query by updated_at column since last sync

### Health checks

Before each run, verify:
- Vector DB is reachable (Qdrant/Claude Context)
- Embedding model is responding
- Source URLs are accessible (HEAD requests)
- SQLite registry is intact

## Skills

Skills in `skills/` auto-apply based on file patterns. They provide domain-specific patterns for:
- **autonomous-agent**: Task planning, memory, self-correction, maintenance workflows
- **knowledge-base**: RAG pipelines, ingestion, vector search, automated sync
- **research**: Multi-source search, synthesis, academic papers, cross-session memory
- **superpowers**: TDD, systematic debugging, code review, planning, git worktrees

## Environment

Required API keys are listed per profile in the Agenta Plugin docs. Missing keys cause individual MCP servers to fail gracefully — the rest still work.
