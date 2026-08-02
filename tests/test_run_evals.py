"""Tests for the eval run-sheet harness (tools/run_evals.py).

The harness deliberately does not call a model, so everything it does IS testable offline:
sheet generation, the results template, and the scorer's three failure modes.
Standard library only.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from run_evals import (  # noqa: E402
    EvalError,
    load_scenarios,
    pack,
    results_template,
    run_sheet,
    score,
)


SAMPLE = [
    {
        "_file": "01-sample.json",
        "name": "sample-positive",
        "query": "幫我設計一個吉祥物",
        "should_trigger": True,
        "expected_behavior": ["先呈現初始化表單", "出示三項驗證"],
    },
    {
        "_file": "02-negative.json",
        "name": "sample-negative",
        "query": "幫我修一段 Python",
        "should_trigger": False,
        "expected_behavior": ["不套用本 skill"],
    },
]


def filled(overrides=None):
    data = {
        "model": "sonnet",
        "runs": [
            {
                "name": "sample-positive",
                "triggered": True,
                "behaviors": {"先呈現初始化表單": True, "出示三項驗證": True},
            },
            {
                "name": "sample-negative",
                "triggered": False,
                "behaviors": {"不套用本 skill": True},
            },
        ],
    }
    if overrides:
        overrides(data)
    return data


class TestLoadScenarios(unittest.TestCase):
    def test_loads_the_repository_scenarios(self):
        scenarios = load_scenarios()
        self.assertGreaterEqual(len(scenarios), 4)
        for scenario in scenarios:
            self.assertTrue(scenario["name"].strip())
            self.assertTrue(scenario["query"].strip())
            self.assertTrue(scenario["expected_behavior"])

    def test_rejects_malformed_scenario(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps({"name": "x", "query": ""}), encoding="utf-8")
            with self.assertRaises(EvalError):
                load_scenarios(Path(tmp))

    def test_rejects_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(EvalError):
                load_scenarios(Path(tmp))


class TestRunSheet(unittest.TestCase):
    def test_sheet_contains_query_model_and_every_behavior(self):
        sheet = run_sheet(SAMPLE[0], "haiku")
        self.assertIn("幫我設計一個吉祥物", sheet)
        self.assertIn("haiku", sheet)
        for behavior in SAMPLE[0]["expected_behavior"]:
            self.assertIn(behavior, sheet)

    def test_negative_scenario_states_it_must_not_trigger(self):
        self.assertIn("不應觸發", run_sheet(SAMPLE[1], "opus"))


class TestPack(unittest.TestCase):
    def test_writes_one_sheet_per_scenario_per_model_plus_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            pack(SAMPLE, ["haiku", "opus"], out)
            for model in ("haiku", "opus"):
                for scenario in SAMPLE:
                    self.assertTrue((out / model / f"{scenario['name']}.md").is_file())
                template = out / f"results-{model}.json"
                self.assertTrue(template.is_file())
                data = json.loads(template.read_text(encoding="utf-8"))
                self.assertEqual(data["model"], model)
                self.assertEqual(len(data["runs"]), len(SAMPLE))

    def test_pack_does_not_clobber_a_filled_results_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            template = out / "results-sonnet.json"
            out.mkdir(parents=True, exist_ok=True)
            template.write_text('{"model": "sonnet", "runs": ["mine"]}', encoding="utf-8")
            pack(SAMPLE, ["sonnet"], out)
            self.assertIn("mine", template.read_text(encoding="utf-8"))

    def test_template_starts_all_behaviors_unmet(self):
        template = results_template(SAMPLE, "sonnet")
        for run in template["runs"]:
            self.assertTrue(all(v is False for v in run["behaviors"].values()))


class TestScore(unittest.TestCase):
    def test_fully_met_results_pass(self):
        report, failures = score(filled(), SAMPLE)
        self.assertEqual(failures, [])
        self.assertTrue(all(line.startswith("pass") for line in report))

    def test_missing_scenario_fails(self):
        data = filled(lambda d: d["runs"].pop(0))
        _, failures = score(data, SAMPLE)
        self.assertTrue(any("no recorded run" in f for f in failures))

    def test_unmet_behavior_fails(self):
        def break_one(d):
            d["runs"][0]["behaviors"]["出示三項驗證"] = False
        _, failures = score(filled(break_one), SAMPLE)
        self.assertTrue(any("unmet behavior" in f for f in failures))

    def test_wrong_trigger_outcome_fails(self):
        def break_trigger(d):
            d["runs"][1]["triggered"] = True
        _, failures = score(filled(break_trigger), SAMPLE)
        self.assertTrue(any("trigger expected" in f for f in failures))

    def test_unrecorded_behavior_fails(self):
        def drop_behavior(d):
            d["runs"][0]["behaviors"].pop("出示三項驗證")
        _, failures = score(filled(drop_behavior), SAMPLE)
        self.assertTrue(any("unrecorded behavior" in f for f in failures))

    def test_malformed_results_raise(self):
        with self.assertRaises(EvalError):
            score({"runs": "nope"}, SAMPLE)


if __name__ == "__main__":
    unittest.main()
