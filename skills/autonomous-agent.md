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
- **E2B**: Sandboxed code execution for safe experimentation
- **Context Mode**: Sandbox tool outputs to prevent context bloat

## Task Decomposition

### Breaking Down Complex Tasks

1. **Analyze the request**: Identify the end goal and constraints
2. **Identify sub-tasks**: Break into independently completable units
3. **Order by dependency**: Determine which tasks block others
4. **Estimate complexity**: Flag tasks that may need user input
5. **Execute iteratively**: Complete one sub-task, verify, proceed

### Decision Framework

Use structured reasoning for complex decisions:

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
- After complex reasoning: review your reasoning step by step

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

## Best Practices

- Prefer incremental progress over big-bang changes
- Verify assumptions before building on them
- Ask for clarification when requirements are ambiguous
- Use sandboxed execution (E2B) for risky operations
- Document non-obvious decisions for future context
