"""Validate the Claude Code plugin marketplace manifests.

These two files are what let a user run

    /plugin marketplace add jacky-0218-lung/character-ip-design
    /plugin install character-ip-design@character-ip-design

Schema per https://code.claude.com/docs/en/plugin-marketplaces and
https://code.claude.com/docs/en/plugins-reference. Standard library only.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / ".claude-plugin"
MARKETPLACE = PLUGIN_DIR / "marketplace.json"
MANIFEST = PLUGIN_DIR / "plugin.json"
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TestMarketplace(unittest.TestCase):
    def test_files_exist_in_claude_plugin_dir(self):
        # The directory name is load-bearing: Claude Code looks for exactly `.claude-plugin/`.
        self.assertTrue(MARKETPLACE.is_file(), ".claude-plugin/marketplace.json must exist")
        self.assertTrue(MANIFEST.is_file(), ".claude-plugin/plugin.json must exist")

    def test_marketplace_required_fields(self):
        data = load(MARKETPLACE)
        self.assertTrue(KEBAB.fullmatch(data["name"]), "marketplace name must be kebab-case")
        self.assertIsInstance(data["owner"], dict)
        self.assertTrue(data["owner"].get("name"), "owner.name is required")
        self.assertIsInstance(data["plugins"], list)
        self.assertGreaterEqual(len(data["plugins"]), 1)

    def test_plugin_entry_is_installable(self):
        entry = load(MARKETPLACE)["plugins"][0]
        self.assertTrue(KEBAB.fullmatch(entry["name"]))
        # A relative source must start with './' and resolve from the repo root — NOT from
        # inside .claude-plugin/. Getting this wrong installs nothing with no clear error.
        self.assertTrue(entry["source"].startswith("./"))
        target = (ROOT / entry["source"]).resolve()
        self.assertTrue(target.is_dir())
        # Self-sourced plugin: skills/ is auto-discovered, so the skill must live there.
        self.assertTrue(
            any((target / "skills").glob("*/SKILL.md")),
            "plugin source exposes no skills/<name>/SKILL.md, so nothing would install",
        )

    def test_list_typed_fields_are_lists(self):
        # A keywords value that is a string instead of an array is a hard load error.
        entry = load(MARKETPLACE)["plugins"][0]
        for field in ("keywords", "tags"):
            if field in entry:
                self.assertIsInstance(entry[field], list)
        manifest = load(MANIFEST)
        if "keywords" in manifest:
            self.assertIsInstance(manifest["keywords"], list)

    def test_manifest_and_entry_agree(self):
        entry = load(MARKETPLACE)["plugins"][0]
        manifest = load(MANIFEST)
        self.assertEqual(entry["name"], manifest["name"])
        self.assertEqual(entry.get("version"), manifest.get("version"))
        self.assertEqual(entry.get("license"), manifest.get("license"))

    def test_version_matches_skill_metadata(self):
        """A published version that never moves means users never get updates."""
        manifest = load(MANIFEST)
        skill_md = ROOT / "skills" / manifest["name"] / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        found = re.search(r"^\s+version:\s*[\"']?([^\s\"']+)", text, re.M)
        self.assertIsNotNone(found, "SKILL.md frontmatter should declare metadata.version")
        self.assertEqual(found.group(1), manifest["version"])

    def test_marketplace_name_not_reserved(self):
        reserved = {
            "claude-code-marketplace", "claude-code-plugins", "claude-plugins-official",
            "claude-plugins-community", "claude-community", "anthropic-marketplace",
            "anthropic-plugins", "agent-skills", "anthropic-agent-skills",
            "knowledge-work-plugins", "life-sciences", "claude-for-legal",
            "claude-for-financial-services", "financial-services-plugins",
            "first-party-plugins", "healthcare",
        }
        self.assertNotIn(load(MARKETPLACE)["name"], reserved)


if __name__ == "__main__":
    unittest.main()
