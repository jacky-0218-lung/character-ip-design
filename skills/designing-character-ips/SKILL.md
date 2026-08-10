---
name: designing-character-ips
description: >-
  Full character-IP development pipeline — market research first, then worldbuilding and a
  character depth profile, then design (Super Symbol 超級符號 method: 3 concept directions, a
  3-style triptych for the user to pick from, single-feature amplification, budgeted appeal,
  silhouette/extension verification), then commercialization (series planning, rollout
  roadmap, KPIs, trademark/cultural screen, premium finishes and AI prompt packages). Use this
  skill whenever the user wants to create, design, redesign, or evaluate a character IP,
  mascot, 吉祥物, 品牌角色, IP 角色/形象, LINE 貼圖角色, app/game/VTuber character, plush or
  blind-box character, or wants 市場調查/世界觀/角色設定 for an original IP — even if they
  only say「幫我設計一個角色/吉祥物」or "design a mascot", whatever art style they name, and
  even if they never use the word "IP". Also for diagnosing why an existing character isn't
  memorable, or simplifying an over-decorated one.
license: Apache-2.0
metadata:
  author: jacky-0218-lung
  version: "0.1.2"
---

# Character IP Design（角色 IP 開發・超級符號法）

## Why this pipeline exists

An IP is a business object that happens to have a face. Professional IP is goal-first, not
art-first: Kumamon was a tourism strategy before it was a bear; POP MART signs artists before
products exist; San-X kills ~198 of its ~200 yearly concepts at the MEANING stage. Drawing
first and thinking later produces wallpaper with eyes — pretty, positioned nowhere, extendable
into nothing.

So the pipeline runs in three phases: **研究與策略** (market, positioning, worldview,
character interior) → **設計** (the Super Symbol method: one amplified feature, visual
subtraction, budgeted charm, style consciously chosen, everything verified) → **商業化**
(series planning, staged rollout, KPIs, licensing readiness). The design phase manages three
budgets: identity (ONE symbol), charm (small, never zero), style (choose once, commit at 80%).

## First run: the intake form（初始化界面）

The very first thing this skill does on a new brief is collect a structured brief. If the user
has not already pasted a filled brief, present the intake:

- **Interactive environments (Cowork/desktop)**: ask the intake questions below as ONE batched
  multiple-choice form via the question tool (e.g., AskUserQuestion). You may also offer
  `assets/intake-form.html` — a self-contained page the user fills and whose "Copy brief"
  output they paste back — for users who prefer a form UI. Either way it is ONE round.
- **Plain chat / headless**: ask the questions as one compact numbered list, or (unattended)
  answer them yourself with reasonable assumptions and put the assumption list at the top of
  the deliverable.

Parse the returned brief into the Phase 1 Step 1 fields and proceed. Never start designing
before the brief exists — an unbriefed character is a generic character.

## Scope ladder — not every brief is a bible

- **Full IP brief**: the user wants an IP to operate (stickers→merch→licensing), says 市場調查
  /世界觀/IP 經營, or is building from zero for commercial growth → run all three phases.
- **Quick mascot brief**: a shop/team wants a mascot for defined surfaces → compress Phase 1
  (competitor scan + name/motif collision check folded into 定位摘要, no separate report) and
  Phase 3 (usage don'ts + light extension notes), full Phase 2 always.
- When unsure, ask in intake. Never inflict a 40-page bible on a coffee shop; never ship a
  naked drawing to someone building a business.

## Pipeline checklist（開工前先複製這張表，每完成一步就打勾）

Copy this checklist into your working notes and tick items as you go. ⊕ 步驟只在 full IP
brief 跑；quick-mascot brief 依上方 scope ladder 壓縮或略過。

```text
Phase 1 研究與策略
- [ ] S1  Intake — brief 已取得（表單或一輪批次提問），scope ladder 已判定
- [ ] S2  市場調查 — 競品佔位表 + 空白定位一句話（⊕ 完整報告；快速吉祥物併入定位摘要）
- [ ] S3  敘事教義 + 世界觀 1 頁 + 角色深度設定（含唯一的反差來源）
Phase 2 設計
- [ ] S4  三個概念方向（不同 motif 且不同身體構成）→ 已選定
- [ ] S5  風格三聯圖（三種不同語域）→ 風格已鎖定，之後不再換
- [ ] S6  放大軸擇一（五官／形態／色彩）
- [ ] S7  視覺減法（never-delete floor 已確認）
- [ ] S8  超級符號一句話＋幾何 + 唯一一個反差
- [ ] S9  Hero 繪製 + 魅力檢核（色彩 4 角色／一處不對稱／細節 ≤ 4 項）
- [ ] S10 三項驗證，每項附圖與判定（失敗 → 修訂 → 附 before/after）
Phase 3 商業化與交付
- [ ] S11 延展組（表情／姿勢／情境圖）+ 各平台輸出 +（若 intake 要求）精緻渲染 lane
- [ ] S12 ⊕ 系列規劃／rollout roadmap（各階 gate）／內容支柱／KPI／商品化檢核／golden record
- [ ] S13 確權與合規（⊕，或任何用過 AI 生圖的案子一律必做）
- [ ] 交付 IP bible（HTML）+ SVG 母檔；marginal 的驗證結果在對話訊息裡主動講
```

S9 在完整 brief 上永遠不能早於 S1–S3——「畫得比想得快」是這條產線最常見的失敗。

---

## PHASE 1 — 研究與策略（think before drawing）

### Step 1 — Intake（先問，再做）

Gather in ONE batched round (5–9 focused questions; see "First run: the intake form" above):

1. 品牌/產品一句話，以及**這是單一吉祥物委託，還是要經營的 IP**（決定 scope ladder）
2. 受眾 — who must love this character
3. 個性三關鍵詞（offer examples to pick from）
4. 商業目標與應用階梯 — 首要 surface（貼圖/icon/週邊/立牌/官網）+ 長期想走到哪（週邊？授權？）
5. 風格方向 — offer 2–3 fitting entries from `references/style-library.md`, plus「有想要的
   參照風格嗎？我會去研究」and dislikes
6. 萌度 vs 成熟度（幼齡可愛 ↔ 冷面成熟 deadpan）
7. 既有品牌資產 — item by item: colors? logo shapes? name? existing audience?
8. 命名 — exists, or propose candidates?
9. 完成度 — flat identity only, or premium key visual (賽璐璐/3D 潮玩/質感印刷) or AI prompt
   package? (`references/rendering.md`)

Don't re-interrogate a detailed brief — confirm the 1–2 open items.

### Step 2 — Market research（市場調查）

Full protocol in `references/market-research.md`. Produce the 市場分析報告: category sizing
with sourced (hyperlinked) numbers, the competitor-IP occupancy table (motif × style × persona
register × surfaces), audience insight, the **positioning white-space statement**,
name/trademark quick screen (with the 非法律意見 disclaimer), cultural screen for multi-market
IPs. The white-space statement is the brief for everything downstream — Phase 2's directions
must be answers to it. Quick-mascot briefs: compress per the reference's scaling rules. No web
access: state it, mark claims unverified.

### Step 3 — Strategy, worldview, character interior（定位、世界觀、角色深度）

Read `references/worldbuilding.md`. Decide and record:

- **Positioning statement** — one sentence built on the white space.
- **Narrative doctrine** — Sanrio 極簡投射型 vs San-X 微敘事型, chosen explicitly with why.
- **世界觀 bible**（1 page max): 一句話設定, 3–5 world rules, 基調, 配角掛鉤, kept mystery
  (if 微敘事型).
- **角色深度設定**: 價值觀/渴望/害怕/習慣/關係/說話方式/行為規則/禁忌清單/反差(the gap)/
  口頭禪. Every later artifact must be derivable from this sheet — stickers are 習慣 drawn,
  the scene is 渴望 staged.

---

## PHASE 2 — 設計（the Super Symbol method）

### Step 4 — Direction fan-out（三個概念方向）

Never refine the first idea. Propose **3 distinct concept directions** aimed at the
white-space statement — different motif AND different body construction (palette swaps don't
count). Each: one-sentence pitch (motif × brand; yuru-chara's "creature × local context"
formula generates well), 3 vibe keywords, amplification axis it would use, register reference
("Sumikko-like underdog energy" — register, never appearance), right for / wrong for, and a
rough silhouette-first SVG thumbnail. User picks via the form; unattended → pick with a
2-sentence justification, keep the others in the appendix.

### Step 5 — Style triptych（同一概念，三種風格，給使用者挑）

Take the chosen concept and render it in **three different styles** side by side — thumbnail
quality, one shared pose, styles drawn from `references/style-library.md` (or researched via
its style research protocol when the user named something outside it; write the 風格規格 with
sources before drawing). Choose the three to span genuinely different registers that all fit
the positioning (e.g., 軟糖圓潤 vs 盲盒 deadpan vs 昭和レトロ — not three flavors of kawaii).
For each: 2-line tradeoff (right for / wrong for, given THEIR application ladder). User picks
via the form; unattended → recommend one with reasons, keep all three renders in the bible so
the choice stays visible. Then lock the style — commit at 80%, no style tourism after this
point.

### Step 6 — Choose exactly ONE amplification axis

| Axis | 中文 | Amplify | Examples |
|------|------|---------|----------|
| Facial feature | 五官 | one feature — or its *absence* | Labubu's nine teeth; Kitty's missing mouth |
| Form | 形態 | one part's proportion, or whole-body geometry | Cinnamoroll's ears; Totoro's egg |
| Color | 色彩 | one signature hue owning the character | Duolingo green; Kumamon's black |

Pick by the top-ranked application (貼圖→五官; 實體/立牌→形態; icon-first/brand color→色彩).
Details, techniques (scale/absence/repetition/purity), and conflict rules:
`references/super-symbol.md`. The symbol must survive the locked style (pixel: native grid;
crayon: lives in the silhouette).

### Step 7 — Visual subtraction（減法管身分，不砍生命感）

Delete identity-competing elements (costumes, hats, wings, welded props). **Never-delete
floor**: catchlight eyes (or recorded deadpan choice), a mouth, one warmth cue. Style-grammar
wear (rubber-hose gloves, sticker borders) is style, not props. Real props are relocated to
scenes, never destroyed. Target: describable over the phone in ≤ 2 sentences.

### Step 8 — Super symbol + the one gap

One sentence plus geometry ("ears are two wing-like arcs ≈ 1.2× head width"). Not
one-sentence-able → not yet a symbol. Then exactly **one gap（反差）** — pulled from the
character interior (Step 3), visual or persona-side. One, not two.

### Step 9 — Hero + appeal pass（畫出來，補魅力）

Draw the hero in the locked style per its SVG 執行要訣. Then the appeal pass from
`references/appeal.md`: palette floor (≥4 roles, style-interpreted; 70%-rule is color-axis
only), statue check (one asymmetry unless symmetry IS the symbol), detail budget (≤4 charm
items, style-native traits don't count), same-grammar-clone check (vs your own previous
characters). Baby-schema dials in appeal.md; SVG conventions in `references/output-spec.md`.
Premium finish waits until after Step 10 (`references/rendering.md` — verify flat first,
render on frozen geometry).

### Step 10 — The three verifications（必做，出示證據）

Per `references/verification-tests.md`: **silhouette test** (all-black, full size + 64 px /
pixel-native), **extension test** (symbol+proportions constant, body bends — ≥2 with line of
action, 1 in-context mock, all in-style), **color test** (color-axis: hue swap breaks it;
else grayscale survives). Failures get revised AND shown — one honest before/after beats ten
claims.

---

## PHASE 3 — 商業化與交付

### Step 11 — Extensions, kit, and finish

Scale to the application ladder (output-spec.md): 貼圖 briefs → 6–8 stickers + labeled poses;
others → ≥4 expressions + 2 poses + 1 character-at-work scene (渴望 staged, props in hand).
Persona card = Step 3's profile compressed (3 keywords + bio + 口頭禪). Premium key visual
and/or AI prompt package per `references/rendering.md` when intake asked. Exports per the
Master + Export table — sticker-spec PNGs, circle-safe icons, print plates, pixel
nearest-neighbor, light GIF where surfaces benefit.

### Step 12 — IP bible + commercialization roadmap

Assemble the self-contained deliverable per output-spec.md. Full-pipeline briefs add the
Phase 1 artifacts and, per `references/commercialization.md`: 系列規劃 (variant axes, 12+1
blind-box convention where relevant, cast expansion hooks, the extensibility test — three
第二彈 themes needing no new symbol), the staged **rollout roadmap** (商標 → 貼圖+社群 →
小物 → 絨毛/盲盒 → 授權/聯名, each rung with its gate condition), **content pillars** derived
from the character's 習慣/口頭禪, a **KPI sheet** (5–7 metrics with check cadence), **商品化
檢核** (print/plush/figure feasibility gates), and **licensing readiness** notes (what a
licensor-grade style guide still lacks). If the plan involves a random-draw mechanic (盲盒/
扭蛋), run that reference's **稀缺性管理**（供給是稀缺性的一部分——熱期擴產是價值破壞）and
**合規關卡**（年齡門檻、機率揭露）. Full briefs also ship a **角色行為設定檔（golden
record）** — the Step 3 interior compressed into a machine-readable lore/性格/情緒幅度/護欄/
視覺不變量 file, which doubles as the licensing attachment and the AI prompt package's
canonical description. Honesty rules from that reference apply: sourced or labeled estimates,
gates not promises, 非法律意見 disclaimers.

### Step 13 — 確權與合規（Rights & Compliance）

Read `references/ip-protection.md` **when the brief is a full-pipeline IP, when any artwork was
AI-generated (i.e. whenever rendering.md Lane 3 ran), or when the user asks about 版權/商標/
可不可以商用**. Quick-mascot briefs read only its §1 and the Tier-0 list in §5. Produce the
確權與合規 block per that reference's §10 template. The three things most users get wrong, and
which this step exists to fix:

- **著作權是弱腿、商標是承重牆** — no jurisdiction's trademark law has an authorship
  requirement; copyright treatment of AI output differs sharply by market. Never tell a user
  "你擁有著作權"; state the market's position and what the workflow did to maximize the claim.
- **公開發表前**是商標 Tier-0 送件與（若適用）外觀設計專利的最後時點 — 絕對新穎性不可逆,
  and a hit character outruns its own trademark portfolio (the LAFUFU case).
- **創作歷程要即時留存** — prompt log, discarded outputs, hand-redrawn areas. An after-the-fact
  re-enactment has already lost in court. This pipeline's own discipline (a human-redrawn flat
  SVG identity master under any AI render) is the strongest evidence available — say so in the
  bible.

---

## Common failure modes — check your own work

- **畫得比想得快**: any drawing before Steps 2–3 exist on a full brief. The white-space
  statement and character interior are upstream of every pixel.
- **Lore-dump worldbuilding**: a 10-page epic nobody asked for. Both doctrines cap the world
  at what serves projection or empathy — 1 page.
- **Addition creep** / **Deleting to blandness**: props welded on ↔ <4 color roles, zero
  asymmetry, no charm and no recorded deadpan choice. Both fatal; the appeal pass arbitrates.
- **萬物皆軟糖 / Style tourism**: default-style outputs, or mixing conventions after the
  triptych locked one. The triptych exists so style is a *decision*.
- **Fake fan-out**: three directions that are one blob with different ears; a triptych of
  three kawaii flavors. Different constructions; genuinely different registers.
- **Twin symbols / Unextensible symbol / Same-grammar clone / Accidental clone / Lipstick on
  a guess** (premium render of unverified design): as before — amplify one thing, verify it,
  render only what passed.
- **Roadmap 畫大餅**: revenue promises, invented budgets. Gates and sourced numbers only.
- **稀缺性當提款機**: a blind-box plan whose only lever is 產量 — scarcity managed as an
  afterthought, or a mystery premium treated as the business's foundation rather than a
  bonus. The 2025–26 Labubu cycle is the worked example; commercialization.md has the rules.

## Originality guardrail

Famous IPs are analysis material and register references only. Genre conventions are free;
a specific IP's symbol combination never is. "Like Labubu" → extract the principle, amplify a
different feature, say so. This protects the user legally and competitively.

The same rule applies **inside AI prompts**: never put a brand, IP, or living-artist name into
a generation prompt — describe the register instead. Models reproduce recognizable IP from
prompts that never name it, and 2026 case law has been shifting liability toward the person who
prompts, publishes, and monetizes. `references/ip-protection.md` §7.

## Deliverables & language

Everything user-facing in the user's language (繁中 user → 繁中報告與設計書; keep 超級符號
terms bilingual where helpful). Send the bible/design sheet and hero via the file-delivery
tool when available. Rationale short and concrete; the deliverables speak.
