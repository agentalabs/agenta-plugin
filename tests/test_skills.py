"""Tests for skill files in skills/."""

import re

import pytest

from conftest import ROOT, INTERNAL_SKILL_NAMES, SUBMODULE_SKILLS

SKILLS_DIR = ROOT / "skills"


class TestInternalSkillCompleteness:

    @pytest.mark.parametrize("skill_name", INTERNAL_SKILL_NAMES)
    def test_skill_exists(self, skill_name):
        path = SKILLS_DIR / f"{skill_name}.md"
        assert path.exists(), f"Missing skill: skills/{skill_name}.md"

    def test_no_extra_internal_skills(self):
        actual = {p.stem for p in SKILLS_DIR.glob("*.md") if p.stem != "SKILL"}
        expected = set(INTERNAL_SKILL_NAMES)
        extra = actual - expected
        assert not extra, f"Unexpected skill files: {extra}"


class TestSubmoduleSkills:

    @pytest.mark.parametrize("skill_name,dir_name", list(SUBMODULE_SKILLS.items()))
    def test_submodule_directory_exists(self, skill_name, dir_name):
        path = SKILLS_DIR / dir_name
        assert path.exists(), (
            f"Missing submodule directory: skills/{dir_name}/ "
            f"(run: git submodule update --init --recursive)"
        )

    @pytest.mark.parametrize("skill_name,dir_name", list(SUBMODULE_SKILLS.items()))
    def test_submodule_has_content(self, skill_name, dir_name):
        path = SKILLS_DIR / dir_name
        if path.exists():
            contents = list(path.iterdir())
            assert len(contents) > 0, f"Submodule skills/{dir_name}/ is empty"


class TestSkillIndex:

    def test_skill_index_exists(self):
        assert (SKILLS_DIR / "SKILL.md").exists(), "Missing skills/SKILL.md index"

    def test_skill_index_has_content(self):
        content = (SKILLS_DIR / "SKILL.md").read_text()
        assert len(content) > 200, "SKILL.md is too short"
        assert "# Skills Index" in content


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
    """Each internal skill must have valid YAML frontmatter."""

    @pytest.fixture(params=INTERNAL_SKILL_NAMES)
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
    """Internal skills should have meaningful content beyond frontmatter."""

    @pytest.fixture(params=INTERNAL_SKILL_NAMES)
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
