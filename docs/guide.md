# Agenta Plugin — Use Cases & User Flows

This guide walks through real-world scenarios showing how to use Agenta Plugin end-to-end. Each section covers a distinct use case, the recommended profile, and the step-by-step flow from installation through daily use.

For reference material, see:
- [profiles.md](profiles.md) — Profile descriptions and MCP composition
- [mcp-catalog.md](mcp-catalog.md) — Individual MCP server setup details
- [env-vars.md](env-vars.md) — All environment variables

---

## Table of Contents

1. [Getting Started — First-Time Setup](#getting-started)
2. [Building a Knowledge Base from Scratch](#building-a-knowledge-base-from-scratch)
3. [Automated KB Maintenance — Daily Sync Agent](#automated-kb-maintenance--daily-sync-agent)
4. [Research & Competitive Analysis](#research--competitive-analysis)
5. [Full-Stack Web Application Development](#full-stack-web-application-development)
6. [Solana Blockchain Development](#solana-blockchain-development)
7. [Running an Autonomous Agent on Any Project](#running-an-autonomous-agent-on-any-project)
8. [Combining Profiles for Multi-Domain Work](#combining-profiles-for-multi-domain-work)
9. [Adding Agenta to an Existing Project](#adding-agenta-to-an-existing-project)
10. [Creating a Custom Profile](#creating-a-custom-profile)
11. [Team Onboarding](#team-onboarding)

---

## Getting Started

### Prerequisites

- [Claude Code](https://claude.ai/code) installed and authenticated
- Node.js 18+ (for npx-based MCP servers)
- Python 3.10+ (for uvx-based servers)
- Docker (optional, for Crawl4AI)

### First installation

```bash
# Clone the plugin repo
git clone https://github.com/superteam-brasil/agenta.git agenta-plugin

# Run the interactive installer pointing at your project
bash agenta-plugin/install.sh /path/to/my-project
```

The installer will:
1. Ask you to pick a profile (core, knowledge-base, research, web-dev, blockchain, full)
2. Copy the matching `.mcp.json` into your project
3. Copy the relevant skill files into `your-project/skills/`
4. Generate a `CLAUDE.md` with agent instructions (skipped if one already exists)
5. Check which required environment variables are set and flag any missing ones

### Non-interactive installation

If you already know your profile:

```bash
bash agenta-plugin/install.sh /path/to/my-project research
```

Or skip the installer entirely:

```bash
cp agenta-plugin/templates/research.mcp.json /path/to/my-project/.mcp.json
cp agenta-plugin/skills/autonomous-agent.md /path/to/my-project/skills/
cp agenta-plugin/skills/research.md /path/to/my-project/skills/
```

### Verifying the setup

Open your project in Claude Code. MCP servers listed in `.mcp.json` will be available as tools. Ask Claude to list its available tools to confirm they loaded.

---

## Building a Knowledge Base from Scratch

**Profile**: `knowledge-base`
**Scenario**: You have a collection of documents (markdown files, web pages, API responses) and want to build a searchable knowledge base with vector retrieval.

### Step 1: Install

```bash
bash agenta-plugin/install.sh ./my-kb-project knowledge-base
```

Set the required environment variables:

```bash
export E2B_API_KEY="..."       # For sandboxed execution
export OPENAI_API_KEY="..."    # For generating embeddings
```

Optional but recommended:

```bash
export QDRANT_URL="http://localhost:6333"  # If running Qdrant locally
export ZILLIZ_API_KEY="..."                # If using Zilliz cloud
```

### Step 2: Ingest local documents

Open Claude Code in the project directory:

```
You: I have markdown files in docs/ that I want to ingest into the knowledge base.
     Read each file, chunk it by heading, and store the chunks in Qdrant with
     source metadata.
```

Claude will use:
- **Filesystem** to read your document files
- **E2B** to run a chunking script in a sandbox
- **Qdrant** to store the embedded chunks
- **SQLite** to maintain a document registry tracking what's been ingested

### Step 3: Ingest web content

```
You: Scrape these pages and add them to the knowledge base:
     - https://example.com/docs/getting-started
     - https://example.com/docs/api-reference
```

Claude will use:
- **Crawl4AI** to scrape pages and extract clean text
- The same chunking and storage pipeline from Step 2

### Step 4: Build a knowledge graph

```
You: Analyze the ingested documents and build a knowledge graph of the key
     concepts, their relationships, and which documents reference them.
```

Claude will use:
- **MemoryGraph** to create entities (concepts, documents, people) and relationships
- **Sequential Thinking** to reason about concept hierarchies

### Step 5: Query the knowledge base

```
You: What does our documentation say about authentication? Include sources.
```

Claude will use:
- **Qdrant** for vector similarity search
- **MemoryGraph** to find related concepts
- **SQLite** to look up source attribution

### Ongoing maintenance

As documents change, tell Claude to re-ingest specific files or URLs. The SQLite registry tracks ingestion dates so Claude can identify stale content. See the next section for automated daily sync.

---

## Automated KB Maintenance — Daily Sync Agent

**Profile**: `knowledge-base`
**Scenario**: You have an existing knowledge base with structured sources (RSS feeds, APIs, database tables) and unstructured ones (web pages, documents). An agent runs daily to check each source, fetch only what's new, and ingest it.

This is the most common Agenta Plugin workflow — a maintenance agent that keeps your KB current without manual intervention.

### The source registry

First, set up a source registry in SQLite. This is the single table that drives all maintenance:

```
You: Create a SQLite table called source_registry with columns:
     id, name, type, url, schedule, last_sync, last_hash, status, error_count

     Types: rss, api, webpage, file, database
     Schedule: daily, weekly, hourly, on-demand
     Status: active, error, disabled
```

Claude will use **SQLite** to create and manage this table.

### Registering sources

Add your sources — both structured and unstructured:

```
You: Register these sources in the source_registry:

     Structured:
     - name: "tech-blog-rss", type: rss, url: https://blog.example.com/rss, schedule: daily
     - name: "product-api", type: api, url: https://api.example.com/v1/products, schedule: daily
     - name: "users-table", type: database, url: supabase://public.users, schedule: daily

     Unstructured:
     - name: "competitor-docs", type: webpage, url: https://competitor.com/docs, schedule: weekly
     - name: "internal-wiki", type: webpage, url: https://wiki.internal.com/knowledge, schedule: daily
     - name: "local-reports", type: file, url: ./reports/*.md, schedule: daily
```

### The daily sync flow

Tell the agent to run the sync:

```
You: Run the daily knowledge base sync. Check all sources due for update,
     fetch only what's new, and ingest it. Give me a summary when done.
```

Claude will execute this flow:

**1. Check what's due**
- Query source_registry for sources where `schedule = 'daily'` AND `last_sync < today` AND `status = 'active'`
- Uses **SQLite**

**2. Fetch each source by type**

| Source type | How it fetches | Change detection | Tools |
|-------------|---------------|------------------|-------|
| **rss** | Parse feed XML | Compare entry GUIDs/dates against last_sync | **Fetch** |
| **api** | GET with `?updated_since=last_sync` | Pagination cursor or timestamp filter | **Fetch** |
| **webpage** | Full page scrape | Hash page content, compare to last_hash | **Crawl4AI** |
| **file** | Read from disk | File modification time + content hash | **Filesystem** |
| **database** | Query `WHERE updated_at > last_sync` | Row count + content hash | **Supabase** or **Postgres** |

**3. Process new content**
- Chunk new content (semantic boundaries, 512-1024 tokens)
- Generate embeddings via OpenAI
- **Deduplicate**: Check vector similarity in Qdrant — skip if any existing chunk has similarity > 0.95
- Upsert new chunks with metadata: `{source, ingested_at, source_url, chunk_index}`
- Uses **Qdrant**, **E2B** (for embedding scripts)

**4. Update the registry**
- Set `last_sync = now()`, `last_hash = new_hash`, `error_count = 0`
- On failure: increment `error_count`, set `status = 'error'` if `error_count >= 3`
- Uses **SQLite**

**5. Update the knowledge graph**
- Extract key entities from new content
- Add/update relationships in MemoryGraph
- Uses **MemoryGraph**

**6. Report**
```
Sync complete:
  Sources checked: 6
  Sources updated: 3 (tech-blog-rss, product-api, internal-wiki)
  Sources unchanged: 2 (competitor-docs, local-reports)
  Sources errored: 1 (users-table — connection timeout)
  Items added: 47
  Items skipped (duplicates): 12
  Next run: tomorrow
```

### Handling structured vs unstructured sources

**Structured sources** (RSS, API, database) have natural change boundaries:
- RSS feeds have per-entry dates and GUIDs
- APIs support `?since=timestamp` or cursor pagination
- Database tables have `updated_at` or `created_at` columns
- Change detection is precise — you know exactly which records are new

**Unstructured sources** (web pages, documents) require hash-based detection:
- Scrape or read the full content
- Hash it (SHA-256 of the cleaned text)
- Compare to `last_hash` in the registry
- If different: re-chunk the entire page and diff against existing vectors
- If same: skip entirely

### Pruning stale content

Run weekly:

```
You: Prune the knowledge base:
     1. Check all sources — flag any that return 404 or have errored 3+ times
     2. Remove vectors whose source is now disabled
     3. Remove vectors older than 90 days that haven't been accessed
     4. Report what was removed
```

### Health checks

Run before each sync:

```
You: Run KB health checks:
     - Is Qdrant reachable? How many vectors are stored?
     - Can we generate a test embedding?
     - Are all active sources accessible? (HEAD request each URL)
     - Any sources stuck in error state?
```

### Example: Adding a new source mid-lifecycle

```
You: Add a new source to the registry:
     name: "engineering-blog"
     type: rss
     url: https://engineering.example.com/feed
     schedule: daily

     Then do an initial full sync of just that source.
```

Claude will register it in SQLite, fetch the full feed, ingest all entries, and set `last_sync` to now. Future daily runs will only fetch entries newer than this timestamp.

---

## Research & Competitive Analysis

**Profile**: `research`
**Scenario**: You need to research a topic, compare alternatives, and produce a structured report.

### Step 1: Install

```bash
bash agenta-plugin/install.sh ./market-research research
export E2B_API_KEY="..."
export TAVILY_API_KEY="..."
```

### Step 2: Broad exploration

```
You: Research the current state of open-source vector databases. I need to
     understand the top 5 options, their trade-offs, and which is best for
     a team of 3 building a RAG pipeline.
```

Claude will:
1. **Omnisearch** (Tavily) — broad web search for "open source vector database comparison 2026"
2. **Omnisearch** (Exa) — semantic search for technical deep-dives
3. **Crawl4AI** — scrape the most relevant comparison articles for full content
4. **Context7** — pull documentation for specific databases (Qdrant, Chroma, Weaviate, etc.)
5. **Sequential Thinking** — structure the comparison framework
6. **MemoryGraph** — store findings as entities with relationships for follow-up

### Step 3: Deep dive on candidates

```
You: Go deeper on Qdrant and Chroma. Compare their Python APIs, hosting
     options, pricing, and performance benchmarks.
```

Claude will use **Puppeteer** for any pages that require JavaScript rendering (pricing pages, interactive docs), and **mcpdoc** if either project publishes an llms.txt endpoint.

### Step 4: Generate the report

```
You: Write a comparison report in reports/vector-db-comparison.md with
     an executive summary, detailed comparison table, and recommendation.
```

### Step 5: Store in Notion (optional)

```
You: Push the report to our Notion workspace under the "Research" database.
```

Claude will use **Notion** to create a new page with the report content.

---

## Full-Stack Web Application Development

**Profile**: `web-dev`
**Scenario**: Building or maintaining a web application with frontend, backend, and tests.

### Step 1: Install

```bash
bash agenta-plugin/install.sh ./my-web-app web-dev
export E2B_API_KEY="..."
```

### Step 2: Scaffold with documentation

```
You: I'm starting a new Next.js 15 app with Tailwind and Prisma. Set up
     the project structure following current best practices.
```

Claude will:
- **Context7** — fetch latest Next.js 15 documentation
- **mcpdoc** — check for llms.txt endpoints from Next.js, Prisma, etc.
- **Omnisearch** — search for current best practices and starter templates
- **Daytona** — spin up a container sandbox to test the scaffolding commands

### Step 3: Develop features

```
You: Add a user authentication system using NextAuth.js with GitHub and
     Google providers.
```

Claude will:
- **Context7** — pull NextAuth.js docs
- **Omnisearch** — search for integration patterns and known issues
- Write the code following patterns from the **web-development** skill

### Step 4: Test with browser automation

```
You: Write Playwright tests for the login flow — test both GitHub and
     Google OAuth, plus the error case when auth is denied.
```

Claude will:
- **Playwright MCP** — automate the browser to run through the OAuth flows
- **E2B** — run the test scripts in a sandbox
- Verify screenshots and assertions

### Step 5: Debug visual issues

```
You: The dashboard layout breaks on mobile. Open the app in a browser
     at 375px width and show me what's happening.
```

Claude will:
- **Puppeteer** — open the page in a headless browser at the specified viewport
- Capture a screenshot and identify the CSS issue
- Propose a fix

### Step 6: Prototype risky changes safely

```
You: I want to try migrating from REST to tRPC. Prototype it in a sandbox
     first without touching the main codebase.
```

Claude will use **Daytona** to create an isolated container with a copy of the project, make the changes there, and report back on feasibility before touching the real code.

---

## Solana Blockchain Development

**Profile**: `blockchain`
**Scenario**: Building Solana programs with Anchor, integrating with DeFi protocols, and managing social media presence.

### Step 1: Install

```bash
bash agenta-plugin/install.sh ./my-solana-project blockchain
export E2B_API_KEY="..."
export HELIUS_API_KEY="..."
export OPENAI_API_KEY="..."
```

### Step 2: Write a Solana program

```
You: Create an Anchor program for a token staking vault. Users deposit SPL
     tokens, earn rewards proportional to time staked, and can withdraw anytime.
```

Claude will:
- **mcpdoc** — fetch Solana, Helius, and Jupiter documentation via llms.txt
- **Claude Context** — search the codebase for existing patterns
- Apply the **solana-development** skill for Anchor best practices, PDA patterns, and security checklist
- **Sequential Thinking** — reason through the account structure and reward math

### Step 3: Query on-chain data

```
You: Show me the top 10 holders of token mint Abc123... and their staking
     positions in our program.
```

Claude will use **Helius** to query on-chain account data, asset info, and transaction history.

### Step 4: Test on devnet

```
You: Deploy the staking program to devnet and run the test suite.
```

Claude will:
- **Daytona** — use a container sandbox with Solana CLI and Anchor installed
- Run `anchor test --provider.cluster devnet`
- Report results and fix any failures

### Step 5: Security audit

```
You: Audit the staking program for common Solana vulnerabilities.
```

Claude will apply the security checklist from the solana-development skill: integer overflow, signer validation, account ownership, PDA bump validation, and close-account safety.

### Step 6: Social media announcement

```
You: Draft and post a tweet announcing the staking vault launch. Include
     the program address and a link to the docs.
```

Claude will use **Twitter** to compose and post the tweet (requires Twitter API credentials).

---

## Running an Autonomous Agent on Any Project

**Profile**: `core`
**Scenario**: You want Claude Code to operate more effectively as an autonomous agent on any type of project — better task planning, persistent memory, and structured reasoning.

### Step 1: Install

```bash
bash agenta-plugin/install.sh ./any-project core
export E2B_API_KEY="..."
```

### Step 2: Complex task planning

```
You: Refactor the payment processing module. It currently handles Stripe
     only, but we need to support Stripe, PayPal, and crypto payments
     through a provider-agnostic interface.
```

Claude will:
- **Sequential Thinking** — break the refactoring into phases, evaluate design options
- **MemoryGraph** — store the architectural decisions for future reference
- **E2B** — test each refactoring step in a sandbox before applying

### Step 3: Cross-session continuity

When you return to the project in a new session:

```
You: What were we working on with the payment module? What's left to do?
```

Claude will query **MemoryGraph** to retrieve the stored decisions, progress, and remaining tasks from the previous session.

### Step 4: External data gathering

```
You: Check if PayPal's API has changed their webhook signature format recently.
```

Claude will use **Fetch** to hit the PayPal developer docs endpoint and parse the response.

---

## Combining Profiles for Multi-Domain Work

**Profile**: `full`
**Scenario**: Your project spans multiple domains — for example, a blockchain application with a web frontend, a knowledge base, and research needs.

### When to use `full`

Use the `full` profile when your project genuinely needs tools from 3+ domains. For most projects, a single focused profile is better — fewer MCP servers means faster startup and less noise.

### Install

```bash
bash agenta-plugin/install.sh ./complex-project full
```

The full profile includes all 19 MCP servers and all 5 skills. Set environment variables for the MCPs you actually need — servers with missing credentials will fail gracefully.

### Typical flow

A DeFi dashboard project might use tools from multiple domains in a single session:

1. **Research** phase — Omnisearch + Crawl4AI to study competitor dashboards
2. **Blockchain** phase — Helius to query on-chain data, mcpdoc for Solana docs
3. **Web dev** phase — Playwright to test the dashboard UI, Context7 for React docs
4. **Knowledge base** phase — Qdrant to store user-facing help content

---

## Adding Agenta to an Existing Project

If your project already has a `.mcp.json`, the installer will ask before overwriting. You have three options:

### Option A: Replace entirely

Let the installer overwrite. Best if your existing `.mcp.json` only has MCPs that the profile already includes.

### Option B: Merge manually

1. Run the installer to a temporary directory:
   ```bash
   bash agenta-plugin/install.sh /tmp/agenta-staging research
   ```
2. Open both `.mcp.json` files and merge the `mcpServers` objects
3. Copy the merged result to your project

### Option C: Cherry-pick MCPs

Skip the installer. Copy individual MCP configs from `mcps/*.json` into your existing `.mcp.json`:

```bash
# View what an MCP config looks like
cat agenta-plugin/mcps/omnisearch.json

# Then manually add it to your .mcp.json under "mcpServers"
```

In all cases, copy the skills you want:

```bash
cp agenta-plugin/skills/autonomous-agent.md ./skills/
cp agenta-plugin/skills/research.md ./skills/
```

---

## Creating a Custom Profile

When no built-in profile fits your workflow, create a custom one.

### Step 1: Define the profile manifest

Create `profiles/my-profile.json`:

```json
{
  "name": "my-profile",
  "description": "Data engineering with research and storage capabilities.",
  "extends": "core",
  "mcps": ["omnisearch", "crawl4ai", "sqlite", "qdrant", "filesystem"],
  "skills": ["research", "knowledge-base"],
  "env_required": ["TAVILY_API_KEY"],
  "env_optional": ["QDRANT_URL", "QDRANT_API_KEY"],
  "mcpdoc_urls": []
}
```

### Step 2: Build the template

Assemble a `.mcp.json` from the fragments. The easiest way:

1. Start from a similar template (e.g., `templates/knowledge-base.mcp.json`)
2. Add or remove MCP entries by referencing `mcps/*.json` for the config
3. Save as `templates/my-profile.mcp.json`

### Step 3: Test it

```bash
bash install.sh /tmp/test-project my-profile
```

The installer recognizes any profile name that has a matching `profiles/*.json` and `templates/*.mcp.json`.

### Step 4: Contribute it back

If your custom profile is useful to others, submit a PR adding it to the repo. Include the profile manifest, template, and any new skills.

---

## Team Onboarding

When multiple people work on the same project with Agenta Plugin:

### Commit the config

Add these files to version control:

```
.mcp.json          # MCP server configuration
skills/            # Skill files for the project
CLAUDE.md          # Agent instructions
```

Do **not** commit API keys. Each team member sets their own environment variables.

### Document required keys

Add a note to your project README or CLAUDE.md:

```markdown
## Setup

This project uses Agenta Plugin (blockchain profile).

Required environment variables:
- `E2B_API_KEY` — get one at https://e2b.dev
- `HELIUS_API_KEY` — get one at https://helius.dev
- `OPENAI_API_KEY` — get one at https://platform.openai.com
```

### Shared vs personal config

- **Shared `.mcp.json`**: Committed to the repo. Contains MCPs the whole team needs.
- **Personal overrides**: Each developer can add extra MCPs to their local `.mcp.json` without committing. Use `.gitignore` patterns if needed, or rely on Claude Code's project-level config merging.

### New team member flow

```bash
# 1. Clone the project (already has .mcp.json and skills/)
git clone <repo-url>

# 2. Set environment variables
export E2B_API_KEY="..."
export HELIUS_API_KEY="..."

# 3. Open in Claude Code — everything works immediately
```

---

## Quick Reference: Which Profile for What

| I want to... | Use profile |
|---|---|
| Add agent memory and reasoning to any project | `core` |
| Build a RAG pipeline or document search | `knowledge-base` |
| Research a topic and write a report | `research` |
| Build or test a web application | `web-dev` |
| Develop Solana programs | `blockchain` |
| Do all of the above in one project | `full` |
| Mix and match specific MCPs | [Custom profile](#creating-a-custom-profile) |
