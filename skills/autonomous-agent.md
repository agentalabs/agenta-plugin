---
description: Autonomous agent operation patterns for task decomposition, memory management, self-correction, and multi-step workflows. Always active as a foundational skill.
globs:
  - "**/*"
---

# Autonomous Agent Skill

## Overview

Foundational patterns for operating as an autonomous agent within Claude Code. Covers task decomposition, persistent memory, self-correction loops, and multi-step workflow execution.

## When This Skill Applies

- Always active as a base operational layer
- Task planning and decomposition
- Multi-step workflows requiring state management
- Self-assessment and error recovery

## Available Tools

- **MemoryGraph**: Persistent knowledge graph for cross-session memory
- **Sequential Thinking**: Structured reasoning for complex decisions
- **E2B**: Sandboxed code execution for safe experimentation
- **Fetch**: HTTP requests for external data gathering

## Task Decomposition

### Breaking Down Complex Tasks

1. **Analyze the request**: Identify the end goal and constraints
2. **Identify sub-tasks**: Break into independently completable units
3. **Order by dependency**: Determine which tasks block others
4. **Estimate complexity**: Flag tasks that may need user input
5. **Execute iteratively**: Complete one sub-task, verify, proceed

### Decision Framework

Use Sequential Thinking MCP for complex decisions:

- Define the problem clearly
- List available options
- Evaluate trade-offs for each option
- Select and justify the chosen approach
- Document the decision for future reference

## Memory Management

### Knowledge Graph (MemoryGraph)

Use MemoryGraph to persist information across sessions:

- **Store discoveries**: Architecture decisions, API patterns, project conventions
- **Track relationships**: Component dependencies, data flow, team ownership
- **Query context**: Retrieve relevant knowledge before starting tasks

### Memory Hygiene

- Store facts, not opinions
- Include timestamps and sources
- Update or remove stale entries
- Keep granularity appropriate (not too broad, not too specific)

## Self-Correction Patterns

### Error Recovery

1. **Detect**: Recognize when output doesn't match expectations
2. **Diagnose**: Identify the root cause (wrong assumption, missing context, tool failure)
3. **Correct**: Apply the fix and verify
4. **Learn**: Store the correction pattern in memory for future reference

### Validation Loops

- After writing code: run tests or linter
- After making changes: verify the change achieves the goal
- After research: cross-reference multiple sources
- After complex reasoning: review with Sequential Thinking

## Multi-Step Workflow Execution

### Workflow Pattern

1. Plan the full workflow before starting
2. Execute each step with clear success criteria
3. Checkpoint progress at natural boundaries
4. Handle failures gracefully (retry, skip, or escalate)
5. Summarize results at completion

### Parallel vs Sequential

- **Parallel**: Independent research queries, file reads, test runs
- **Sequential**: Steps with data dependencies, stateful operations
- **Mixed**: Parallelize where possible, serialize where necessary

## Scheduled Maintenance & Recurring Tasks

### Task Scheduling Patterns

Define recurring tasks using a simple manifest format. Store this in a YAML config or as structured data in SQLite/MemoryGraph:

```yaml
tasks:
  - name: sync-rss-feeds
    schedule: daily
    sources:
      - type: rss
        url: https://example.com/feed.xml
      - type: rss
        url: https://blog.example.com/rss
    action: ingest-to-kb
  - name: cleanup-stale-entries
    schedule: weekly
    action: prune-older-than-30d
  - name: generate-weekly-digest
    schedule: weekly
    action: summarize-new-entries
  - name: full-reindex
    schedule: monthly
    action: rebuild-vector-indexes
```

Supported schedules: `daily`, `weekly`, `monthly`, or cron-style expressions for finer control. Each task declares its sources and the action to perform.

### Run Loop Pattern

On startup (or when triggered), the agent follows this loop:

1. **Check what's due**: Query the task registry for tasks whose `last_run + schedule_interval < now`
2. **Execute each due task**: Run the declared action against the declared sources
3. **Log results**: Record start time, end time, items processed, errors encountered
4. **Report summary**: Produce a concise summary of what ran, what succeeded, and what failed

This pattern works whether the agent runs continuously, on a cron schedule, or is invoked manually. The key is that the agent can always determine what needs doing by comparing timestamps.

### Idempotency

Every maintenance task must be safe to re-run without causing duplicates or corruption:

- **Use checksums**: Hash content before ingesting. If the hash matches an existing entry, skip it.
- **Use timestamps**: Track `last_processed_at` per source. Only fetch items newer than that timestamp.
- **Use upsert semantics**: When writing to vector DBs or SQLite, use upsert (insert-or-update) rather than blind inserts.
- **Deduplication on read**: Before inserting a new chunk, query for existing chunks with the same source URL and content hash.

If a task is interrupted mid-run, re-running it should pick up where it left off without creating duplicates.

### Logging

Store run history for auditability and debugging:

- **SQLite**: Create a `task_runs` table with columns: `id`, `task_name`, `started_at`, `completed_at`, `status`, `items_added`, `items_skipped`, `errors`, `summary`
- **MemoryGraph**: Store run summaries as entities with relationships to the sources they processed. Useful for cross-session queries like "when did we last sync source X?"
- Retain at least 30 days of run history for troubleshooting
- Flag runs with errors for review

## Knowledge Base Maintenance

### Incremental Sync

Only fetch and process what's new since the last run to minimize wasted work and API calls:

- **Track last-fetched timestamps** per source in SQLite. Each source row stores `last_sync` — only request content newer than this.
- **Use HTTP ETags / Last-Modified headers** via Fetch MCP. Send `If-None-Match` or `If-Modified-Since` headers. If the server returns 304 Not Modified, skip processing entirely.
- **Compare content hashes** to detect actual changes. A page may return 200 OK but have identical content (dynamic timestamps in headers, ad changes, etc.). Hash the extracted text content and compare to the stored hash before re-processing.

### Structured Source Ingestion

For sources with well-defined schemas:

- **RSS/Atom feeds**: Parse the feed XML, extract entries with `<pubDate>` or `<updated>` newer than `last_sync`. For each entry, fetch the full content URL, chunk the text, generate embeddings, and upsert into the vector DB with metadata (title, author, date, feed URL).
- **API endpoints**: Use pagination (offset/cursor) to fetch records modified since `last_sync`. Transform API responses into a consistent document format before chunking. Handle rate limits with exponential backoff.
- **Database tables**: Query for rows where `modified_at > last_sync`. Export as structured documents. Particularly useful for syncing from Supabase or Postgres via their respective MCPs.
- **Git repos**: Clone or pull in an E2B sandbox. Diff against the last known commit hash. Only process files that changed. Useful for syncing documentation repos or codebases.

### Unstructured Source Ingestion

For sources without predictable structure:

- **Web pages**: Use Crawl4AI to scrape the page. Compare the extracted text against the cached version (stored hash). If content changed, re-chunk and re-embed the entire page. Delete old chunks for that URL before inserting new ones to avoid stale fragments.
- **Documents (PDF, DOCX, etc.)**: Use Filesystem MCP to read the file. Compare file modification time and content hash against stored values. If modified, re-process the entire document. For large documents, consider incremental chunking if the format supports it (e.g., markdown with clear section boundaries).

### Deduplication

Before inserting any new chunk into the vector DB:

1. Generate the embedding for the new chunk
2. Query the vector DB for existing entries with similarity > 0.95
3. If a near-duplicate exists from the same source, update metadata (timestamp) but skip re-insertion
4. If a near-duplicate exists from a different source, insert but add a `duplicate_of` metadata field for transparency
5. Log all skipped duplicates for the run summary

### Pruning & Cleanup

Regularly remove stale or broken content:

- **Dead sources**: Check source URLs with HEAD requests. If a source returns 404 three or more times consecutively, mark it as `inactive` in the registry and optionally archive or delete its entries.
- **Expired content**: Remove entries older than the configured retention period (e.g., 90 days for news, indefinite for documentation).
- **Orphaned chunks**: After deleting a document entry, ensure all associated chunks are also removed from the vector DB.
- **Index rebuilding**: After large batch deletions or insertions (100+ entries), trigger an index rebuild in Qdrant to maintain search performance.

### Health Checks

Run periodic health checks to catch issues early:

- **Vector DB connectivity**: Ping Qdrant, verify collection exists and is accessible
- **Embedding model availability**: Send a test embedding request with a short string, verify a vector is returned
- **Source accessibility**: HEAD request each registered source URL, flag any that are unreachable
- **Storage usage**: Query Qdrant collection info for point count and storage size, alert if approaching limits
- **SQLite integrity**: Run `PRAGMA integrity_check` on the metadata database

## Source Registry Pattern

Maintain a central registry of all data sources the agent manages. This is the single source of truth for what to sync, when, and the current status.

### Registry Schema

```
Source Registry (SQLite table: source_registry)
| id | name           | type    | url                          | schedule | last_sync           | last_hash                        | status   |
|----|----------------|---------|------------------------------|----------|---------------------|----------------------------------|----------|
| 1  | tech-blog-rss  | rss     | https://blog.example.com/rss | daily    | 2025-01-15T08:00:00 | a1b2c3d4e5f6...                  | active   |
| 2  | docs-api       | api     | https://api.example.com/docs | daily    | 2025-01-15T08:00:00 | b2c3d4e5f6a7...                  | active   |
| 3  | company-wiki   | webpage | https://wiki.example.com     | weekly   | 2025-01-13T00:00:00 | c3d4e5f6a7b8...                  | active   |
| 4  | local-docs     | file    | /data/documents/             | daily    | 2025-01-15T08:00:00 | d4e5f6a7b8c9...                  | active   |
| 5  | analytics-db   | database| postgres://analytics/main    | weekly   | 2025-01-13T00:00:00 | e5f6a7b8c9d0...                  | active   |
| 6  | docs-repo      | git     | https://github.com/org/docs  | daily    | 2025-01-15T08:00:00 | f6a7b8c9d0e1...                  | active   |
| 7  | old-blog       | rss     | https://old.example.com/rss  | daily    | 2025-01-10T08:00:00 | -                                | inactive |
```

### Supported Types

- **rss**: RSS or Atom feed URLs. Parsed with XML extraction.
- **api**: REST API endpoints. Requires pagination strategy in metadata.
- **webpage**: Single web pages. Scraped with Crawl4AI.
- **file**: Local file paths or directories. Read via Filesystem MCP.
- **database**: Database connection strings. Queried via Supabase/Postgres MCP.
- **git**: Git repository URLs. Cloned and diffed in E2B sandbox.

### Agent Startup Flow

1. **Load registry**: Query `source_registry` for all `status = 'active'` sources
2. **Identify due sources**: Filter where `last_sync + schedule_interval < now()`
3. **Execute sync** for each due source using the appropriate ingestion method for its type
4. **Update registry**: Set `last_sync = now()`, `last_hash = new_hash` for successfully synced sources
5. **Handle errors**: Increment an `error_count` column. If `error_count >= 3`, set `status = 'inactive'` and log a warning.

### Dynamic Source Management

Sources can be added or removed at runtime:

- **Add a source**: Insert a new row with `status = 'active'` and `last_sync = NULL` (triggers immediate sync on next run)
- **Remove a source**: Set `status = 'removed'`. Optionally delete associated chunks from the vector DB.
- **Pause a source**: Set `status = 'paused'`. The agent skips it during sync but preserves existing data.
- **Re-activate**: Set `status = 'active'` and optionally reset `last_sync` to force a full re-sync.

The agent should expose these operations through natural language commands: "add this RSS feed to the knowledge base", "pause syncing the wiki", "remove the old blog source and clean up its entries".

## Best Practices

- Prefer incremental progress over big-bang changes
- Verify assumptions before building on them
- Ask for clarification when requirements are ambiguous
- Use sandboxed execution (E2B) for risky operations
- Document non-obvious decisions for future context
- Always check what's already stored before ingesting (prevent duplicates)
- Use content hashes to detect real changes vs. cosmetic URL/timestamp differences
- Batch vector operations (embed and upsert in groups of 50-100)
- Log every sync run with source, items_added, items_skipped, errors
- Fail gracefully per-source — one broken feed shouldn't stop the whole run
