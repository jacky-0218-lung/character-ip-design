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
- `references/ip-protection.md` — 新的第 10 份 reference：**AI 時代的角色確權**（著作權/商標/
  外觀設計專利的正確結構與時序、各法域對 AI 生成物的分歧立場、可主張著作權的工作流、創作歷程
  留存清單、商標 Tier-0 與中國子類別陷阱、侵權方向的風險、生圖平台條款與補償條款的排除項、
  EU AI Act 第 50 條與中國《標識辦法》的標示合規時程）。這是本 skill 最大的內容缺口：一條
  「用 AI 做角色 IP 並要商業化」的產線，卻沒有告訴使用者他到底擁有什麼。
- `SKILL.md` — 新增 **Step 13 確權與合規**，附明確的條件式載入指引（full pipeline / 用過
  Lane 3 生圖 / 使用者問版權商標時才讀），並在原創性防線補上「絕不在提示詞中放入品牌、IP 或
  在世藝術家姓名」這條規則的法律理由。
- `evals/scenarios/06-ai-artwork-rights.json` — 對應新路徑的行為評測情境。
- `output-spec.md` — IP bible 結構新增 ⊕「確權與合規」章節。

### Changed
- `references/rendering.md` Lane 3 模型段整段重寫為 2026-07 的實測樣貌：改為「依工作分派」
  的選型表（並點出**編輯榜才是 IP 工作的關鍵榜，前五名實質並列**）、角色一致性的新優先序
  （模型內建多參考 → Midjourney `--oref` → LoRA → IPAdapter/InstantID 降級為自架選項）、
  參考圖配額硬數字（官方覆核值見下方 Fixed）、
  一致性期望值（prompt 65–75%／LoRA 85–92%／**跨風格僅 75–85%**）與跨風格衰減警語，
  以及 negative prompt 的分流說明（閉源對話式模型沒有 negative 欄位，要改寫成正面描述）。
- `SKILL.md` Step 12 加入稀缺性管理、合規關卡與 golden record 的觸發指示；失敗模式新增
  「稀缺性當提款機」。
- `README.md` — 反映商業化章節的新內容，並說明 repo guard 現已做開放標準驗證。
- `references/rendering.md` Lane 3 — 修正一項**事實錯誤並更新到 2026-07 的模型現況**：
  Midjourney 的角色參考在 V8 線**已不可用**（`--oref` 僅 V7 且會自動改跑 V7、`--cref` 僅
  v6/niji 6），必須顯式 pin `--v 7`；網路上多數教學仍是舊行為。同時補上 Nano Banana 2 系列的
  **分槽參考圖配額**（Pro：6 object + 5 character + 3 style）、FLUX.2 多參考與 production 用
  JSON prompt、GPT Image 官方自承的角色一致性弱點、Recraft 的向量端點與方案層級陷阱，並把
  「參考圖分槽」與「identity block 重複注入」提煉成兩條跨版本原則。新增 provenance log 為
  Lane 3 的必要產出。
- `references/market-research.md` — 市場錨點更新到 2026 年最新且全部附可連結來源：
  Licensing International 2026（全球 US$3,898 億 +5.45%；角色/娛樂 US$1,618 億 +8%；北亞
  +14.1%；動漫電玩合計 34% 首度超越影視 33%）、矢野經濟 2026-07-17（日本 ¥2兆9,635億，
  **並標注「前年度比103.0%＝成長 3.0%」的日文讀數陷阱**）、POP MART FY2025 高點與 2026 年
  下行/二手崩盤，並點出崩盤主因是**供給側**（產能拉高約 10 倍）——用來支撐本 pipeline
  「靠角色深度續命」與「roadmap 寫 gate 而非產能」兩條紀律。
- `references/commercialization.md` / `references/market-research.md` §5 — 與新 reference
  交叉連結：rollout ladder 新增第 0 階「確權前置」，商標快篩明確劃清「設計前撞名檢索」與
  「公開前佈局送件」的分工。

### Fixed
- `references/rendering.md` Lane 3 的 **Midjourney 版本相容性事實錯誤**。官方文件覆核結果：
  Omni Reference「compatible with Midjourney version 7」，**V8 線（V8.2 為 2026-07 預設）
  沒有角色參考功能**——附上 `--oref` 會讓該 prompt 自動改跑 V7；`--cref` 則僅 v6/niji 6。
  `--ow` 官方範圍 1–1000、預設 100（先前引用第三方部落格的「400–600」未區分版本）。角色工作
  必須顯式 pin `--v 7`，V8.1/8.2 只用 `--sref` 做風格參考。網路上多數教學仍在描述舊行為，
  故在文中加上明確警語。
  （[Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997)、
  [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)）
- `references/rendering.md` 的 Gemini 參考圖配額改為官方覆核的精確值與模型 ID：
  `gemini-3-pro-image` 6 object + 5 character + 3 style、`gemini-3.1-flash-image`
  10 object + 4 character、`gemini-3.1-flash-lite-image` 14 object 但**無 character 槽**，
  並修正失效的文件連結
  （[Gemini API docs](https://ai.google.dev/gemini-api/docs/image-generation)）。
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
