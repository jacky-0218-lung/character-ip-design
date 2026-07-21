# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses semantic versioning.

## [Unreleased]

### Changed
- `references/rendering.md` — refreshed Lane 3 (AI 生圖 prompt package) to the 2026 model
  landscape: added Google「Nano Banana」/ Nano Banana Pro (current identity-preservation /
  character-consistency leader), GPT Image (prompt adherence + in-image text), and FLUX.2 /
  FLUX Kontext (context-aware editing), alongside the existing Midjourney and LoRA routes.
  Framed the per-tool block as principle-first and version-swappable ("current as of 2026-07")
  per Anthropic's skill-authoring guidance to avoid pinning time-sensitive detail, and updated
  the on-model drift note to reflect that identity-preservation models narrow but don't close
  the fine-symbol-detail gap.

### Added
- Added a 目錄（Contents）table of contents to the five reference files over 100 lines
  (`rendering.md`, `style-library.md`, `output-spec.md`, `appeal.md`, `super-symbol.md`),
  following Anthropic's skill best practice of giving longer reference files a table of
  contents for faster navigation and progressive disclosure.

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
