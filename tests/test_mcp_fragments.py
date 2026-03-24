"""Tests for individual MCP server configuration fragments in mcps/."""

import pytest

from conftest import ROOT, ALL_MCP_NAMES, load_json

MCPS_DIR = ROOT / "mcps"


class TestMcpFragmentCompleteness:
    """Every MCP in the canonical list has a corresponding fragment file."""

    @pytest.mark.parametrize("mcp_name", ALL_MCP_NAMES)
    def test_fragment_exists(self, mcp_name):
        path = MCPS_DIR / f"{mcp_name}.json"
        assert path.exists(), f"Missing MCP fragment: mcps/{mcp_name}.json"

    def test_no_extra_fragments(self):
        """No unexpected MCP files that aren't in the canonical list."""
        actual = {p.stem for p in MCPS_DIR.glob("*.json")}
        expected = set(ALL_MCP_NAMES)
        extra = actual - expected
        assert not extra, f"Unexpected MCP fragments: {extra}"


class TestMcpFragmentStructure:
    """Each MCP fragment must have valid config shape."""

    @pytest.fixture(params=ALL_MCP_NAMES)
    def mcp_data(self, request):
        name = request.param
        path = MCPS_DIR / f"{name}.json"
        return name, load_json(path)

    def test_has_transport_method(self, mcp_data):
        """Each MCP must have either 'command' (stdio) or 'type'+'url' (http)."""
        name, data = mcp_data
        has_command = "command" in data
        has_http = data.get("type") == "http" and "url" in data
        assert has_command or has_http, (
            f"mcps/{name}.json must have 'command' or 'type:http'+'url'"
        )

    def test_has_description(self, mcp_data):
        name, data = mcp_data
        assert "description" in data, f"mcps/{name}.json missing 'description'"
        assert len(data["description"]) >= 10, (
            f"mcps/{name}.json description too short"
        )

    def test_command_type_consistency(self, mcp_data):
        """If command is 'npx', args must start with ['-y', ...]."""
        name, data = mcp_data
        if data.get("command") == "npx":
            args = data.get("args", [])
            assert len(args) >= 2, f"mcps/{name}.json npx needs args"
            assert args[0] == "-y", f"mcps/{name}.json npx args should start with -y"

    def test_env_values_are_templates(self, mcp_data):
        """Env values should use ${VAR} template syntax, not literal secrets."""
        name, data = mcp_data
        env = data.get("env", {})
        for key, val in env.items():
            assert val.startswith("${") and val.endswith("}"), (
                f"mcps/{name}.json env.{key} should be a ${{VAR}} template, got: {val}"
            )

    def test_no_unexpected_keys(self, mcp_data):
        """MCP fragments should only contain known keys."""
        name, data = mcp_data
        allowed = {"command", "args", "env", "description", "type", "url"}
        unexpected = set(data.keys()) - allowed
        assert not unexpected, (
            f"mcps/{name}.json has unexpected keys: {unexpected}"
        )
