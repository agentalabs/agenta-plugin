"""Tests for profile manifests in profiles/."""

import pytest

from conftest import (
    ROOT, PROFILES, ALL_MCP_NAMES, ALL_SKILL_NAMES,
    PROFILE_MATRIX, PROFILE_SKILLS, load_json,
)

PROFILES_DIR = ROOT / "profiles"
MCPS_DIR = ROOT / "mcps"
SKILLS_DIR = ROOT / "skills"


class TestProfileCompleteness:
    """All expected profiles exist and no extras."""

    @pytest.mark.parametrize("profile_name", PROFILES)
    def test_profile_exists(self, profile_name):
        path = PROFILES_DIR / f"{profile_name}.json"
        assert path.exists(), f"Missing profile: profiles/{profile_name}.json"

    def test_no_extra_profiles(self):
        actual = {p.stem for p in PROFILES_DIR.glob("*.json")}
        expected = set(PROFILES)
        extra = actual - expected
        assert not extra, f"Unexpected profiles: {extra}"


class TestProfileSchema:
    """Each profile must have required fields with correct types."""

    @pytest.fixture(params=PROFILES)
    def profile(self, request):
        name = request.param
        data = load_json(PROFILES_DIR / f"{name}.json")
        return name, data

    def test_required_fields(self, profile):
        name, data = profile
        assert "name" in data
        assert "description" in data
        assert "mcps" in data
        assert "skills" in data

    def test_name_matches_filename(self, profile):
        name, data = profile
        assert data["name"] == name

    def test_mcps_is_list_of_strings(self, profile):
        name, data = profile
        assert isinstance(data["mcps"], list)
        for mcp in data["mcps"]:
            assert isinstance(mcp, str), f"Profile {name}: mcp entry must be string"

    def test_skills_is_list_of_strings(self, profile):
        name, data = profile
        assert isinstance(data["skills"], list)
        for skill in data["skills"]:
            assert isinstance(skill, str)

    def test_env_fields_are_lists(self, profile):
        name, data = profile
        for field in ("env_required", "env_optional"):
            if field in data:
                assert isinstance(data[field], list), (
                    f"Profile {name}: {field} must be a list"
                )

    def test_extends_references_valid_profile(self, profile):
        name, data = profile
        if "extends" in data:
            base = data["extends"]
            assert base in PROFILES, (
                f"Profile {name} extends unknown profile '{base}'"
            )
            # Base profile must exist
            assert (PROFILES_DIR / f"{base}.json").exists()

    def test_core_has_no_extends(self, profile):
        """Core is the root — it should not extend anything."""
        name, data = profile
        if name == "core":
            assert "extends" not in data, "Core profile should not extend another"

    def test_non_core_extends_core(self, profile):
        """All non-core profiles should extend core."""
        name, data = profile
        if name != "core":
            assert data.get("extends") == "core", (
                f"Profile {name} should extend 'core'"
            )


class TestProfileReferences:
    """All MCPs and skills referenced by profiles must actually exist."""

    @pytest.fixture(params=PROFILES)
    def profile_data(self, request):
        name = request.param
        return name, load_json(PROFILES_DIR / f"{name}.json")

    def test_mcps_reference_existing_fragments(self, profile_data):
        name, data = profile_data
        for mcp in data["mcps"]:
            path = MCPS_DIR / f"{mcp}.json"
            assert path.exists(), (
                f"Profile {name} references non-existent MCP '{mcp}'"
            )

    def test_skills_reference_existing_files(self, profile_data):
        name, data = profile_data
        for skill in data["skills"]:
            path = SKILLS_DIR / f"{skill}.md"
            assert path.exists(), (
                f"Profile {name} references non-existent skill '{skill}'"
            )


class TestProfileMatrix:
    """Verify profiles match the canonical composition matrix."""

    @pytest.mark.parametrize("profile_name", PROFILES)
    def test_resolved_mcps_match_matrix(self, profile_name):
        """Profile MCPs (including inherited from extends) must match the matrix."""
        data = load_json(PROFILES_DIR / f"{profile_name}.json")

        # Resolve: own mcps + base mcps
        resolved = set(data["mcps"])
        if "extends" in data:
            base = load_json(PROFILES_DIR / f"{data['extends']}.json")
            resolved |= set(base["mcps"])

        expected = PROFILE_MATRIX[profile_name]
        assert resolved == expected, (
            f"Profile {profile_name} MCP mismatch.\n"
            f"  Missing: {expected - resolved}\n"
            f"  Extra:   {resolved - expected}"
        )

    @pytest.mark.parametrize("profile_name", PROFILES)
    def test_resolved_skills_match_expected(self, profile_name):
        """Profile skills (including inherited) must match expected set."""
        data = load_json(PROFILES_DIR / f"{profile_name}.json")

        resolved = set(data["skills"])
        if "extends" in data:
            base = load_json(PROFILES_DIR / f"{data['extends']}.json")
            resolved |= set(base["skills"])

        expected = PROFILE_SKILLS[profile_name]
        assert resolved == expected, (
            f"Profile {profile_name} skills mismatch.\n"
            f"  Missing: {expected - resolved}\n"
            f"  Extra:   {resolved - expected}"
        )
