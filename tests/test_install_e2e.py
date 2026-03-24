"""End-to-end tests for install.sh — runs the installer for each profile and validates output."""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

from conftest import ROOT, PROFILES, PROFILE_MATRIX, PROFILE_SKILLS

INSTALL_SH = ROOT / "install.sh"


def run_installer(target_dir: str, profile: str) -> subprocess.CompletedProcess:
    """Run install.sh with a profile and target directory."""
    return subprocess.run(
        ["bash", str(INSTALL_SH), target_dir, profile],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(ROOT),
    )


class TestInstallerExecution:

    def test_script_is_executable(self):
        assert os.access(INSTALL_SH, os.X_OK), "install.sh must be executable"

    def test_rejects_invalid_profile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_installer(tmpdir, "nonexistent")
            assert result.returncode != 0
            assert "Unknown profile" in result.stdout or "Unknown profile" in result.stderr

    @pytest.mark.parametrize("profile", PROFILES)
    def test_runs_successfully(self, profile):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_installer(tmpdir, profile)
            assert result.returncode == 0, (
                f"install.sh failed for profile {profile}:\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )

    @pytest.mark.parametrize("profile", PROFILES)
    def test_prints_completion_message(self, profile):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_installer(tmpdir, profile)
            assert "Installation complete" in result.stdout


class TestInstallerOutput:
    """Verify the files produced by install.sh."""

    @pytest.fixture(params=PROFILES)
    def installed(self, request, tmp_path):
        """Run installer and return (profile_name, target_dir)."""
        profile = request.param
        target = tmp_path / profile
        target.mkdir()
        result = run_installer(str(target), profile)
        assert result.returncode == 0, f"Installer failed: {result.stderr}"
        return profile, target

    def test_creates_mcp_json(self, installed):
        profile, target = installed
        mcp_file = target / ".mcp.json"
        assert mcp_file.exists(), f"install.sh did not create .mcp.json for {profile}"

    def test_mcp_json_is_valid_json(self, installed):
        profile, target = installed
        mcp_file = target / ".mcp.json"
        with open(mcp_file) as f:
            data = json.load(f)
        assert "mcpServers" in data

    def test_mcp_json_has_correct_servers(self, installed):
        """The generated .mcp.json should match the profile matrix."""
        profile, target = installed
        with open(target / ".mcp.json") as f:
            data = json.load(f)
        actual = set(data["mcpServers"].keys())
        expected = PROFILE_MATRIX[profile]
        assert actual == expected, (
            f"Installed {profile} .mcp.json mismatch.\n"
            f"  Missing: {expected - actual}\n"
            f"  Extra:   {actual - expected}"
        )

    def test_creates_claude_md(self, installed):
        profile, target = installed
        assert (target / "CLAUDE.md").exists()

    def test_claude_md_has_content(self, installed):
        profile, target = installed
        content = (target / "CLAUDE.md").read_text()
        assert len(content) > 100
        assert "MCP" in content

    def test_creates_skills_directory(self, installed):
        profile, target = installed
        assert (target / "skills").is_dir()

    def test_copies_correct_skills(self, installed):
        """Skills directory should contain exactly the skills for this profile."""
        profile, target = installed
        skills_dir = target / "skills"
        actual = {p.stem for p in skills_dir.glob("*.md")}
        expected = PROFILE_SKILLS[profile]
        assert actual == expected, (
            f"Installed {profile} skills mismatch.\n"
            f"  Missing: {expected - actual}\n"
            f"  Extra:   {actual - expected}"
        )

    def test_skill_files_are_complete(self, installed):
        """Copied skill files should not be truncated."""
        profile, target = installed
        for skill_file in (target / "skills").glob("*.md"):
            source = ROOT / "skills" / skill_file.name
            assert skill_file.stat().st_size == source.stat().st_size, (
                f"Skill {skill_file.name} appears truncated "
                f"({skill_file.stat().st_size} vs {source.stat().st_size} bytes)"
            )


class TestInstallerIdempotency:
    """Running installer twice should be safe."""

    def test_does_not_clobber_existing_claude_md(self, tmp_path):
        """If CLAUDE.md already exists, installer should not overwrite it."""
        custom_content = "# My Custom Instructions\nDo not touch this."
        (tmp_path / "CLAUDE.md").write_text(custom_content)

        result = run_installer(str(tmp_path), "core")
        assert result.returncode == 0

        actual = (tmp_path / "CLAUDE.md").read_text()
        assert actual == custom_content, "Installer overwrote existing CLAUDE.md"


class TestInstallerEnvCheck:
    """Installer should report missing env vars."""

    def test_reports_missing_env(self, tmp_path):
        """When E2B_API_KEY is not set, installer should flag it."""
        env = os.environ.copy()
        env.pop("E2B_API_KEY", None)
        result = subprocess.run(
            ["bash", str(INSTALL_SH), str(tmp_path), "core"],
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
            cwd=str(ROOT),
        )
        assert result.returncode == 0  # Should still succeed
        assert "E2B_API_KEY" in result.stdout

    def test_recognizes_set_env(self, tmp_path):
        """When a required env var IS set, it should show as OK."""
        env = os.environ.copy()
        env["E2B_API_KEY"] = "test-key-123"
        result = subprocess.run(
            ["bash", str(INSTALL_SH), str(tmp_path), "core"],
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
            cwd=str(ROOT),
        )
        # Should show the checkmark (✓) for E2B_API_KEY
        assert "E2B_API_KEY" in result.stdout
