"""Tests for pre-built template .mcp.json files in templates/."""

import pytest

from conftest import ROOT, PROFILES, PROFILE_MATRIX, load_json

TEMPLATES_DIR = ROOT / "templates"
MCPS_DIR = ROOT / "mcps"


class TestTemplateCompleteness:

    @pytest.mark.parametrize("profile_name", PROFILES)
    def test_template_exists(self, profile_name):
        path = TEMPLATES_DIR / f"{profile_name}.mcp.json"
        assert path.exists(), f"Missing template: templates/{profile_name}.mcp.json"

    def test_no_extra_templates(self):
        actual = {p.stem.replace(".mcp", "") for p in TEMPLATES_DIR.glob("*.mcp.json")}
        expected = set(PROFILES)
        extra = actual - expected
        assert not extra, f"Unexpected templates: {extra}"


class TestTemplateStructure:

    @pytest.fixture(params=PROFILES)
    def template(self, request):
        name = request.param
        data = load_json(TEMPLATES_DIR / f"{name}.mcp.json")
        return name, data

    def test_has_mcpservers_key(self, template):
        name, data = template
        assert "mcpServers" in data, f"Template {name} missing 'mcpServers' key"

    def test_mcpservers_is_dict(self, template):
        name, data = template
        assert isinstance(data["mcpServers"], dict)

    def test_no_extra_top_level_keys(self, template):
        name, data = template
        extra = set(data.keys()) - {"mcpServers"}
        assert not extra, f"Template {name} has unexpected top-level keys: {extra}"


class TestTemplateMatchesMatrix:
    """Each template must contain exactly the MCPs specified by the profile matrix."""

    @pytest.mark.parametrize("profile_name", PROFILES)
    def test_mcp_set_matches(self, profile_name):
        data = load_json(TEMPLATES_DIR / f"{profile_name}.mcp.json")
        actual = set(data["mcpServers"].keys())
        expected = PROFILE_MATRIX[profile_name]
        assert actual == expected, (
            f"Template {profile_name} MCP mismatch.\n"
            f"  Missing: {expected - actual}\n"
            f"  Extra:   {actual - expected}"
        )


class TestTemplateConfigConsistency:
    """Template MCP configs should be consistent with the individual fragments."""

    @pytest.mark.parametrize("profile_name", PROFILES)
    def test_configs_match_fragments(self, profile_name):
        """Each MCP entry in a template should match its fragment, except mcpdoc
        which may have profile-specific --urls args."""
        data = load_json(TEMPLATES_DIR / f"{profile_name}.mcp.json")

        for mcp_name, mcp_config in data["mcpServers"].items():
            fragment_path = MCPS_DIR / f"{mcp_name}.json"
            if not fragment_path.exists():
                # context7 doesn't have its own fragment file — it's referenced
                # but only appears in templates. Skip if missing.
                continue

            fragment = load_json(fragment_path)

            # mcpdoc is special — profile templates may add --urls args
            if mcp_name == "mcpdoc":
                assert mcp_config["command"] == fragment["command"], (
                    f"Template {profile_name}: mcpdoc command mismatch"
                )
                continue

            # For all others, command must match
            if "command" in fragment:
                assert mcp_config.get("command") == fragment["command"], (
                    f"Template {profile_name}: {mcp_name} command mismatch"
                )

            # Type+URL for HTTP MCPs
            if "type" in fragment:
                assert mcp_config.get("type") == fragment["type"]
                assert mcp_config.get("url") == fragment["url"]

            # Env keys must match (values are templates)
            frag_env_keys = set(fragment.get("env", {}).keys())
            tmpl_env_keys = set(mcp_config.get("env", {}).keys())
            assert tmpl_env_keys == frag_env_keys, (
                f"Template {profile_name}: {mcp_name} env keys mismatch.\n"
                f"  Fragment: {frag_env_keys}\n"
                f"  Template: {tmpl_env_keys}"
            )

    @pytest.mark.parametrize("profile_name", PROFILES)
    def test_no_hardcoded_secrets(self, profile_name):
        """No template should contain actual API keys."""
        data = load_json(TEMPLATES_DIR / f"{profile_name}.mcp.json")
        for mcp_name, config in data["mcpServers"].items():
            env = config.get("env", {})
            for key, val in env.items():
                assert val.startswith("${") and val.endswith("}"), (
                    f"Template {profile_name}: {mcp_name}.env.{key} "
                    f"looks like a hardcoded secret: {val[:20]}..."
                )
