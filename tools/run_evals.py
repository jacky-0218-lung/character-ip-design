#!/usr/bin/env python3
"""Run-sheet generator and scorer for the behavioral eval scenarios.

Behavioral evals need a model to actually run; this repo's CI is offline and dependency-free,
so the harness is split in two halves that ARE deterministic and testable:

    pack   scenarios -> one graded run sheet per scenario, plus a results template
    score  a filled-in results file -> pass/fail summary, non-zero exit on regression

The model call itself stays manual (or scripted by the operator against whatever agent CLI
they have), which keeps the repo free of network calls, API keys, and vendor SDKs while still
making "run the evals" a concrete command instead of a paragraph of prose.

Anthropic's guidance is to test across Haiku / Sonnet / Opus, so ``pack`` and the results file
are both keyed by model: a scenario is only considered covered once every declared model has a
recorded run.

Standard library only; Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS_DIR = ROOT / "evals" / "scenarios"
DEFAULT_OUT = ROOT / "evals" / "runs"
# Anthropic recommends validating a skill on every model it will be used with: what an Opus
# run infers from terse instructions, a Haiku run often needs spelled out.
DEFAULT_MODELS = ("haiku", "sonnet", "opus")


class EvalError(ValueError):
    """Raised when scenarios or a results file are malformed."""


def load_scenarios(directory: Path = SCENARIOS_DIR) -> list[dict[str, Any]]:
    if not directory.is_dir():
        raise EvalError(f"scenario directory not found: {directory}")
    scenarios: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise EvalError(f"{path.name}: invalid JSON ({exc})") from exc
        for field in ("name", "query"):
            if not isinstance(data.get(field), str) or not data[field].strip():
                raise EvalError(f"{path.name}: '{field}' must be a non-empty string")
        behaviors = data.get("expected_behavior")
        if not isinstance(behaviors, list) or not behaviors:
            raise EvalError(f"{path.name}: 'expected_behavior' must be a non-empty array")
        data["_file"] = path.name
        scenarios.append(data)
    if not scenarios:
        raise EvalError(f"no scenarios found in {directory}")
    return scenarios


def run_sheet(scenario: dict[str, Any], model: str) -> str:
    """One self-contained sheet: what to paste, and what to grade it against."""
    should_trigger = scenario.get("should_trigger", True)
    trigger_line = (
        "**應觸發本 skill**" if should_trigger else "**不應觸發本 skill**（負向情境）"
    )
    lines = [
        f"# Eval run sheet — {scenario['name']} @ {model}",
        "",
        f"- 情境檔：`evals/scenarios/{scenario['_file']}`",
        f"- 模型：`{model}`",
        f"- 觸發預期：{trigger_line}",
        "",
        "## 1. 把下面這段原封不動貼給掛載了本 skill 的 agent",
        "",
        "```text",
        scenario["query"].strip(),
        "```",
        "",
        "## 2. 對照預期行為逐條打勾",
        "",
        f"- [ ] 觸發行為符合預期（{'有' if should_trigger else '沒有'}套用本 skill）",
    ]
    for behavior in scenario["expected_behavior"]:
        lines.append(f"- [ ] {behavior}")
    notes = scenario.get("notes")
    if notes:
        lines += ["", f"> 備註：{notes}"]
    lines += [
        "",
        "## 3. 把結果記進 results 檔",
        "",
        "填寫 `evals/runs/results-template.json` 的對應項目後，執行：",
        "",
        "```bash",
        "python3 tools/run_evals.py score evals/runs/results-<model>.json",
        "```",
        "",
        "未達成的項目就是下一輪 SKILL.md／references 的修訂點。",
        "",
    ]
    return "\n".join(lines)


def results_template(scenarios: list[dict[str, Any]], model: str) -> dict[str, Any]:
    return {
        "model": model,
        "runs": [
            {
                "name": s["name"],
                "triggered": bool(s.get("should_trigger", True)),
                "behaviors": {b: False for b in s["expected_behavior"]},
                "notes": "",
            }
            for s in scenarios
        ],
    }


def pack(scenarios: list[dict[str, Any]], models: list[str], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for model in models:
        model_dir = out_dir / model
        model_dir.mkdir(parents=True, exist_ok=True)
        for scenario in scenarios:
            path = model_dir / f"{scenario['name']}.md"
            path.write_text(run_sheet(scenario, model), encoding="utf-8")
            written.append(path)
        template = out_dir / f"results-{model}.json"
        if not template.exists():
            template.write_text(
                json.dumps(results_template(scenarios, model), ensure_ascii=False, indent=2)
                + "\n",
                encoding="utf-8",
            )
            written.append(template)
    return written


def score(results: dict[str, Any], scenarios: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    """Compare a filled results file against the scenarios.

    Returns (report_lines, failures). A scenario fails when it is missing from the results,
    when the trigger outcome disagrees with the scenario's expectation, or when any expected
    behavior is unmet — an unmet behavior is the actual signal the evals exist to produce.
    """
    if not isinstance(results.get("runs"), list):
        raise EvalError("results file must contain a 'runs' array")
    by_name = {r.get("name"): r for r in results["runs"] if isinstance(r, dict)}
    report: list[str] = []
    failures: list[str] = []
    model = results.get("model", "?")
    for scenario in scenarios:
        name = scenario["name"]
        expected_trigger = bool(scenario.get("should_trigger", True))
        run = by_name.get(name)
        if run is None:
            failures.append(f"{name}: no recorded run for model {model!r}")
            report.append(f"MISSING  {name}")
            continue
        problems: list[str] = []
        if bool(run.get("triggered")) != expected_trigger:
            problems.append(
                f"trigger expected {expected_trigger}, got {bool(run.get('triggered'))}"
            )
        recorded = run.get("behaviors") or {}
        if not isinstance(recorded, dict):
            raise EvalError(f"{name}: 'behaviors' must be an object of behavior -> bool")
        for behavior in scenario["expected_behavior"]:
            if behavior not in recorded:
                problems.append(f"unrecorded behavior: {behavior}")
            elif not recorded[behavior]:
                problems.append(f"unmet behavior: {behavior}")
        if problems:
            failures.extend(f"{name}: {p}" for p in problems)
            report.append(f"FAIL     {name}  ({len(problems)} problem(s))")
        else:
            report.append(f"pass     {name}")
    return report, failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    listing = sub.add_parser("list", help="List scenarios and their trigger expectation")
    listing.add_argument("--scenarios", type=Path, default=SCENARIOS_DIR)

    packer = sub.add_parser("pack", help="Emit per-model run sheets and a results template")
    packer.add_argument("--scenarios", type=Path, default=SCENARIOS_DIR)
    packer.add_argument("--out", type=Path, default=DEFAULT_OUT)
    packer.add_argument("--models", nargs="+", default=list(DEFAULT_MODELS))

    scorer = sub.add_parser("score", help="Score a filled-in results file")
    scorer.add_argument("results", type=Path)
    scorer.add_argument("--scenarios", type=Path, default=SCENARIOS_DIR)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        scenarios = load_scenarios(args.scenarios)
        if args.command == "list":
            for scenario in scenarios:
                mark = "+" if scenario.get("should_trigger", True) else "-"
                print(f"{mark} {scenario['name']:<28} {len(scenario['expected_behavior'])} behaviors")
            return 0
        if args.command == "pack":
            written = pack(scenarios, args.models, args.out)
            print(f"wrote {len(written)} files under {args.out}")
            return 0
        results = json.loads(args.results.read_text(encoding="utf-8"))
        report, failures = score(results, scenarios)
        for line in report:
            print(line)
        if failures:
            print("", file=sys.stderr)
            for failure in failures:
                print(f"error: {failure}", file=sys.stderr)
            return 1
        print(f"\nall {len(scenarios)} scenarios passed for model {results.get('model', '?')!r}")
        return 0
    except (OSError, EvalError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
