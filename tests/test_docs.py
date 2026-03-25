"""Tests for documentation files in docs/."""

import re

import pytest

from conftest import ROOT, PROFILES, ALL_MCP_NAMES

DOCS_DIR = ROOT / "docs"

EXPECTED_DOCS = ["llms.txt", "profiles.md", "mcp-catalog.md", "env-vars.md", "guide.md"]


class TestDocsCompleteness:

    @pytest.mark.parametrize("filename", EXPECTED_DOCS)
    def test_doc_exists(self, filename):
        assert (DOCS_DIR / filename).exists(), f"Missing doc: docs/{filename}"


class TestLlmsTxt:

    @pytest.fixture
    def llms(self):
        return (DOCS_DIR / "llms.txt").read_text()

    def test_has_title(self, llms):
        assert "Agenta" in llms

    def test_lists_profiles(self, llms):
        for profile in ["core", "knowledge-base", "research", "web-dev", "blockchain"]:
            assert profile in llms

    def test_has_quick_start(self, llms):
        assert "install.sh" in llms or "template" in llms.lower()


class TestProfilesDocs:

    @pytest.fixture
    def profiles_doc(self):
        return (DOCS_DIR / "profiles.md").read_text()

    def test_documents_all_profiles(self, profiles_doc):
        for profile in PROFILES:
            assert profile in profiles_doc, (
                f"docs/profiles.md should document profile '{profile}'"
            )

    def test_has_usage_instructions(self, profiles_doc):
        assert "template" in profiles_doc.lower() or "install" in profiles_doc.lower()


class TestMcpCatalog:

    @pytest.fixture
    def catalog(self):
        return (DOCS_DIR / "mcp-catalog.md").read_text()

    def test_documents_all_mcps(self, catalog):
        """Every MCP should be documented in the catalog."""
        catalog_lower = catalog.lower()
        for mcp in ALL_MCP_NAMES:
            # Normalize: playwright-mcp -> playwright
            search_term = mcp.replace("-mcp", "").replace("-", "")
            assert search_term in catalog_lower.replace("-", ""), (
                f"docs/mcp-catalog.md missing documentation for '{mcp}'"
            )

    def test_has_env_info(self, catalog):
        """Catalog should mention env vars for MCPs that need them."""
        assert "env" in catalog.lower() or "API_KEY" in catalog


class TestEnvVarsDocs:

    @pytest.fixture
    def env_doc(self):
        return (DOCS_DIR / "env-vars.md").read_text()

    def test_has_all_variables_table(self, env_doc):
        assert "E2B_API_KEY" in env_doc
        assert "HELIUS_API_KEY" in env_doc
        assert "OPENAI_API_KEY" in env_doc
        assert "TAVILY_API_KEY" in env_doc

    def test_has_per_profile_section(self, env_doc):
        for profile in ["Core", "Knowledge Base", "Research", "Blockchain"]:
            assert profile in env_doc, (
                f"docs/env-vars.md should have section for '{profile}'"
            )

    def test_documents_optional_vars(self, env_doc):
        for var in ["TWITTER_API_KEY", "NOTION_TOKEN", "QDRANT_URL"]:
            assert var in env_doc, f"docs/env-vars.md missing optional var '{var}'"


class TestGuide:

    @pytest.fixture
    def guide(self):
        return (DOCS_DIR / "guide.md").read_text()

    def test_has_title(self, guide):
        assert guide.startswith("#")

    def test_has_table_of_contents(self, guide):
        assert "Table of Contents" in guide

    def test_covers_all_profiles_as_use_cases(self, guide):
        """Guide should have sections demonstrating each profile."""
        guide_lower = guide.lower()
        assert "knowledge-base" in guide_lower or "knowledge base" in guide_lower
        assert "research" in guide_lower
        assert "web-dev" in guide_lower or "web dev" in guide_lower or "web application" in guide_lower
        assert "blockchain" in guide_lower or "solana" in guide_lower
        assert "core" in guide_lower

    def test_has_installation_steps(self, guide):
        """Each use case should show how to install."""
        assert guide.count("install.sh") >= 5, (
            "Guide should show install.sh usage for each major use case"
        )

    def test_has_env_var_examples(self, guide):
        """Guide should show setting env vars in context."""
        assert "E2B_API_KEY" in guide
        assert "export" in guide

    def test_explains_mcp_tool_usage(self, guide):
        """Guide should explain which MCP tools are used in each flow."""
        for mcp in ["Omnisearch", "Crawl4AI", "MemoryGraph", "Helius", "Puppeteer", "Qdrant"]:
            assert mcp in guide, (
                f"Guide should mention {mcp} in a use case flow"
            )

    def test_has_team_onboarding_section(self, guide):
        assert "team" in guide.lower() or "onboarding" in guide.lower()

    def test_has_custom_profile_section(self, guide):
        assert "custom profile" in guide.lower() or "creating a custom" in guide.lower()

    def test_has_existing_project_section(self, guide):
        assert "existing project" in guide.lower()

    def test_has_minimum_length(self, guide):
        """A proper guide should be substantial."""
        assert len(guide) >= 5000, (
            f"Guide is too short ({len(guide)} chars) for production documentation"
        )

    def test_has_sufficient_sections(self, guide):
        """Should have at least 8 major sections."""
        h2_count = len(re.findall(r"^## ", guide, re.MULTILINE))
        assert h2_count >= 8, (
            f"Guide should have at least 8 major sections, found {h2_count}"
        )

    def test_references_other_docs(self, guide):
        """Guide should cross-reference other documentation files."""
        assert "profiles.md" in guide
        assert "mcp-catalog.md" in guide
        assert "env-vars.md" in guide

    def test_quick_reference_table(self, guide):
        """Should end with a quick-reference lookup table."""
        assert "Quick Reference" in guide or "quick reference" in guide
