# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses semantic versioning.

## [Unreleased]

### ⚠️ Breaking（僅影響手動安裝，且尚未 release）
- **skill 更名：`character-ip-design` → `designing-character-ips`**，目錄同步改名為
  `skills/designing-character-ips/`。依 Anthropic 官方
  [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
  的 name 命名建議（動名詞形，如 `processing-pdfs`／`analyzing-spreadsheets`），並保留
  「design」這個觸發字——name 與 description 是唯一預載的兩個欄位，name 多帶一個高頻觸發詞
  是白拿的。趁 0.1.2 尚未發布處理，晚一版成本只會更高。
  - **plugin／marketplace 名稱刻意維持 `character-ip-design`**，所以
    `/plugin marketplace add`、`/plugin install character-ip-design@character-ip-design`、
    `/plugin update`、`/plugin uninstall` **全部不變**；plugin 安裝者無感。
  - 受影響的只有**安裝方式 B（手動搬子目錄）**：來源路徑改為
    `skills/designing-character-ips`，安裝目的地建議一併改名。
  - 未更動：repo 名稱、`pyproject.toml` 的專案名、`skill_bundle.py` 的
    `character-ip-design-bundle-v1` 演算法識別字串（那是**格式版本識別字**，不是 skill 身分；
    改了會使 v0.1.0／v0.1.1 已發出的 receipt 無法比對）。
- `tools/check_repository.py` — 上述更名暴露了一個**原本靜默失效的守門**：plugin/skill 的
  版本漂移檢查是用 `skills/<plugin name>/SKILL.md` 定位的，一旦兩個名稱分家，該路徑找不到
  檔案就**整條檢查悄悄跳過**（測試會炸，守門卻回報 ok）。改為新的 `resolve_version_anchor()`：
  先精確比對名稱，找不到則退回 `skills/` 內唯一的 skill，**若有多個 skill 且都不匹配就報錯**
  ——沉默地停用一項檢查，正是過期版本號流到使用者手上的典型路徑。附 4 項新測試。

### Added
- `tools/run_evals.py` — **行為評測 harness**。模型呼叫本身仍需人工（repo 刻意不帶網路呼叫、
  API key 或廠商 SDK），但**其餘每一步都已工具化**，所以「跑 evals」現在是一條指令而不是一段
  散文：
  - `list` 列出情境與觸發預期；
  - `pack` 產生 `evals/runs/<model>/<情境>.md` 執行單（可直接貼的 query ＋ 打勾清單）與
    `results-<model>.json` 範本，**已填好的 results 檔不會被覆蓋**；
  - `score` 對照情境計分，三種失敗模式（漏跑／觸發結果不符／expected_behavior 未達成或未記錄）
    任一發生即以非零狀態結束。
  依官方建議預設涵蓋 **haiku／sonnet／opus** 三個模型——小模型往往需要更明確的指示，
  Opus 能從精簡指令推出的東西 Haiku 可能需要寫白。搭配 `tests/test_run_evals.py` 的 14 項測試
  與 CI 的冒煙步驟；`evals/runs/` 已列入 `.gitignore`。
- `SKILL.md` — **Pipeline checklist（執行檢核表）**：一張可直接複製到工作筆記的 13 步打勾清單，
  標出哪些步驟只在 full IP brief 跑。依 Anthropic 官方
  [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
  的「Use Workflows for Complex Tasks — 多步驟流程要給可複製的 checklist」與「Implement
  Feedback Loops」兩條建議。這條產線有 13 個步驟又有 scope ladder 分支，最常見的失敗不是做錯
  而是**漏做**（跳過三項驗證、忘記 Step 13 確權、full brief 卻沒出 roadmap）；把狀態外顯成
  checklist 是官方明列、成本最低的修法。SKILL.md 仍為 289 行，遠低於 500 行上限。
- `references/market-research.md` §2 — 競品佔位表新增**第四個佔位維度：場景**（輕場景／重場景
  兩層讀法），並要求**掃描範圍跨出品類**：2026 上半年與潮玩爭同一批貨架的已包含茶飲（蜜雪
  冰城）與遊戲 IP（王者榮耀、英雄聯盟），且中國市場**本土 IP 上榜次數約為海外 IP 的三倍**
  （YOYO 75 次、兔閃閃 ShyShy 58 次）。只掃同品類會系統性低估競爭密度。
- `references/commercialization.md` — Rollout ladder 每一階新增 `場景：___` 欄位與**輕/重場景
  對照表**，並要求與 market-research §2 的場景欄位一致。產業共識已從「誰有新 IP」移到**場景
  爭奪**：奧飛以小顆粒矩陣逐一對應場景（疊疊樂＝桌面，銷量破 8,000 萬只；粒粒＝陪伴、咔咔＝
  解壓、扣扣＝穿戴），POP MART 則投向樂園／門店／電影等重場景。獨立創作者不碰重場景，但必須
  能一句話回答「這個角色平常出現在使用者的哪裡」。

- `.claude-plugin/marketplace.json` 與 `.claude-plugin/plugin.json` — 本 repo 現在**同時是一個
  Claude Code plugin marketplace**，可用兩行指令安裝，不必手動搬檔案或知道 skills 目錄在哪：

  ```text
  /plugin marketplace add jacky-0218-lung/character-ip-design
  /plugin install character-ip-design@character-ip-design
  ```

  plugin 以 `source: "./"` 指向 repo 自身，`skills/character-ip-design/` 由 Claude Code 自動
  探索（不需宣告 `skills` 欄位）。研究時掃過三份主要 awesome 清單與同型的創意類 skill repo
  （naming、anydesign、styleseed），**沒有一個做到可直接 `/plugin marketplace add`**——
  styleseed 甚至有 `plugin.json` 卻漏了 `marketplace.json`，因此實際上裝不起來。
  參考 [plugin-marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)、
  [plugins-reference](https://code.claude.com/docs/en/plugins-reference)。
- `tools/check_repository.py` — 新增 plugin manifest 守門：marketplace 必要欄位與 kebab-case、
  **保留名稱**（`agent-skills` 等 16 個官方保留名，用了會被判為不可信來源而停止載入）、相對
  source 必須以 `./` 開頭且能解析到實際目錄、該目錄必須真的有 `SKILL.md` 或
  `skills/<name>/SKILL.md`（否則安裝後空無一物）、`keywords`/`tags` 型別（寫成字串是載入錯誤
  而非警告）、以及兩份 manifest 的 `name`/`version` 一致性。另加一條本 repo 專屬的不變量：
  **plugin 版本必須與 SKILL.md 的 `metadata.version` 同步**——版本沒 bump，既有使用者就永遠
  收不到更新。
- `tests/test_plugin_manifest.py` — 對應的 8 項單元測試。
- `install.md` / `README.md` — 新增 plugin 安裝路徑（中英雙語），並保留原本的一鍵貼上安裝法
  給非 Claude Code 的 agent。
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
- `references/rendering.md` Lane 3 — 依官方 anti-pattern「**Avoid time-sensitive
  information**」重構為官方建議的 **"Old patterns" 結構**：把不會過期的部分抽成
  **「模型選型與角色一致性：跨版本原則」9 條**（依工作分派選型且看編輯榜、參考圖是分槽的、
  identity block 每次重複注入、turnaround sheet 是第一個產出物、一致性方法優先序、跨風格衰減、
  negative prompt 分流、必記版本字串、一致性是機率不是保證），會過期的型號表／Gemini 分槽配額／
  Midjourney V7-V8 相容性／LoRA 訓練集數字／一致性百分比則收進標註
  「2026-07 快照（as of 2026-07）」的 `<details>` 區塊。**內容零損失**——agent 讀的是原始
  Markdown，`<details>` 內容一樣看得到；改變的是**過期時一眼可辨、可整塊替換**。
  另刪去因重構而重複的 Negative prompt 章節，Recraft 的型號與輸出規格同樣收進快照區塊。
- `references/commercialization.md` — 新增**高收藏品類（BJD）這條岔路**：2026 年 BJD 由小眾
  轉大眾，日本市場光素體即達千元級並形成妝面／服裝／假髮／攝影的完整生態鏈。附與盲盒的
  **五項對照表**（獲利來源／稀缺性／客單價／對設計的要求／合規風險）——兩者是相反的商業模型，
  選錯會全盤皆錯。並把判斷點前推到 Phase 2：BJD 路線要求**超級符號落在不可拆的部位**
  （頭型／臉部編碼／耳形），且在 Step 6 應優先考慮形態軸或五官軸而**避免色彩軸**，因為換色
  換裝正是該品類的賣點。
- `references/market-research.md` 潮玩週期段補上**收尾（2026 上半年）**：POP MART 王寧於
  2026-03-25 法說把今年定調為「F1 進站休整」、明講不追求「增收不增利」並下修營收增速目標；
  新品「復古理髮店」上市即破發，原定 7 月的上海 PTS 潮玩嘉年華取消；同期 TNTSPACE／黑玩／
  AYOR TOYS 等新勢力完成融資。判讀寫成一句可教的話：**這是品類的週期修正，不是品類的死亡**
  ——熱期靠供給換來的營收會在冷期原數還回去，活下來靠換賽道（場景、BJD 等高收藏品類）與換
  節奏，不是加大產能。
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
