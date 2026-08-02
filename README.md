# Character IP Design（角色 IP 開發 Skill）

[![CI](https://github.com/jacky-0218-lung/character-ip-design/actions/workflows/ci.yml/badge.svg)](https://github.com/jacky-0218-lung/character-ip-design/actions/workflows/ci.yml)

[繁體中文](#繁體中文) ・ [English](#english)

---

## 繁體中文

一個把「原創角色 IP」從**市場調查**一路做到**商業化規劃**的 Agent Skill。它不是只出一張設計圖，而是一條完整產線：

**研究與策略** → **設計** → **商業化**

- **研究**：市場調查（競品 IP 佔位表，含 motif／風格／人格／**場景**四個佔位維度、空白定位）、世界觀設定、角色深度分析（價值觀／渴望／禁忌清單／反差）
- **設計**：三個概念方向讓你挑 → **同一角色三種畫風三聯圖讓你挑** → 超級符號（超級符號法）→ 剪影／延展／色彩三項驗證
- **商業化**：系列規劃與**稀缺性管理**（含盲盒 12+1 慣例、隨機機制合規關卡）、上市 roadmap（各階附啟動條件與**場景佔位**）、內容支柱、KPI、商標與文化檢核、**角色行為設定檔（golden record）**
- **13 種畫風庫**（軟糖圓潤／盲盒潮玩／像素／1930 橡膠管／蠟筆手繪／昭和復古／Y2K／水墨…）＋庫外風格上網研究協定
- **四條精緻渲染 lane**：賽璐璐立繪／3D 潮玩渲染／質感印刷／AI 生圖 prompt 套件
- **多格式輸出**：SVG 母檔 → LINE 貼圖 PNG、圓形 icon、印刷版、像素原生放大、輕量 GIF
- **確權與合規**：AI 生成角色的著作權／商標／外觀設計專利該用什麼順序處理、創作歷程要留什麼、
  商標 Tier-0 類別與中國子類別陷阱、EU AI Act 與中國《標識辦法》的 AI 標示義務（非法律意見）

### 安裝方式 A：Claude Code plugin（最快，兩行指令）

本 repo 同時是一個 Claude Code plugin marketplace，在 Claude Code 或 Cowork 裡直接輸入：

```text
/plugin marketplace add jacky-0218-lung/character-ip-design
/plugin install character-ip-design@character-ip-design
```

之後用 `/plugin update character-ip-design` 更新。這條路徑不需要手動搬檔案，也不必知道你的
skills 目錄在哪。

### 安裝方式 B：一鍵安裝（把下面這段話貼給你的 AI Agent）

適合非 Claude Code 的 agent（Codex、Cursor…），或想自己控制安裝位置的人。

> 請從 `https://github.com/jacky-0218-lung/character-ip-design/tree/main/skills/character-ip-design` 安裝 `character-ip-design` 這個 skill。優先用公開 repository 的直接下載；只有在直接下載因權限問題失敗時才退回 git clone。只安裝 `skills/character-ip-design` 這個子目錄到我 Agent 信任的 skills 目錄。若目的地已存在，請停止並回報，不要覆蓋。安裝完成後回報安裝路徑，並告訴我何時可以開始使用。

安裝後，skill 的名稱與描述會常駐在 Agent 的可用技能清單。你不需要記任何指令——當你說「幫我設計一個吉祥物」「我想做一個原創 IP」時，Agent 會自動選用它。

需要可重現的安裝，可把 `main` 換成某個 release tag 或完整 40 字元 commit SHA；本 repo 的 `install.md` 也提供 digest 驗證流程。

### 安裝後怎麼用（初始化界面）

1. 你說「幫我做一個角色／IP」→ skill 啟動。
2. **初始化表單**：Agent 用一張選擇題表單一次問齊 9 題（品牌、受眾、個性、應用階梯、風格、萌度、既有資產、命名、完成度）。也可以打開 [`skills/character-ip-design/assets/intake-form.html`](skills/character-ip-design/assets/intake-form.html) 自己填，按「產生需求摘要」把摘要貼回對話。
3. 之後 skill 照流程走：（完整 IP）市場調查報告 → 世界觀＋角色設定 → 三概念 → 三風格 → 設計＋驗證 → 商業化 roadmap；（快速吉祥物）自動壓縮成幾分鐘一份設計書。
4. 最後交付：一份整合的 **IP bible（自帶所有圖的 HTML）** ＋ SVG 母檔 ＋ 各平台輸出。

### 開發

執行階段的 skill 只有 Markdown 與一份自足的 HTML 表單，沒有任何執行階段相依。倉庫工具只用 Python 標準函式庫（3.10+）：

```bash
python3 -m unittest discover -s tests -v
python3 tools/check_repository.py
python3 tools/skill_bundle.py digest skills/character-ip-design
```

`check_repository.py` 除了倉庫守則，也會依 [Agent Skills 開放標準](https://agentskills.io/specification)
驗證每個 skill 的 frontmatter（name 規則與目錄同名、description ≤ 1024 字元、欄位白名單、
SKILL.md ≤ 500 行、references 連結可解析），確保這個 skill 在 Claude 之外的 agent 也能安裝。

### 授權

Apache License 2.0，見 [LICENSE](LICENSE)。角色設計方法論以知名 IP 為分析素材；本 skill 只產出原創角色，並內建原創性防線，不複製任何既有 IP 的符號組合。

---

## English

An Agent Skill that develops an original character IP end-to-end — from **market research**
to a **commercialization plan**, not just a drawing. Three phases: **research & strategy → design → commercialization.**

- **Research**: market study (competitor-IP occupancy table, white-space positioning), worldview, and a character depth profile (values / desire / taboo list / the one "gap").
- **Design**: 3 concept directions to choose from → **a 3-style triptych of the chosen character to pick from** → the Super Symbol method → silhouette / extension / color verification.
- **Commercialization**: series plan and **scarcity management** (incl. the blind-box 12+1 convention and random-mechanic compliance gates), staged rollout roadmap with gate conditions, content pillars, KPIs, trademark & cultural screens, and a machine-readable **character golden record**.
- **13-style library** (soft-kawaii, blind-box, pixel, 1930s rubber-hose, crayon, Shōwa retro, Y2K, ink-wash…) plus a research protocol for any style the user names.
- **Four premium rendering lanes**: cel-shade key visual, faux-3D toy render, print textures, and an AI-generation prompt package.
- **Multi-format export**: SVG masters → LINE sticker PNGs, circle-safe icons, print plates, pixel nearest-neighbor, light GIF.
- **Rights & compliance**: the right ordering for copyright / trademark / design-patent filings on an AI-assisted character, what provenance to log, Tier-0 trademark classes and China's sub-class trap, and AI-disclosure duties (EU AI Act Art. 50, China's labeling rules). Not legal advice.

### Install A: as a Claude Code plugin (two commands)

This repo doubles as a Claude Code plugin marketplace:

```text
/plugin marketplace add jacky-0218-lung/character-ip-design
/plugin install character-ip-design@character-ip-design
```

Update later with `/plugin update character-ip-design`. No manual file copying, and you don't
need to know where your skills directory lives.

### Install B: one-prompt install (paste this to your agent)

For non-Claude-Code agents (Codex, Cursor…) or when you want to control the install location.

> Install the `character-ip-design` skill from `https://github.com/jacky-0218-lung/character-ip-design/tree/main/skills/character-ip-design`. Prefer direct download for this public repository and fall back to git clone only on permission errors. Install only the `skills/character-ip-design` subtree into my agent's trusted skills directory. If the destination already exists, stop and report it instead of overwriting. Report the installed path when done.

After install, the skill's name and description sit in the agent's available-skills list; it auto-triggers when you ask to design a mascot / character / IP. For a reproducible install, replace `main` with a release tag or full commit SHA; `install.md` documents a digest-verified flow.

### After install — the intake interface

You ask to make a character → the skill presents a **one-round intake form** (9 questions), or you fill [`skills/character-ip-design/assets/intake-form.html`](skills/character-ip-design/assets/intake-form.html) and paste the generated brief back. Then the pipeline runs and delivers one self-contained **IP bible (HTML with every asset inlined)** plus SVG masters and per-surface exports.

### Development

```bash
python3 -m unittest discover -s tests -v
python3 tools/check_repository.py
python3 tools/skill_bundle.py digest skills/character-ip-design
```

### License

Apache License 2.0 — see [LICENSE](LICENSE). The skill produces only original characters and
includes an originality guardrail; famous IPs are analysis material, never copied.
