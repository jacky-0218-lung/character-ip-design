"""Validate the canonical bundle digest tool: deterministic, tamper-evident."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import skill_bundle  # noqa: E402

SKILL_DIR = ROOT / "skills" / "designing-character-ips"


class TestBundleDigest(unittest.TestCase):
    def test_digest_is_deterministic(self):
        a, files_a = skill_bundle.canonical_bundle_digest(SKILL_DIR)
        b, files_b = skill_bundle.canonical_bundle_digest(SKILL_DIR)
        self.assertEqual(a, b)
        self.assertEqual(files_a, files_b)
        self.assertRegex(a, r"^[0-9a-f]{64}$")

    def test_digest_covers_skill_and_references(self):
        _, files = skill_bundle.canonical_bundle_digest(SKILL_DIR)
        self.assertIn("SKILL.md", files)
        self.assertIn("references/super-symbol.md", files)
        self.assertIn("assets/intake-form.html", files)

    def test_verify_accepts_matching_digest(self):
        digest, _ = skill_bundle.canonical_bundle_digest(SKILL_DIR)
        self.assertEqual(skill_bundle.verify_digest(SKILL_DIR, digest), digest)

    def test_verify_rejects_wrong_digest(self):
        with self.assertRaises(skill_bundle.BundleError):
            skill_bundle.verify_digest(SKILL_DIR, "0" * 64)

    def test_verify_rejects_malformed_digest(self):
        with self.assertRaises(skill_bundle.BundleError):
            skill_bundle.verify_digest(SKILL_DIR, "not-a-digest")

    def test_receipt_has_expected_fields(self):
        receipt = skill_bundle.build_receipt(
            SKILL_DIR,
            repository="jacky-0218-lung/character-ip-design",
            origin="https://github.com/jacky-0218-lung/character-ip-design",
            commit="0" * 40,
            destination="/home/user/.claude/skills/designing-character-ips",
        )
        for key in ("algorithm", "repository", "commit", "bundle_digest", "files"):
            self.assertIn(key, receipt)
        self.assertEqual(receipt["algorithm"], "character-ip-design-bundle-v1")


if __name__ == "__main__":
    unittest.main()
