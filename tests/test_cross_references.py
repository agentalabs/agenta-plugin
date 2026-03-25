"""Cross-reference integrity tests — ensures all internal references are consistent."""

import json
import re
from pathlib import Path

import pytest

from conftest import (
    ROOT, PROFILES, ALL_MCP_NAMES, ALL_SKILL_NAMES,
    INTERNAL_SKILL_NAMES, SUBMODULE_SKILLS, load_json,
)


class TestNoOrphanedMcps:
    """Every MCP fragment should be referenced by at least one profile or template."""

    def test_all_fragments_used(self):
        # Collect all MCPs referenced across profiles (including extends)
        referenced = set()
        for profile_name in PROFILES:
            data = load_json(ROOT / "profiles" / f"{profile_name}.json")
            referenced.update(data["mcps"])

        # Also check if core MCPs are implicitly included via extends
        core = load_json(ROOT / "profiles" / "core.json")
        referenced.update(core["mcps"])

        fragments = {p.stem for p in (ROOT / "mcps").glob("*.json")}

        orphaned = fragments - referenced
        assert not orphaned, (
            f"MCP fragments not referenced by any profile: {orphaned}"
        )


class TestNoOrphanedSkills:
    """Every internal skill file should be referenced by at least one profile."""

    def test_all_internal_skills_used(self):
        referenced = set()
        for profile_name in PROFILES:
            data = load_json(ROOT / "profiles" / f"{profile_name}.json")
            referenced.update(data["skills"])

        # Add base profile skills
        for profile_name in PROFILES:
            data = load_json(ROOT / "profiles" / f"{profile_name}.json")
            if "extends" in data:
                base = load_json(ROOT / "profiles" / f"{data['extends']}.json")
                referenced.update(base["skills"])

        # Only check internal .md files (not submodules or SKILL.md)
        skill_files = {
            p.stem for p in (ROOT / "skills").glob("*.md")
            if p.stem != "SKILL"
        }
        orphaned = skill_files - referenced
        assert not orphaned, (
            f"Skill files not referenced by any profile: {orphaned}"
        )


class TestTemplateFragmentConsistency:
    """Templates should use the same package names/commands as fragments."""

    @pytest.mark.parametrize("profile_name", PROFILES)
    def test_template_args_consistency(self, profile_name):
        """For npx-based MCPs, the package name in templates must match fragments."""
        template = load_json(ROOT / "templates" / f"{profile_name}.mcp.json")

        for mcp_name, config in template["mcpServers"].items():
            frag_path = ROOT / "mcps" / f"{mcp_name}.json"
            if not frag_path.exists():
                continue

            fragment = load_json(frag_path)

            # Skip mcpdoc (args differ per profile)
            if mcp_name == "mcpdoc":
                continue

            if "args" in fragment:
                frag_pkg = None
                tmpl_pkg = None

                frag_args = fragment.get("args", [])
                tmpl_args = config.get("args", [])

                # For npx commands, the package is the arg after -y
                if fragment.get("command") == "npx" and len(frag_args) >= 2:
                    frag_pkg = frag_args[1]
                if config.get("command") == "npx" and len(tmpl_args) >= 2:
                    tmpl_pkg = tmpl_args[1]

                if frag_pkg and tmpl_pkg:
                    assert tmpl_pkg == frag_pkg, (
                        f"Template {profile_name}: {mcp_name} package mismatch "
                        f"({tmpl_pkg} vs {frag_pkg})"
                    )


class TestPluginJsonAccuracy:
    """plugin.json capabilities counts should match reality."""

    def test_mcp_count(self):
        plugin = load_json(ROOT / "plugin.json")
        assert plugin["capabilities"]["mcpServers"] == len(ALL_MCP_NAMES)

    def test_profile_count(self):
        plugin = load_json(ROOT / "plugin.json")
        actual = len(list((ROOT / "profiles").glob("*.json")))
        assert plugin["capabilities"]["profiles"] == actual

    def test_skill_count(self):
        plugin = load_json(ROOT / "plugin.json")
        assert plugin["capabilities"]["skills"] == len(ALL_SKILL_NAMES)

    def test_template_count(self):
        plugin = load_json(ROOT / "plugin.json")
        actual = len(list((ROOT / "templates").glob("*.mcp.json")))
        assert plugin["capabilities"]["templates"] == actual


class TestOldFilesRemoved:
    """Verify cleanup of legacy files."""

    def test_old_skill_md_removed(self):
        """The old SKILL.md should have been deleted (moved to skills/)."""
        assert not (ROOT / "SKILL.md").exists(), (
            "Legacy SKILL.md should be removed — content moved to skills/"
        )

    def test_old_solana_removed(self):
        """Old solana-development.md should not exist in skills/ root."""
        assert not (ROOT / "skills" / "solana-development.md").exists(), (
            "solana-development.md was replaced by solana-foundation submodule"
        )


class TestNoCircularExtends:
    """Profile extends chains should not be circular."""

    def test_no_circular_extends(self):
        for profile_name in PROFILES:
            visited = set()
            current = profile_name

            while current:
                assert current not in visited, (
                    f"Circular extends chain detected: {visited} -> {current}"
                )
                visited.add(current)
                data = load_json(ROOT / "profiles" / f"{current}.json")
                current = data.get("extends")
