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
        "e2b", "memorygraph", "sequential-thinking", "fetch",
    },
    "knowledge-base": {
        "e2b", "memorygraph", "sequential-thinking", "fetch",
        "claude-context", "qdrant", "filesystem", "sqlite", "mcpdoc", "crawl4ai",
        "supabase", "postgres",
    },
    "research": {
        "e2b", "memorygraph", "sequential-thinking", "fetch",
        "mcpdoc", "crawl4ai", "omnisearch", "context7", "notion", "puppeteer",
    },
    "web-dev": {
        "e2b", "memorygraph", "sequential-thinking", "fetch",
        "mcpdoc", "omnisearch", "context7", "playwright-mcp", "puppeteer", "daytona",
        "supabase", "postgres",
    },
    "blockchain": {
        "e2b", "memorygraph", "sequential-thinking", "fetch",
        "claude-context", "mcpdoc", "omnisearch", "daytona", "helius", "twitter",
    },
}
# full = union of all + clickup
PROFILE_MATRIX["full"] = set()
for _mcps in PROFILE_MATRIX.values():
    PROFILE_MATRIX["full"] |= _mcps
PROFILE_MATRIX["full"].add("clickup")

PROFILE_SKILLS = {
    "core": {"autonomous-agent"},
    "knowledge-base": {"autonomous-agent", "knowledge-base"},
    "research": {"autonomous-agent", "research"},
    "web-dev": {"autonomous-agent", "web-development"},
    "blockchain": {"autonomous-agent", "solana-development"},
    "full": {"knowledge-base", "research", "autonomous-agent", "solana-development", "web-development"},
}

ALL_MCP_NAMES = sorted({
    "e2b", "daytona", "omnisearch", "helius", "memorygraph", "twitter",
    "crawl4ai", "mcpdoc", "claude-context", "clickup", "filesystem",
    "sqlite", "qdrant", "sequential-thinking", "fetch", "notion",
    "playwright-mcp", "puppeteer", "context7", "supabase", "postgres",
})

ALL_SKILL_NAMES = sorted({
    "autonomous-agent", "knowledge-base", "research",
    "solana-development", "web-development",
})


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
