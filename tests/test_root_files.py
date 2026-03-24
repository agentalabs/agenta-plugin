"""Tests for root-level metadata files: plugin.json, marketplace.json, CLAUDE.md, README.md."""

import re

import pytest

from conftest import ROOT, PROFILES, ALL_MCP_NAMES, ALL_SKILL_NAMES, load_json


class TestPluginJson:

    @pytest.fixture
    def plugin(self):
        return load_json(ROOT / "plugin.json")

    def test_version_is_2(self, plugin):
        assert plugin["version"].startswith("2."), (
            "plugin.json should be version 2.x after the modular rewrite"
        )

    def test_has_required_fields(self, plugin):
        for field in ("name", "version", "description", "author", "license"):
            assert field in plugin, f"plugin.json missing '{field}'"

    def test_profiles_listed(self, plugin):
        assert "profiles" in plugin
        assert set(plugin["profiles"]) == set(PROFILES)

    def test_capabilities_accurate(self, plugin):
        caps = plugin["capabilities"]
        assert caps["mcpServers"] >= len(ALL_MCP_NAMES) - 1  # context7 only in templates
        assert caps["profiles"] == len(PROFILES)
        assert caps["skills"] == len(ALL_SKILL_NAMES)
        assert caps["templates"] == len(PROFILES)

    def test_description_not_solana_only(self, plugin):
        """Description should reflect the general-purpose nature."""
        desc = plugin["description"].lower()
        assert "modular" in desc or "collection" in desc or "profile" in desc, (
            "plugin.json description should mention modular/profile nature"
        )

    def test_keywords_include_new_domains(self, plugin):
        kw = set(plugin.get("keywords", []))
        assert "mcp" in kw
        assert "knowledge-base" in kw or "research" in kw


class TestMarketplaceJson:

    @pytest.fixture
    def marketplace(self):
        return load_json(ROOT / "marketplace.json")

    def test_version_is_2(self, marketplace):
        assert marketplace["metadata"]["version"].startswith("2.")

    def test_has_plugins_array(self, marketplace):
        assert "plugins" in marketplace
        assert len(marketplace["plugins"]) >= 1

    def test_plugin_entry_has_required_fields(self, marketplace):
        for plugin in marketplace["plugins"]:
            for field in ("name", "description", "version"):
                assert field in plugin, f"marketplace plugin entry missing '{field}'"


class TestClaudeMd:

    @pytest.fixture
    def claude_md(self):
        return (ROOT / "CLAUDE.md").read_text()

    def test_exists(self):
        assert (ROOT / "CLAUDE.md").exists()

    def test_has_title(self, claude_md):
        assert claude_md.startswith("#")

    def test_mentions_mcp(self, claude_md):
        assert "MCP" in claude_md or "mcp" in claude_md

    def test_mentions_skills(self, claude_md):
        assert "skill" in claude_md.lower()


class TestReadme:

    @pytest.fixture
    def readme(self):
        return (ROOT / "README.md").read_text()

    def test_exists(self):
        assert (ROOT / "README.md").exists()

    def test_title_is_agenta_plugin(self, readme):
        first_line = readme.split("\n")[0]
        assert "Agenta Plugin" in first_line

    def test_not_solana_only_title(self, readme):
        first_line = readme.split("\n")[0]
        assert "Solana" not in first_line, (
            "README title should be general-purpose, not Solana-specific"
        )

    def test_lists_all_profiles(self, readme):
        for profile in PROFILES:
            assert profile in readme, f"README should mention profile '{profile}'"

    def test_has_quick_start(self, readme):
        assert "Quick Start" in readme or "quick start" in readme.lower()

    def test_has_install_instructions(self, readme):
        assert "install.sh" in readme

    def test_references_existing_docs(self, readme):
        """Any doc links should point to files that exist."""
        doc_refs = re.findall(r'\(docs/([^)]+)\)', readme)
        for ref in doc_refs:
            path = ROOT / "docs" / ref
            assert path.exists(), f"README references non-existent doc: docs/{ref}"
