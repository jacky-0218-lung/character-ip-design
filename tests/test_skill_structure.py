"""Validate the Skill's structure, frontmatter, and internal reference links."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "character-ip-design"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCES = SKILL_DIR / "references"

EXPECTED_REFERENCES = {
    "market-research.md",
    "worldbuilding.md",
    "style-library.md",
    "super-symbol.md",
    "appeal.md",
    "rendering.md",
    "verification-tests.md",
    "output-spec.md",
    "commercialization.md",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    block = match.group(1)
    data: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m and not line.startswith(" "):
            key = m.group(1)
            data[key] = m.group(2).strip()
        elif key and line.startswith(" "):
            data[key] = (data.get(key, "") + " " + line.strip()).strip()
    return data


class TestSkillStructure(unittest.TestCase):
    def test_skill_md_exists(self):
        self.assertTrue(SKILL_MD.is_file(), "SKILL.md must exist")

    def test_frontmatter_name_matches_directory(self):
        fm = frontmatter(read(SKILL_MD))
        self.assertEqual(fm.get("name"), "character-ip-design")

    def test_description_is_substantial(self):
        fm = frontmatter(read(SKILL_MD))
        desc = fm.get("description", "")
        # A "pushy", trigger-rich description is intentional; enforce a floor.
        self.assertGreater(len(desc), 200, "description should be detailed for reliable triggering")
        for kw in ("mascot", "吉祥物", "IP"):
            self.assertIn(kw, desc, f"description should mention {kw!r}")

    def test_all_expected_references_present(self):
        present = {p.name for p in REFERENCES.glob("*.md")}
        self.assertEqual(present, EXPECTED_REFERENCES, "reference file set drifted")

    def test_every_referenced_file_exists(self):
        text = read(SKILL_MD)
        for name in re.findall(r"references/([A-Za-z0-9_-]+\.md)", text):
            self.assertTrue((REFERENCES / name).is_file(), f"SKILL.md points to missing references/{name}")

    def test_intake_form_present(self):
        self.assertTrue((SKILL_DIR / "assets" / "intake-form.html").is_file())

    def test_references_are_nonempty(self):
        for path in REFERENCES.glob("*.md"):
            self.assertGreater(path.stat().st_size, 400, f"{path.name} looks truncated")


if __name__ == "__main__":
    unittest.main()
