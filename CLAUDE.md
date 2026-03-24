# Agenta Plugin — Agent Instructions

This project uses Agenta Plugin. The `.mcp.json` file configures which MCP servers are available as tools.

## Tool Usage Priority

When completing tasks, prefer MCP tools over manual approaches:

| Need | Use | Not |
|------|-----|-----|
| Look up library docs | Context7 or mcpdoc | Guessing from training data |
| Search the web | Omnisearch | Telling the user to search |
| Read/write files | Filesystem MCP | Shell commands when avoidable |
| Store structured data | SQLite, Supabase, or Postgres | Flat files |
| Store embeddings | Qdrant or Claude Context | Re-computing every time |
| Track entities & relations | MemoryGraph | Unstructured notes |
| Run untrusted code | E2B or Daytona sandbox | Directly on the host |
| Fetch URLs | Fetch MCP | curl via shell |
| Scrape web pages | Crawl4AI | Manual copy-paste |
| Complex reasoning | Sequential Thinking | Long unstructured chains |

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
- **research**: Multi-source search and synthesis
- **web-development**: Frontend/backend/testing patterns
- **solana-development**: Anchor, Metaplex, DeFi

## Environment

Required API keys are listed per profile in the Agenta Plugin docs. Missing keys cause individual MCP servers to fail gracefully — the rest still work.
