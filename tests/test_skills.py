"""Tests for skill markdown files in skills/."""

import re

import pytest

from conftest import ROOT, ALL_SKILL_NAMES

SKILLS_DIR = ROOT / "skills"


class TestSkillCompleteness:

    @pytest.mark.parametrize("skill_name", ALL_SKILL_NAMES)
    def test_skill_exists(self, skill_name):
        path = SKILLS_DIR / f"{skill_name}.md"
        assert path.exists(), f"Missing skill: skills/{skill_name}.md"

    def test_no_extra_skills(self):
        actual = {p.stem for p in SKILLS_DIR.glob("*.md")}
        expected = set(ALL_SKILL_NAMES)
        extra = actual - expected
        assert not extra, f"Unexpected skill files: {extra}"


def _parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from a markdown file.
    Returns dict with 'description' and 'globs' keys if present."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    fm = {}
    raw = match.group(1)

    # Extract description
    desc_match = re.search(r"^description:\s*(.+?)(?:\nglobs:|\Z)", raw, re.DOTALL | re.MULTILINE)
    if desc_match:
        fm["description"] = desc_match.group(1).strip()

    # Extract globs list
    globs_match = re.search(r"^globs:\s*\n((?:\s+-\s+.+\n?)+)", raw, re.MULTILINE)
    if globs_match:
        globs_raw = globs_match.group(1)
        fm["globs"] = [
            line.strip().lstrip("- ").strip('"\'')
            for line in globs_raw.strip().split("\n")
            if line.strip().startswith("-")
        ]

    return fm


class TestSkillFrontmatter:
    """Each skill must have valid YAML frontmatter."""

    @pytest.fixture(params=ALL_SKILL_NAMES)
    def skill(self, request):
        name = request.param
        path = SKILLS_DIR / f"{name}.md"
        text = path.read_text()
        return name, text

    def test_starts_with_frontmatter_delimiter(self, skill):
        name, text = skill
        assert text.startswith("---"), (
            f"Skill {name} must start with YAML frontmatter '---'"
        )

    def test_has_closing_frontmatter_delimiter(self, skill):
        name, text = skill
        # Find second ---
        second = text.find("---", 3)
        assert second > 3, (
            f"Skill {name} missing closing frontmatter '---'"
        )

    def test_has_description(self, skill):
        name, text = skill
        fm = _parse_frontmatter(text)
        assert "description" in fm, f"Skill {name} frontmatter missing 'description'"
        assert len(fm["description"]) >= 20, (
            f"Skill {name} description too short"
        )

    def test_has_globs(self, skill):
        name, text = skill
        fm = _parse_frontmatter(text)
        assert "globs" in fm, f"Skill {name} frontmatter missing 'globs'"
        assert len(fm["globs"]) >= 1, f"Skill {name} must have at least one glob"

    def test_globs_are_valid_patterns(self, skill):
        """Globs should contain wildcard patterns, not plain filenames."""
        name, text = skill
        fm = _parse_frontmatter(text)
        for glob in fm.get("globs", []):
            assert isinstance(glob, str) and len(glob) > 0, (
                f"Skill {name}: invalid glob '{glob}'"
            )


class TestSkillContent:
    """Skills should have meaningful content beyond frontmatter."""

    @pytest.fixture(params=ALL_SKILL_NAMES)
    def skill_content(self, request):
        name = request.param
        path = SKILLS_DIR / f"{name}.md"
        text = path.read_text()
        # Get content after frontmatter
        second_delim = text.find("---", 3)
        body = text[second_delim + 3:].strip()
        return name, body

    def test_has_h1_title(self, skill_content):
        name, body = skill_content
        assert body.startswith("# "), (
            f"Skill {name} body should start with an H1 title"
        )

    def test_has_minimum_length(self, skill_content):
        name, body = skill_content
        assert len(body) >= 500, (
            f"Skill {name} body too short ({len(body)} chars). "
            "Production skills should have substantial content."
        )

    def test_has_sections(self, skill_content):
        """Should have at least 3 ## sections for meaningful structure."""
        name, body = skill_content
        sections = re.findall(r"^## ", body, re.MULTILINE)
        assert len(sections) >= 3, (
            f"Skill {name} should have at least 3 sections, found {len(sections)}"
        )
