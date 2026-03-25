---
description: Research workflow patterns for multi-source search, information synthesis, fact verification, and structured note-taking. Auto-applies when doing research or analysis tasks.
globs:
  - "**/research/**/*"
  - "**/notes/**/*"
  - "**/reports/**/*"
---

# Research Skill

## Overview

Patterns for conducting thorough research using multiple search engines, web scraping, documentation lookup, academic paper search, persistent memory, and structured synthesis.

## When This Skill Applies

- Researching a topic, library, or technology
- Comparing alternatives or solutions
- Fact-checking or verifying claims
- Writing reports or summaries
- Gathering competitive intelligence
- Academic or scientific literature review
- Cross-session research continuity

## Available Tools

- **Omnisearch**: Unified search across Tavily, Exa, and Perplexity
- **Consensus**: Academic paper search across 200M+ peer-reviewed papers
- **Crawl4AI**: Deep web scraping for full page content (primary browsing tool)
- **Puppeteer**: Headless browser for JavaScript-rendered pages (Crawl4AI fallback)
- **WebFetch**: Native HTTP requests for APIs and structured data (final fallback)
- **mcpdoc**: Documentation lookup via llms.txt
- **Context7**: Live documentation for popular libraries
- **Notion**: Store and organize research notes
- **Memsearch**: Persistent cross-session memory with hybrid vector + BM25 search
- **MemoryGraph**: Knowledge graph for entities and relationships

## Research Workflow

### 1. Define the Question

- State the research question precisely
- Identify what type of answer is needed (factual, comparative, exploratory, academic)
- Set scope boundaries (time range, sources, depth)
- Check Memsearch for prior research on this or related topics

### 2. Multi-Source Search

Execute searches across multiple engines for coverage:

- **Tavily** (via Omnisearch): Best for recent, factual results
- **Exa** (via Omnisearch): Best for semantic similarity and finding related content
- **Perplexity** (via Omnisearch): Best for synthesized answers with citations
- **Consensus**: Best for scientific claims, peer-reviewed evidence, and academic literature
- **Context7**: Best for library/framework documentation
- **mcpdoc**: Best for projects that publish llms.txt

### 3. Deep Dive

For promising results, go deeper:

- Use Crawl4AI to extract full page content
- Use Puppeteer for JavaScript-rendered pages that Crawl4AI cannot handle
- Use WebFetch for API endpoints and structured data
- Follow citation chains for primary sources

### 4. Synthesis

Combine findings into structured output:

- Cross-reference claims across sources
- Note contradictions or disagreements
- Identify consensus and confidence levels
- Attribute all claims to sources

### 5. Output

Format research as:

- **Summary**: Key findings in 3-5 bullets
- **Details**: Organized by subtopic
- **Sources**: All URLs and references
- **Gaps**: What couldn't be determined

### 6. Persist Findings

Store key findings for cross-session continuity:

- Save to Memsearch with descriptive tags and metadata
- Update MemoryGraph with entities and relationships discovered
- Record source URLs and retrieval dates for future verification

## Browsing Fallback Chain

When you need to fetch or render web content, follow this escalation pattern:

1. **Crawl4AI** (first choice) — Free, self-hosted, handles anti-bot measures. Use for most web scraping needs including articles, documentation, and data extraction.

2. **Puppeteer** (fallback) — Use when Crawl4AI fails or when the page requires JavaScript rendering (SPAs, dynamic content, interactive elements, pages behind client-side routing).

3. **WebFetch** (final fallback) — Use Claude Code's native WebFetch for simple HTTP requests, APIs, JSON endpoints, or when both Crawl4AI and Puppeteer are unavailable. No JavaScript rendering.

**When to skip directly to Puppeteer:**
- Known SPA frameworks (React/Vue/Angular apps without SSR)
- Pages that require interaction (clicking, scrolling, form filling)
- Sites with aggressive anti-scraping that Crawl4AI can't handle
- Pricing pages and dashboards with dynamic content

## Academic Research Workflow

For research requiring scientific evidence or peer-reviewed sources:

### Step 1: Consensus Search

Start with Consensus for the core scientific question. Consensus searches 200M+ academic papers and provides:
- Paper titles, authors, and publication details
- Key findings and abstracts
- Consensus meters showing scientific agreement levels

### Step 2: Deep Read with Crawl4AI/Puppeteer

For the most relevant papers found via Consensus:
- Use Crawl4AI to scrape full paper content from open-access sources
- Use Puppeteer for papers behind paywalls that offer HTML previews
- Extract methodology, data, and specific findings

### Step 3: Broaden with Omnisearch

Fill gaps that academic papers don't cover:
- Industry reports and whitepapers
- Blog posts from domain experts
- News coverage and real-world applications

### Step 4: Persist to Memsearch

Store the research session findings:
- Key papers with citations and DOIs
- Summary of scientific consensus
- Open questions and contradictions
- Tags for easy retrieval in future sessions

## Cross-Session Research Memory

Use Memsearch to maintain research continuity across conversations:

### Saving Research

After completing a research task:
- Store findings as structured notes with clear titles
- Include source URLs, retrieval dates, and confidence levels
- Tag with topic keywords for future retrieval
- Record what questions remain unanswered

### Retrieving Prior Research

At the start of a research task:
- Query Memsearch for related prior findings
- Check if the question has been partially or fully answered before
- Build on previous work rather than starting from scratch
- Verify that previously stored findings are still current

### Updating Stale Research

When revisiting a topic:
- Compare new findings against stored Memsearch entries
- Update entries that have become outdated
- Record the date of the update and what changed
- Flag conflicting information between old and new sources

## Search Strategy Patterns

### Exploratory Research

Cast a wide net, then narrow:
1. Broad search across all engines
2. Identify key themes and subtopics
3. Targeted deep dives per subtopic
4. Synthesize across all findings

### Comparative Analysis

Structure around alternatives:
1. Identify all candidates
2. Define comparison criteria
3. Research each candidate against criteria
4. Build comparison matrix
5. Highlight trade-offs

### Fact Verification

Require multiple independent sources:
1. Find the original claim and its source
2. Search for independent corroboration
3. Check for contradicting evidence
4. Assess source credibility
5. Rate confidence level

### Scientific Literature Review

Use Consensus as the primary tool:
1. Search Consensus for the core scientific question
2. Review the consensus meter and top papers
3. Deep-read the 3-5 most cited/relevant papers
4. Cross-reference with Omnisearch for recent developments
5. Store findings in Memsearch with DOIs and citations

## Best Practices

- Always cite sources with URLs
- Distinguish between facts, opinions, and speculation
- Note the publication date of sources
- Prefer primary sources over secondary
- Cross-reference at least 2-3 sources for key claims
- Be explicit about confidence levels
- Use Consensus for any scientific or medical claims — do not rely on web search alone
- Store research findings in Memsearch for cross-session persistence
- Use MemoryGraph for tracking entity relationships discovered during research
- Follow the browsing fallback chain: Crawl4AI → Puppeteer → WebFetch
- When citing academic papers, include DOI or publication details when available
