"""Validate the intake form asset: self-contained, no browser storage, all questions present."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORM = ROOT / "skills" / "character-ip-design" / "assets" / "intake-form.html"


class TestIntakeForm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = FORM.read_text(encoding="utf-8")

    def test_exists_and_is_html(self):
        self.assertTrue(FORM.is_file())
        self.assertIn("<!DOCTYPE html>", self.html)

    def test_no_browser_storage(self):
        # Artifacts must not use localStorage/sessionStorage; the form keeps state in memory.
        for banned in ("localStorage", "sessionStorage", "indexedDB"):
            self.assertNotIn(banned, self.html, f"intake form must not use {banned}")

    def test_self_contained(self):
        # No external network dependencies — inline CSS/JS only.
        for banned in ("http://", "src=\"http", "href=\"http"):
            self.assertNotIn(banned, self.html, "intake form must be fully self-contained")

    def test_all_questions_present(self):
        for marker in [
            "品牌", "受眾", "個性三關鍵詞", "應用階梯", "風格方向",
            "萌度", "既有品牌資產", "命名", "完成度",
        ]:
            self.assertIn(marker, self.html, f"intake form missing question: {marker}")

    def test_generates_brief(self):
        self.assertIn("需求摘要", self.html)
        self.assertIn("character-ip-design skill", self.html)
        self.assertIn("function build", self.html)


if __name__ == "__main__":
    unittest.main()
