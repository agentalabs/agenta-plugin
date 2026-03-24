#!/usr/bin/env bash
set -euo pipefail

# Agenta Plugin Installer
# Assembles a .mcp.json from a selected profile and copies relevant skills.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILES_DIR="$SCRIPT_DIR/profiles"
TEMPLATES_DIR="$SCRIPT_DIR/templates"
SKILLS_DIR="$SCRIPT_DIR/skills"
TARGET_DIR="${1:-.}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║       Agenta Plugin Installer        ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
    echo ""
}

print_profiles() {
    echo -e "${YELLOW}Available profiles:${NC}"
    echo ""
    echo "  1) core            - Essential MCPs (sandbox, memory, reasoning, HTTP)"
    echo "  2) knowledge-base  - RAG pipelines, vector search, document management"
    echo "  3) research        - Multi-source search, scraping, synthesis"
    echo "  4) web-dev         - Full-stack development with browser automation"
    echo "  5) blockchain      - Solana development with Helius, Jupiter, Twitter"
    echo "  6) full            - Everything combined"
    echo ""
}

select_profile() {
    local choice
    read -rp "Select a profile [1-6]: " choice
    case "$choice" in
        1) PROFILE="core" ;;
        2) PROFILE="knowledge-base" ;;
        3) PROFILE="research" ;;
        4) PROFILE="web-dev" ;;
        5) PROFILE="blockchain" ;;
        6) PROFILE="full" ;;
        *)
            echo -e "${RED}Invalid choice. Exiting.${NC}"
            exit 1
            ;;
    esac
}

copy_template() {
    local template_file="$TEMPLATES_DIR/${PROFILE}.mcp.json"
    local target_file="$TARGET_DIR/.mcp.json"

    if [ ! -f "$template_file" ]; then
        echo -e "${RED}Template not found: $template_file${NC}"
        exit 1
    fi

    if [ -f "$target_file" ]; then
        echo -e "${YELLOW}Warning: .mcp.json already exists at $target_file${NC}"
        read -rp "Overwrite? [y/N]: " overwrite
        if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
            echo "Skipping .mcp.json copy."
            return
        fi
    fi

    cp "$template_file" "$target_file"
    echo -e "${GREEN}Copied ${PROFILE}.mcp.json -> $target_file${NC}"
}

copy_skills() {
    local profile_file="$PROFILES_DIR/${PROFILE}.json"
    local target_skills_dir="$TARGET_DIR/skills"

    if [ ! -f "$profile_file" ]; then
        echo -e "${RED}Profile not found: $profile_file${NC}"
        exit 1
    fi

    # Parse skills from profile JSON
    local skills
    skills=$(python3 -c "
import json, sys
with open('$profile_file') as f:
    profile = json.load(f)
skills = profile.get('skills', [])
# If profile extends core, add core skills
if 'extends' in profile:
    with open('$PROFILES_DIR/' + profile['extends'] + '.json') as f:
        base = json.load(f)
    skills = list(set(skills + base.get('skills', [])))
for s in skills:
    print(s)
" 2>/dev/null) || true

    if [ -z "$skills" ]; then
        echo "No skills to copy for this profile."
        return
    fi

    mkdir -p "$target_skills_dir"
    while IFS= read -r skill; do
        local skill_file="$SKILLS_DIR/${skill}.md"
        if [ -f "$skill_file" ]; then
            cp "$skill_file" "$target_skills_dir/"
            echo -e "${GREEN}  Copied skill: ${skill}.md${NC}"
        else
            echo -e "${YELLOW}  Skill not found: ${skill}.md (skipped)${NC}"
        fi
    done <<< "$skills"
}

generate_claude_md() {
    local target_file="$TARGET_DIR/CLAUDE.md"

    if [ -f "$target_file" ]; then
        echo -e "${YELLOW}CLAUDE.md already exists. Skipping.${NC}"
        return
    fi

    cat > "$target_file" << 'CLAUDE_EOF'
# Agenta Plugin — Agent Instructions

This project uses Agenta Plugin. The `.mcp.json` file configures which MCP servers are available as tools.

## Tool Usage Priority

When completing tasks, prefer MCP tools over manual approaches:

| Need | Use | Not |
|------|-----|-----|
| Look up library docs | Context7 or mcpdoc | Guessing from training data |
| Search the web | Omnisearch | Telling the user to search |
| Store structured data | SQLite, Supabase, or Postgres | Flat files |
| Store embeddings | Qdrant or Claude Context | Re-computing every time |
| Track entities & relations | MemoryGraph | Unstructured notes |
| Run untrusted code | E2B or Daytona sandbox | Directly on the host |
| Fetch URLs | Fetch MCP | curl via shell |
| Scrape web pages | Crawl4AI | Manual copy-paste |
| Complex reasoning | Sequential Thinking | Long unstructured chains |

## Knowledge Base Maintenance

If this project maintains a knowledge base, follow the incremental sync pattern:
1. Check source registry (SQLite) for sources due for sync
2. Fetch content, compare hash to last known — skip if unchanged
3. Chunk, embed, deduplicate (similarity > 0.95 = skip), upsert
4. Update registry with new timestamp and hash
5. Log results: sources_checked, items_added, items_skipped, errors

## Skills

Skills in `skills/` auto-apply based on file patterns in their YAML frontmatter.

## Environment

Missing API keys cause individual MCP servers to fail gracefully — the rest still work.
CLAUDE_EOF

    echo -e "${GREEN}Generated CLAUDE.md${NC}"
}

check_env_vars() {
    local profile_file="$PROFILES_DIR/${PROFILE}.json"
    local missing=()

    local required
    required=$(python3 -c "
import json
with open('$profile_file') as f:
    profile = json.load(f)
# Include base profile env if extends
if 'extends' in profile:
    with open('$PROFILES_DIR/' + profile['extends'] + '.json') as f:
        base = json.load(f)
    reqs = list(set(profile.get('env_required', []) + base.get('env_required', [])))
else:
    reqs = profile.get('env_required', [])
for r in reqs:
    print(r)
" 2>/dev/null) || true

    if [ -z "$required" ]; then
        return
    fi

    echo ""
    echo -e "${YELLOW}Checking required environment variables:${NC}"
    while IFS= read -r var; do
        if [ -z "${!var:-}" ]; then
            missing+=("$var")
            echo -e "  ${RED}✗ $var${NC} - not set"
        else
            echo -e "  ${GREEN}✓ $var${NC} - set"
        fi
    done <<< "$required"

    if [ ${#missing[@]} -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}Note: Set missing variables before using the MCP servers that require them.${NC}"
        echo -e "${YELLOW}See docs/env-vars.md for details on obtaining API keys.${NC}"
    fi
}

main() {
    print_header

    # Allow profile to be passed as second argument
    if [ -n "${2:-}" ]; then
        PROFILE="$2"
        case "$PROFILE" in
            core|knowledge-base|research|web-dev|blockchain|full) ;;
            *)
                echo -e "${RED}Unknown profile: $PROFILE${NC}"
                echo "Valid profiles: core, knowledge-base, research, web-dev, blockchain, full"
                exit 1
                ;;
        esac
        echo -e "Using profile: ${GREEN}${PROFILE}${NC}"
    else
        print_profiles
        select_profile
    fi

    echo ""
    echo -e "Installing profile ${GREEN}${PROFILE}${NC} to ${BLUE}${TARGET_DIR}${NC}"
    echo ""

    # Step 1: Copy template .mcp.json
    copy_template

    # Step 2: Copy relevant skills
    echo ""
    echo -e "${YELLOW}Copying skills:${NC}"
    copy_skills

    # Step 3: Generate CLAUDE.md if not present
    echo ""
    generate_claude_md

    # Step 4: Check environment variables
    check_env_vars

    echo ""
    echo -e "${GREEN}Installation complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Set any missing environment variables"
    echo "  2. Review .mcp.json and customize as needed"
    echo "  3. Start Claude Code in your project directory"
    echo ""
}

main "$@"
