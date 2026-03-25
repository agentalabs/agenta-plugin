"""Test that every JSON file in the repo parses correctly and has valid structure."""

import json
from pathlib import Path

import pytest

from conftest import ROOT, load_json


def _find_json_files():
    """Yield all JSON files excluding .git, .claude, and submodule dirs."""
    submodule_dirs = {"solana-foundation", "sendai", "trailofbits", "cloudflare", "superpowers"}
    for p in ROOT.rglob("*.json"):
        if ".git" in p.parts or ".claude" in p.parts:
            continue
        # Exclude files inside skill submodules
        if "skills" in p.parts:
            rel_parts = p.relative_to(ROOT / "skills").parts
            if rel_parts and rel_parts[0] in submodule_dirs:
                continue
        yield p


@pytest.mark.parametrize("json_file", list(_find_json_files()), ids=lambda p: str(p.relative_to(ROOT)))
class TestJsonValidity:
    """Every JSON file must parse without errors."""

    def test_parses(self, json_file):
        with open(json_file) as f:
            data = json.load(f)
        assert isinstance(data, dict), f"{json_file.name} root must be an object"

    def test_no_trailing_commas(self, json_file):
        """Catches a common hand-edit mistake — stdlib json rejects trailing commas,
        but let's be explicit about the check."""
        text = json_file.read_text()
        # json.loads will raise on trailing commas; just verify it doesn't.
        json.loads(text)

    def test_not_empty(self, json_file):
        data = load_json(json_file)
        assert len(data) > 0, f"{json_file.name} must not be empty"
