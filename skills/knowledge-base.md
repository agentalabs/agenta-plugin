---
description: Knowledge base management patterns for RAG pipelines, document ingestion, vector search, and structured storage. Auto-applies when working with embeddings, knowledge graphs, or document processing.
globs:
  - "**/knowledge/**/*"
  - "**/kb/**/*"
  - "**/embeddings/**/*"
  - "**/vectors/**/*"
  - "**/*.jsonl"
---

# Knowledge Base Management Skill

## Overview

Patterns and best practices for building, maintaining, and querying knowledge bases using vector databases, knowledge graphs, and structured storage.

## When This Skill Applies

- Building or maintaining a knowledge base or RAG pipeline
- Ingesting documents, web pages, or structured data
- Configuring vector search or embeddings
- Working with knowledge graphs (MemoryGraph)
- Setting up retrieval-augmented generation

## Available Tools

- **MemoryGraph**: Store and query entity-relationship knowledge graphs
- **Qdrant**: Vector database for embeddings and similarity search
- **Claude Context**: Semantic codebase search with vector indexing
- **SQLite**: Structured metadata and relational data storage
- **Crawl4AI**: Scrape web content for ingestion

## Document Ingestion Workflow

### 1. Source Collection

Gather documents from multiple sources:

- **Local files**: Read files directly (Claude Code has native file access)
- **Web pages**: Use Crawl4AI to scrape and extract clean text
- **APIs**: Use WebFetch to pull data from REST endpoints

### 2. Chunking Strategy

Split documents into retrieval-friendly chunks:

- **Semantic chunking**: Split on headings, paragraphs, or topic boundaries
- **Fixed-size chunks**: 512-1024 tokens with 50-100 token overlap
- **Hybrid**: Semantic boundaries with max-size fallback

### 3. Embedding & Storage

- Generate embeddings via OpenAI API or local models
- Store in Qdrant with metadata (source, date, section, tags)
- Index in Claude Context for codebase-aware search

### 4. Knowledge Graph

Use MemoryGraph for structured relationships:

- **Entities**: Documents, concepts, people, projects
- **Relations**: references, depends-on, authored-by, related-to
- **Queries**: Traverse relationships for context-aware retrieval

## RAG Query Patterns

### Basic Retrieval

1. Embed the user query
2. Search Qdrant for top-k similar chunks
3. Combine chunks as context for generation

### Hybrid Search

1. Vector search for semantic similarity
2. Keyword/BM25 search for exact matches
3. Knowledge graph traversal for related entities
4. Merge and re-rank results

### Context Window Management

- Prioritize most relevant chunks
- Include metadata for source attribution
- Keep total context under model limits
- Use Context Mode for token reduction on large outputs

## Storage Schema Patterns

### SQLite Metadata

Use SQLite for structured metadata alongside vector storage:

- Document registry (id, source, ingestion_date, status)
- Chunk index (chunk_id, doc_id, position, token_count)
- Query logs (query, results, feedback, timestamp)

### Qdrant Collections

Organize vectors by content type:

- `documents` - Main knowledge base content
- `code` - Code snippets and examples
- `conversations` - Chat history and Q&A pairs

## Best Practices

- Always store source attribution with chunks
- Version your knowledge base (track ingestion dates)
- Implement deduplication before ingestion
- Monitor retrieval quality with relevance scoring
- Use metadata filters to scope searches
- Regularly re-index when source documents change

## Automated Maintenance

### Daily Sync Workflow

For knowledge bases with recurring sources, follow this pattern:

1. **Load source registry** from SQLite (source name, URL, type, last_sync, schedule)
2. **Filter due sources** based on schedule and last_sync timestamp
3. **For each due source**:
   - Fetch new content (RSS → parse feed, API → paginate since last_sync, webpage → scrape)
   - Compare content hash against last known hash — skip if unchanged
   - Chunk new content and generate embeddings
   - Check for duplicates in vector DB (similarity > 0.95 = skip)
   - Upsert new chunks with metadata (source, timestamp, hash)
   - Update source registry with new last_sync and content hash
4. **Prune stale entries** — check sources that return errors 3+ times consecutively
5. **Log run summary** — sources checked, items added, items skipped, errors

### Source Types

| Type | Fetch Method | Change Detection | Tools Used |
|------|-------------|-----------------|------------|
| RSS/Atom | WebFetch | ETag / Last-Modified | WebFetch, E2B |
| API | WebFetch | Pagination cursor / timestamp | WebFetch |
| Webpage | Crawl4AI | Content hash comparison | Crawl4AI |
| Local files | Native file access | File modification time + hash | Native file access |
| Database | Supabase/Postgres | Modified-at column query | Supabase, Postgres |
| Git repo | E2B sandbox | Commit hash comparison | E2B |

### Source Registry Schema

Maintain a central registry of all data sources. This is the single source of truth for what to sync, when, and the current status.

```sql
CREATE TABLE source_registry (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    type        TEXT NOT NULL CHECK (type IN ('rss', 'api', 'webpage', 'file', 'database', 'git')),
    url         TEXT NOT NULL,
    schedule    TEXT NOT NULL DEFAULT 'daily',
    last_sync   TIMESTAMP,
    last_hash   TEXT,
    error_count INTEGER DEFAULT 0,
    status      TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'paused', 'removed'))
);
```

Supported types:
- **rss**: RSS or Atom feed URLs. Parsed with XML extraction.
- **api**: REST API endpoints. Requires pagination strategy in metadata.
- **webpage**: Single web pages. Scraped with Crawl4AI.
- **file**: Local file paths or directories. Read via native file access.
- **database**: Database connection strings. Queried via Supabase/Postgres MCP.
- **git**: Git repository URLs. Cloned and diffed in E2B sandbox.

### Dynamic Source Management

Sources can be added or removed at runtime:

- **Add a source**: Insert a new row with `status = 'active'` and `last_sync = NULL` (triggers immediate sync on next run)
- **Remove a source**: Set `status = 'removed'`. Optionally delete associated chunks from the vector DB.
- **Pause a source**: Set `status = 'paused'`. The agent skips it during sync but preserves existing data.
- **Re-activate**: Set `status = 'active'` and optionally reset `last_sync` to force a full re-sync.

### Idempotency

Every maintenance task must be safe to re-run without causing duplicates or corruption:

- **Use checksums**: Hash content before ingesting. If the hash matches an existing entry, skip it.
- **Use timestamps**: Track `last_processed_at` per source. Only fetch items newer than that timestamp.
- **Use upsert semantics**: When writing to vector DBs or SQLite, use upsert (insert-or-update) rather than blind inserts.
- **Deduplication on read**: Before inserting a new chunk, query for existing chunks with the same source URL and content hash.

If a task is interrupted mid-run, re-running it should pick up where it left off without creating duplicates.

### Pruning & Cleanup

Regularly remove stale or broken content:

- **Dead sources**: Check source URLs with HEAD requests. If a source returns 404 three or more times consecutively, mark it as `inactive` in the registry and optionally archive or delete its entries.
- **Expired content**: Remove entries older than the configured retention period (e.g., 90 days for news, indefinite for documentation).
- **Orphaned chunks**: After deleting a document entry, ensure all associated chunks are also removed from the vector DB.
- **Index rebuilding**: After large batch deletions or insertions (100+ entries), trigger an index rebuild in Qdrant to maintain search performance.

### Health Monitoring

Run periodic checks:
- Vector DB connection alive (Qdrant ping)
- Embedding model responding (test embed a short string)
- Source URLs accessible (HEAD request via WebFetch)
- Storage usage within limits (Qdrant collection info)
- SQLite registry integrity check
