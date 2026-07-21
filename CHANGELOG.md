# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses semantic versioning.

## [Unreleased]

## [0.1.1] - 2026-07-21

### Added
- `.github/workflows/auto-open-weekly-pr.yml` — a guard-compliant workflow that auto-opens a
  PR when a `weekly-improve-*` branch is pushed. It runs on GitHub's infrastructure (using the
  built-in `GITHUB_TOKEN`), so the weekly maintenance task can open PRs even when its cloud
  sandbox cannot reach the GitHub API directly. Top-level permissions stay read-only; the job
  grants only `pull-requests: write`; no third-party actions are used; and it prints a clear
  hint if the repo's "Allow Actions to create PRs" setting is disabled.
- 目錄（Contents）table of contents on the five reference files over 100 lines
  (`rendering.md`, `style-library.md`, `output-spec.md`, `appeal.md`, `super-symbol.md`),
  per Anthropic's skill best practice for longer files.
- `evals/` — a lightweight behavioral evaluation set (5 scenario specs + `evals/README.md`,
  including a negative no-trigger case) plus `tests/test_evals.py` to validate scenario schema,
  following evaluation-driven skill authoring.
- Two new entries in `references/style-library.md`: **12 Y2K 千禧未來感** and **13 水墨 東方水墨風**
  — the two styles the library's own research protocol previously named as uncovered.

### Changed
- `references/rendering.md` — refreshed Lane 3 (AI 生圖 prompt package) to the 2026 model
  landscape (Google「Nano Banana」/ Nano Banana Pro, GPT Image, FLUX.2 / FLUX Kontext,
  alongside Midjourney and the LoRA route), written principle-first and version-swappable
  ("current as of 2026-07") per Anthropic's guidance to avoid pinning time-sensitive detail;
  updated the on-model drift note.
- `references/market-research.md` — added 2024–2025 潮玩／blind-box category anchors (POP MART
  scale, plush +1,289%, design-fatigue & minor-protection signals) with live sources, keeping
  the verify-by-search discipline.
- `README.md` — style-library count updated 11 → 13; the reproducible-install-by-tag
  instruction is now backed by a real `v0.1.1` release tag.

## [0.1.0] - 2026-07-21

### Added
- Initial release of the `character-ip-design` Agent Skill.
- Three-phase pipeline: research & strategy → design → commercialization.
- References: market-research, worldbuilding, style-library (11 styles + research protocol),
  super-symbol, appeal, rendering (4 premium lanes), verification-tests, output-spec,
  commercialization.
- `assets/intake-form.html`: self-contained intake interface that emits a paste-back brief.
- Repository tooling: `tools/skill_bundle.py` (canonical bundle digest + receipt),
  `tools/check_repository.py` (repo guard), unit tests, and a read-only CI workflow.
