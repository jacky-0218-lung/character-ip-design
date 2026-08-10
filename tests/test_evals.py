"""Validate the behavioral eval scenarios are well-formed.

These do NOT call a model — running the evals for real needs an agent harness
(see evals/README.md). This test only guards the scenario schema so a malformed
or truncated scenario file fails CI early. Standard library only.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "evals" / "scenarios"
SKILL_NAME = "designing-character-ips"


def load_scenarios() -> list[tuple[Path, dict]]:
    return [(p, json.loads(p.read_text(encoding="utf-8"))) for p in sorted(SCENARIOS.glob("*.json"))]


class TestEvalScenarios(unittest.TestCase):
    def test_scenarios_directory_exists(self):
        self.assertTrue(SCENARIOS.is_dir(), "evals/scenarios must exist")

    def test_has_enough_scenarios(self):
        # Anthropic best practice: at least a few real scenarios.
        self.assertGreaterEqual(len(list(SCENARIOS.glob("*.json"))), 4)

    def test_each_scenario_is_well_formed(self):
        for path, data in load_scenarios():
            with self.subTest(scenario=path.name):
                self.assertIsInstance(data.get("name"), str)
                self.assertTrue(data["name"].strip(), "name must be non-empty")

                self.assertIsInstance(data.get("query"), str)
                self.assertTrue(data["query"].strip(), "query must be non-empty")

                behaviors = data.get("expected_behavior")
                self.assertIsInstance(behaviors, list)
                self.assertGreaterEqual(len(behaviors), 1, "need at least one expected behavior")
                for b in behaviors:
                    self.assertIsInstance(b, str)
                    self.assertTrue(b.strip(), "expected_behavior items must be non-empty")

                should_trigger = data.get("should_trigger", True)
                self.assertIsInstance(should_trigger, bool)
                skills = data.get("skills", [])
                self.assertIsInstance(skills, list)
                if should_trigger:
                    self.assertIn(SKILL_NAME, skills, "triggering scenario must list the skill")
                else:
                    self.assertEqual(skills, [], "non-triggering scenario must have empty skills")

    def test_has_at_least_one_negative(self):
        negatives = [d for _, d in load_scenarios() if not d.get("should_trigger", True)]
        self.assertGreaterEqual(len(negatives), 1, "include at least one no-trigger scenario")

    def test_names_are_unique(self):
        names = [d["name"] for _, d in load_scenarios()]
        self.assertEqual(len(names), len(set(names)), "scenario names must be unique")


if __name__ == "__main__":
    unittest.main()
