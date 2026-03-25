# MCP Server Catalog

Complete reference for all MCP servers available in Agenta Plugin.

## Sandbox & Execution

### e2b
- **Package**: `@e2b/mcp-server`
- **Purpose**: Cloud sandboxed code execution for TypeScript and Python
- **Env**: `E2B_API_KEY`
- **Profiles**: all

### daytona
- **Command**: `daytona mcp serve`
- **Purpose**: Container-based sandbox with full language support
- **Env**: none (requires daytona CLI installed)
- **Profiles**: web-dev, blockchain

## Search & Research

### omnisearch
- **Package**: `mcp-omnisearch`
- **Purpose**: Unified search across Tavily, Exa, and Perplexity
- **Env**: `TAVILY_API_KEY`, `EXA_API_KEY` (optional), `PERPLEXITY_API_KEY` (optional)
- **Profiles**: research, web-dev, blockchain

### crawl4ai
- **Command**: Docker container `uysalsadi/crawl4ai-mcp-server:latest`
- **Purpose**: Free, self-hosted web scraping with anti-bot handling
- **Env**: none (requires Docker)
- **Profiles**: knowledge-base, research, web-dev

### context7
- **Package**: `@upstash/context7-mcp`
- **Purpose**: Live documentation lookup for popular libraries
- **Env**: none
- **Profiles**: research, web-dev, blockchain

### consensus
- **Type**: HTTP MCP
- **URL**: `https://mcp.consensus.app/mcp`
- **Purpose**: Academic paper search across 200M+ peer-reviewed papers via Consensus
- **Env**: none
- **Profiles**: research, full

## Documentation

### mcpdoc
- **Command**: `uvx --from mcpdoc mcpdoc`
- **Purpose**: Documentation via llms.txt endpoints
- **Env**: none
- **Notes**: Add `--urls Name:URL` args to configure sources. Blockchain profile includes Solana/Helius/Jupiter URLs.
- **Profiles**: knowledge-base, research, web-dev, blockchain

## Memory & Storage

### memorygraph
- **Command**: `memorygraph`
- **Purpose**: Knowledge graph with SQLite default, supports Neo4j backend
- **Env**: none
- **Profiles**: all

### sqlite
- **Package**: `sqlite-mcp`
- **Purpose**: Local SQLite database operations
- **Env**: none
- **Profiles**: knowledge-base

### qdrant
- **Package**: `qdrant-mcp-server`
- **Purpose**: Vector database for embeddings and similarity search
- **Env**: `QDRANT_URL`, `QDRANT_API_KEY`
- **Profiles**: knowledge-base

### claude-context
- **Package**: `@zilliz/claude-context-mcp@latest`
- **Purpose**: Vector search + semantic codebase search
- **Env**: `OPENAI_API_KEY`, `ZILLIZ_API_KEY` (optional)
- **Profiles**: knowledge-base, blockchain

## Context & Memory

### context-mode
- **Package**: `context-mode`
- **Purpose**: Sandbox tool outputs to prevent context bloat with up to 98% token reduction
- **Env**: none
- **Profiles**: all

### memsearch
- **Command**: `memsearch serve`
- **Purpose**: Persistent markdown-first memory with hybrid vector + BM25 search across sessions
- **Env**: none (requires `pip install memsearch`)
- **Profiles**: knowledge-base, research, web-dev, blockchain

### skill-seekers
- **Command**: `skill-seekers`
- **Purpose**: Transforms source types into structured AI knowledge for ingestion pipelines
- **Env**: none (requires `pip install skill-seekers`)
- **Profiles**: knowledge-base

## Browser Automation

### puppeteer
- **Package**: `@modelcontextprotocol/server-puppeteer`
- **Purpose**: Headless browser with anti-detection
- **Env**: none
- **Profiles**: research, web-dev

## Database

### supabase
- **Package**: `@supabase/mcp-server-supabase`
- **Purpose**: Supabase integration — database, auth, storage, edge functions
- **Env**: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`
- **Profiles**: knowledge-base, web-dev, full

### postgres
- **Package**: `@modelcontextprotocol/server-postgres`
- **Purpose**: Direct PostgreSQL database operations and queries
- **Env**: `POSTGRES_URL`
- **Profiles**: knowledge-base, web-dev, full

## Integrations

### notion
- **Package**: `@notionhq/notion-mcp-server`
- **Purpose**: Notion workspace integration
- **Env**: `NOTION_TOKEN`
- **Profiles**: research

### clickup
- **Type**: HTTP MCP
- **URL**: `https://mcp.clickup.com/mcp`
- **Purpose**: ClickUp task management
- **Env**: none (OAuth-based)
- **Profiles**: full only

## Blockchain

### helius
- **Package**: `@dcspark/mcp-server-helius`
- **Purpose**: Solana blockchain data, transactions, Jupiter swaps
- **Env**: `HELIUS_API_KEY`
- **Profiles**: blockchain

## Social Media

### twitter
- **Package**: `@mbelinky/x-mcp-server`
- **Purpose**: Twitter/X automation
- **Env**: `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`
- **Profiles**: blockchain
