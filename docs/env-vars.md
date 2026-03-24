# Environment Variables Reference

All environment variables used by Agenta Plugin MCP servers.

## Required by Profile

### Core
| Variable | MCP | Description |
|----------|-----|-------------|
| `E2B_API_KEY` | e2b | E2B cloud sandbox API key |

### Knowledge Base
| Variable | MCP | Description |
|----------|-----|-------------|
| `E2B_API_KEY` | e2b | E2B cloud sandbox API key |
| `OPENAI_API_KEY` | claude-context | OpenAI API key for embeddings |

### Research
| Variable | MCP | Description |
|----------|-----|-------------|
| `E2B_API_KEY` | e2b | E2B cloud sandbox API key |
| `TAVILY_API_KEY` | omnisearch | Tavily search API key |

### Web Dev
| Variable | MCP | Description |
|----------|-----|-------------|
| `E2B_API_KEY` | e2b | E2B cloud sandbox API key |

### Blockchain
| Variable | MCP | Description |
|----------|-----|-------------|
| `E2B_API_KEY` | e2b | E2B cloud sandbox API key |
| `HELIUS_API_KEY` | helius | Helius RPC API key |
| `OPENAI_API_KEY` | claude-context | OpenAI API key for embeddings |

## All Variables

| Variable | MCP Server | Required By | Description |
|----------|-----------|-------------|-------------|
| `E2B_API_KEY` | e2b | all profiles | E2B cloud sandbox |
| `OPENAI_API_KEY` | claude-context | knowledge-base, blockchain | OpenAI embeddings |
| `ZILLIZ_API_KEY` | claude-context | — (optional) | Zilliz/Milvus vector storage |
| `HELIUS_API_KEY` | helius | blockchain | Solana RPC via Helius |
| `TAVILY_API_KEY` | omnisearch | research | Tavily search engine |
| `EXA_API_KEY` | omnisearch | — (optional) | Exa semantic search |
| `PERPLEXITY_API_KEY` | omnisearch | — (optional) | Perplexity AI search |
| `QDRANT_URL` | qdrant | — (optional) | Qdrant server URL |
| `QDRANT_API_KEY` | qdrant | — (optional) | Qdrant authentication |
| `NOTION_TOKEN` | notion | — (optional) | Notion integration token |
| `TWITTER_API_KEY` | twitter | — (optional) | Twitter API key |
| `TWITTER_API_SECRET` | twitter | — (optional) | Twitter API secret |
| `TWITTER_ACCESS_TOKEN` | twitter | — (optional) | Twitter access token |
| `TWITTER_ACCESS_TOKEN_SECRET` | twitter | — (optional) | Twitter access token secret |
| `SUPABASE_URL` | supabase | — (optional) | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | supabase | — (optional) | Supabase service role key |
| `POSTGRES_URL` | postgres | — (optional) | PostgreSQL connection string |

## Getting API Keys

| Service | Free Tier | Sign Up |
|---------|-----------|---------|
| E2B | Yes | https://e2b.dev |
| OpenAI | Pay-per-use | https://platform.openai.com |
| Helius | 1M credits free | https://helius.dev |
| Tavily | Limited free | https://tavily.com |
| Exa | Limited free | https://exa.ai |
| Perplexity | Paid | https://perplexity.ai |
| Qdrant | Free (self-hosted) | https://qdrant.tech |
| Notion | Free | https://developers.notion.com |
| Twitter/X | Paid | https://developer.twitter.com |
| Supabase | Free tier | https://supabase.com |
| PostgreSQL | Free (self-hosted) | https://postgresql.org |
