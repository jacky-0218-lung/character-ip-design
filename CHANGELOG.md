# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses semantic versioning.

## [Unreleased]

### Added
- `references/commercialization.md` — 三個新章節：**系列規劃與稀缺性管理**（以 2025–26 的
  Labubu 週期為實證：二級市場溢價崩塌領先於營收下滑、熱期擴產是價值破壞、單一系列營收佔比
  1/3 警戒線）、**隨機機制合規關卡**（年齡門檻、機率與隱藏款揭露、單價上限方向）、以及
  **角色行為設定檔（golden record）** —— 對應 2026 年新出現的 Behavioral Licensing 品類，
  由 Phase 1 Step 3 的角色深度設定直接推導，同時可當授權附件與 AI 生圖的 canonical
  description 來源。另補上 2026 市場錨點（授權零售 US$389.8B／角色類 +8%／遊戲・漫畫・社群
  原生 34% 已超過影視 33%／kidult 佔比）、潮玩定價階梯、組合策略（shots on goal），以及
  細特徵量產預警與二級溢價 KPI。
- `references/rendering.md` Lane 3 — 新增「系列 prompt 架構：fixed / variable 雙區塊」
  （12+1 盲盒與節慶版一致性的核心做法）與「外部向量生成（Recraft 路線）」一節，含
  SVG-friendly 約束詞庫、已知失敗模式與人工清理緩衝；並確立 turnaround sheet 為 Lane 3 的
  第一個產出物（四格拼版、正交、白底、≥2048 px／視角）。
- `tools/check_repository.py` — 依 [Agent Skills 開放標準](https://agentskills.io/specification)
  驗證每個 skill：name 規則與目錄同名、description 1–1024 字元、frontmatter 欄位白名單、
  compatibility ≤ 500 字元、SKILL.md ≤ 500 行、references 連結可解析，另加一則 Claude skill
  listing 1,536 字元截斷警告。搭配 `tests/test_skill_structure.py` 的四個新測試。
- `SKILL.md` frontmatter — 補上標準允許的 `license` 與 `metadata`（author / version）欄位。

### Changed
- `references/rendering.md` Lane 3 模型段整段重寫為 2026-07 的實測樣貌：改為「依工作分派」
  的選型表（並點出**編輯榜才是 IP 工作的關鍵榜，前五名實質並列**）、角色一致性的新優先序
  （模型內建多參考 → Midjourney `--oref/--ow 400–600` → LoRA → IPAdapter/InstantID 降級為
  自架選項）、參考圖配額硬數字（NB Pro 約 5 角色＋6 物件、NB2 約 4 角色＋10 物件）、
  一致性期望值（prompt 65–75%／LoRA 85–92%／**跨風格僅 75–85%**）與跨風格衰減警語，
  以及 negative prompt 的分流說明（閉源對話式模型沒有 negative 欄位，要改寫成正面描述）。
- `SKILL.md` Step 12 加入稀缺性管理、合規關卡與 golden record 的觸發指示；失敗模式新增
  「稀缺性當提款機」。
- `README.md` — 反映商業化章節的新內容，並說明 repo guard 現已做開放標準驗證。

### Fixed
- `references/commercialization.md` 的簡體字「东西」修正為「東西」。

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
