"""Shared fixtures for Agenta Plugin test suite."""

import json
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

PROFILES = ["core", "knowledge-base", "research", "web-dev", "blockchain", "full"]

# The canonical profile → MCP composition matrix from the design doc.
PROFILE_MATRIX = {
    "core": {
        "e2b", "memorygraph", "context-mode",
    },
    "knowledge-base": {
        "e2b", "memorygraph", "context-mode",
        "claude-context", "qdrant", "sqlite", "mcpdoc", "crawl4ai",
        "supabase", "postgres", "memsearch", "skill-seekers",
    },
    "research": {
        "e2b", "memorygraph", "context-mode",
        "mcpdoc", "crawl4ai", "omnisearch", "context7", "notion", "puppeteer",
        "memsearch", "consensus",
    },
    "web-dev": {
        "e2b", "memorygraph", "context-mode",
        "mcpdoc", "omnisearch", "context7", "puppeteer", "daytona",
        "supabase", "postgres", "memsearch", "crawl4ai",
    },
    "blockchain": {
        "e2b", "memorygraph", "context-mode",
        "claude-context", "mcpdoc", "omnisearch", "daytona", "helius", "twitter",
        "memsearch", "context7",
    },
}
# full = union of all + clickup + skill-seekers
PROFILE_MATRIX["full"] = set()
for _mcps in PROFILE_MATRIX.values():
    PROFILE_MATRIX["full"] |= _mcps
PROFILE_MATRIX["full"].add("clickup")
PROFILE_MATRIX["full"].add("skill-seekers")

PROFILE_SKILLS = {
    "core": {"autonomous-agent"},
    "knowledge-base": {"autonomous-agent", "knowledge-base"},
    "research": {"autonomous-agent", "research"},
    "web-dev": {"autonomous-agent", "superpowers", "cloudflare"},
    "blockchain": {"autonomous-agent", "solana-foundation", "solana-ecosystem", "security"},
    "full": {"knowledge-base", "research", "autonomous-agent", "superpowers",
             "solana-foundation", "solana-ecosystem", "security", "cloudflare"},
}

ALL_MCP_NAMES = sorted({
    "e2b", "daytona", "omnisearch", "helius", "memorygraph", "twitter",
    "crawl4ai", "mcpdoc", "claude-context", "clickup",
    "sqlite", "qdrant", "notion",
    "consensus", "puppeteer", "context7", "supabase", "postgres",
    "context-mode", "memsearch", "skill-seekers",
})

# Internal skills are .md files directly in skills/
# Submodule skills are directories in skills/
INTERNAL_SKILL_NAMES = sorted({
    "autonomous-agent", "knowledge-base", "research",
})

# All skill names referenced by profiles (internal + submodule-based)
ALL_SKILL_NAMES = sorted({
    "autonomous-agent", "knowledge-base", "research", "superpowers",
    "solana-foundation", "solana-ecosystem", "security", "cloudflare",
})

# Submodule skill names map to directories
SUBMODULE_SKILLS = {
    "solana-foundation": "solana-foundation",
    "solana-ecosystem": "sendai",
    "security": "trailofbits",
    "cloudflare": "cloudflare",
    "superpowers": "superpowers",
}


@pytest.fixture
def root():
    return ROOT


@pytest.fixture
def mcps_dir():
    return ROOT / "mcps"


@pytest.fixture
def profiles_dir():
    return ROOT / "profiles"


@pytest.fixture
def templates_dir():
    return ROOT / "templates"


@pytest.fixture
def skills_dir():
    return ROOT / "skills"


@pytest.fixture
def docs_dir():
    return ROOT / "docs"


def load_json(path: Path) -> dict:
    """Load and return parsed JSON from a file."""
    with open(path) as f:
        return json.load(f)
