---
description: Research workflow patterns for multi-source search, information synthesis, fact verification, and structured note-taking. Auto-applies when doing research or analysis tasks.
globs:
  - "**/research/**/*"
  - "**/notes/**/*"
  - "**/reports/**/*"
---

# Research Skill

## Overview

Patterns for conducting thorough research using multiple search engines, web scraping, documentation lookup, and structured synthesis.

## When This Skill Applies

- Researching a topic, library, or technology
- Comparing alternatives or solutions
- Fact-checking or verifying claims
- Writing reports or summaries
- Gathering competitive intelligence

## Available Tools

- **Omnisearch**: Unified search across Tavily, Exa, and Perplexity
- **Crawl4AI**: Deep web scraping for full page content
- **mcpdoc**: Documentation lookup via llms.txt
- **Context7**: Live documentation for popular libraries
- **Notion**: Store and organize research notes
- **Puppeteer**: Browser automation for dynamic content
- **Fetch**: Direct HTTP requests for APIs and data

## Research Workflow

### 1. Define the Question

- State the research question precisely
- Identify what type of answer is needed (factual, comparative, exploratory)
- Set scope boundaries (time range, sources, depth)

### 2. Multi-Source Search

Execute searches across multiple engines for coverage:

- **Tavily** (via Omnisearch): Best for recent, factual results
- **Exa** (via Omnisearch): Best for semantic similarity and finding related content
- **Perplexity** (via Omnisearch): Best for synthesized answers with citations
- **Context7**: Best for library/framework documentation
- **mcpdoc**: Best for projects that publish llms.txt

### 3. Deep Dive

For promising results, go deeper:

- Use Crawl4AI to extract full page content
- Use Puppeteer for JavaScript-rendered pages
- Use Fetch for API endpoints and structured data
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

## Best Practices

- Always cite sources with URLs
- Distinguish between facts, opinions, and speculation
- Note the publication date of sources
- Prefer primary sources over secondary
- Cross-reference at least 2-3 sources for key claims
- Be explicit about confidence levels
- Store research findings in Notion or MemoryGraph for persistence
