# Rendering Reference（精緻渲染層：完成度是疊上去的，不是改設計）

Read this when the brief wants more finish than flat identity art: a 精緻 hero illustration,
a product-render look, print textures, or AI-generated painterly art. Four lanes, one
doctrine:

**The finish ladder.** Identity assets (logo lockups, sticker masters, silhouette, spec
drawings) stay FLAT — that is what stays reproducible on a cup at 300 dpi and a favicon at
16 px. Premium finish applies to *presentation surfaces*: website hero, key visual, crowdfund
page, poster. Both levels ship from the same frozen master: run the design + verification
steps on the flat master first, THEN layer rendering on the approved geometry as a **separate
file**. Never redesign under the render; if the premium version needs different shapes, the
flat master was wrong — go back.

**Pipeline warning**: cairosvg does not implement most SVG filter primitives. Any artifact
using filters/gradient-heavy rendering must be rasterized via headless Chromium screenshot.
Keep the identity master filter-free; premium files carry the filters.

Pick the finish level at intake (完成度 question). Record the chosen lane and its parameters
as a 渲染規格 block inside the design sheet's 風格規格 section.

## 目錄（Contents）

- Lane 1 — 賽璐璐 Cel-shade（anime-grade vector）
- Lane 2 — 3D 潮玩渲染 Faux-3D toy render
- Lane 3 — AI 生圖 Prompt package（外部工具的精緻筆觸稿）
  - 模型選型：依工作分派，不依榜單第一
  - 角色一致性：2026 的方法優先序與硬數字
  - 系列 prompt 架構：fixed / variable 雙區塊
  - Negative prompt 的正確用法（2026 已分流）
  - 外部向量生成（Recraft 路線）與 SVG 母檔的關係
  - On-model drift checklist
  - Provenance log（確權用，不是選配）
  - 提示詞裡的原創性防線
- Lane 4 — 質感印刷 Print textures（水彩／riso／紙紋）
- Choosing a lane

## Lane 1 — 賽璐璐 Cel-shade（anime-grade vector）

The workhorse premium look; pure SVG, huge fidelity jump.

- **Light**: ONE fixed key light, typically ~45° upper-left or upper-right. State the
  direction in the 渲染規格 — every shadow obeys it.
- **Tones**: base + 1 hard shadow tone (「1影」) is the default. Add a 2nd darker tone (「2影」)
  only for occlusion (under chin, inside ears, between limbs). Optional 1 highlight tone.
  Edges 100% hard — no soft blends.
- **Shadow color**: never plain darker. Shift hue 10–25° toward blue/violet (warm key light),
  +5–15 saturation, −20–30 lightness. Never pure black shadows or pure white highlights.
- **Canonical shadow shapes**: under-jaw neck shadow (largest, sharpest), fringe/brow cast
  shadow, occlusion inside ears/under symbol, one big form shadow on the body's dark side.
  Few LARGE readable polygons — shadow noise is the amateur tell.
- **Highlights**: eye catchlight = large white circle upper-quadrant on the light side (+
  optional tiny secondary opposite); hair/head shine = one "angel ring" arc or zigzag band.
- **Rim light**: thin hard stripe (~2–4% of figure width) along the silhouette edge OPPOSITE
  the key light, sky-blue or complement-colored — instant "lit like a poster" separation.
- **SVG execution**: draw shadow shapes as loose paths in ONE translucent cool color (e.g.
  #2B2340 at ~30%, or `mix-blend-mode: multiply`) clipped by the body via `<clipPath>` — the
  clip lets shadow paths be sloppy while staying inside the lines. Rim light = offset inner
  path, same clip. At most one ≤15%-opacity vertical linearGradient for atmosphere.

## Lane 2 — 3D 潮玩渲染 Faux-3D toy render（blind-box product-photo look）

- **Volume**: per-part `radialGradient` with the center offset toward the light (cx≈0.35,
  cy≈0.30 for an upper-left key); stops: base +20–30% lightness → base → base −15–25% at the
  rim.
- **Material**: glossy vinyl = small hard white ellipse (5–10% of part width, 90–95% opacity)
  near the gradient center + broad soft sheen (white→transparent radial, 20–30% opacity).
  Matte vinyl = soft sheen only at 10–15%, NO hard dot. Declare the material in 渲染規格.
- **Ambient occlusion**: soft dark shapes at every contact/seam (head-body, limb joins): base
  hue −30–40% lightness, multiply, 30–50% opacity, blur 2–4 (at 512), plus a 1–2 px tight AO
  line right at the seam.
- **Ground shadow**: two layers — tight core (~35% opacity, blur ~3) + penumbra (~15%, blur
  8–12); width 70–90% of figure, height 15–20% of its width.
- **Extras**: 1–3 px light bevel on top edges; bounce light from the ground color on
  undersides at 10–15%; background = studio cyc sweep (vertical gradient, lightest band right
  behind the figure, 0→8% corner vignette).
- **True 3D option** (when headless Chromium available): build the character from Three.js
  primitives + `MeshToonMaterial` with a 3–5 step `gradientMap` (DataTexture with
  `NearestFilter` — otherwise it silently smooths) or `MeshMatcapMaterial` with a studio
  matcap; outline = duplicate mesh scaled 1.02–1.05, black, `side: BackSide`; renderer
  `{antialias: true, preserveDrawingBuffer: true}` → screenshot. Only worth it for
  turntables/multiple angles.

## Lane 3 — AI 生圖 Prompt package（外部工具的精緻筆觸稿）

This environment doesn't paint; when the user wants painterly/photoreal finish, compile the
design spec into a **prompt package** (`<name>-prompt-package.md`) their team runs in
external tools. Structure — all five parts:

1. **Canonical description**: one paragraph — unique name token, numeric proportions ("2.5
   heads tall"), palette as hex anchored to parts ("mist-blue #A3B6C1 body, copper #C7794A
   beak"), the super symbol named explicitly, style tags. This paragraph opens every prompt.
2. **Turnaround-sheet prompt**: "character reference sheet, front view, side view, back view,
   same character, neutral A-pose, plain white background…" — generate this FIRST, then use
   it as the reference image for everything else.
3. **Scene templates**: 3–5 prompts with [SLOT]s for situation/pose/mood, each restating the
   symbol.
4. **Per-tool parameter blocks** — see the model-selection and consistency subsections below.
5. **On-model drift checklist** — see the checklist subsection below.

### 模型選型：依工作分派，不依榜單第一

Model names and rankings move every few months (snapshot 2026-07). Two habits outlive any
version: **pick by the job, and read the editing leaderboard, not the generation one** — 80%
of IP work is "change one thing, keep the character", which is editing. On the generation
board GPT Image 2 leads by a wide margin, but on the editing board the top five sit within
~14 Elo of each other, i.e. effectively tied ([Artificial Analysis
生成榜](https://artificialanalysis.ai/image/leaderboard/text-to-image) ·
[編輯榜](https://artificialanalysis.ai/image/leaderboard/editing)). So choose on cost,
reference-image quota, and API convenience rather than on a headline rank.

| 工作 | 首選（2026-07） | 為什麼 |
|------|------------------|--------|
| 主視覺、改稿、雙參考身分轉移 | GPT Image 2 | 指令服從與對話式局部改圖最強 |
| 4K 印刷級、多角色同場 | Nano Banana Pro / Nano Banana 2 | 原生 4K + 內建多參考角色鎖定 |
| 風格化概念稿、世界觀探索 | Midjourney V8.1 | 美感天花板、moodboard 與 `--sref` 穩定 |
| 商品／包裝上的可讀文字 | Ideogram 4.0 或 GPT Image 2 | 字形與版面正確率高 |
| 向量母檔候選 | Recraft V4.1 Pro | 目前唯一原生輸出可編輯 SVG（見下） |
| 需自架、可控、可自訓 | Qwen-Image / FLUX.2 | 開源權重＋成熟 LoRA 生態 |

Record the chosen model **and its version string** in the 渲染規格 — a package that doesn't
say which model it was tuned for is not reproducible next quarter.

### 角色一致性：2026 的方法優先序與硬數字

Identity preservation moved *into* the models; the old adapter stack is now the fallback,
not the first move. Try in this order:

1. **模型內建多參考**（第一線）。**參考圖在 2026 已經「分槽」**——問題不是「丟幾張」，而是
   「哪張圖放哪個槽」。官方配額（[Gemini API
   docs](https://ai.google.dev/gemini-api/docs/image-generation)，2026-07 覆核）：

   | 模型 ID | object | character | style |
   |---------|--------|-----------|-------|
   | `gemini-3-pro-image`（NB Pro） | 6 | **5** | 3 |
   | `gemini-3.1-flash-image`（NB2） | 10 | **4** | — |
   | `gemini-3.1-flash-lite-image` | 14 | **無 character 槽** | — |

   turnaround sheet 放 **character 槽**、道具與場景參考放 object 槽。lite 版沒有角色槽，
   不要拿來做 IP 一致性工作。`gemini-2.5-flash-image` 為 legacy，應遷移。
2. **Midjourney `--oref <turnaround URL>` + `--ow`**（風格化 IP）。
   **⚠️ 引用任何 Midjourney 教學前先讀這一段**：官方文件寫明 Omni Reference「compatible with
   Midjourney version 7」，**V8 線（V8.2 為 2026-07 預設）沒有角色參考功能**——附上 `--oref`
   會讓該 prompt **自動改跑 V7**；`--cref`/`--cw` 則只在 v6/niji 6。所以角色工作必須**顯式
   pin `--v 7`** 並接受 V7 世代的美感，`--oref` 也**一次只吃一張參考圖**，且與 draft/fast
   模式、inpainting 互斥。`--ow` 範圍 1–1000、**預設 100**，鎖角色往上調但留意過高會連風格
   一起鎖死。想用 V8.1/8.2 的美感時，只用 `--sref` 做**風格**參考，角色仍由人重畫。
   網路上絕大多數教學仍在描述舊行為，這是本 lane 最常見的坑。
   （[Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997)、
   [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)）
3. **角色 LoRA**（量產或需要無限姿勢自由度時）。訓練集 20–40 張，**其中至少 6–8 張是非正面
   角度**；caption everything EXCEPT the character — the trigger word is the thing you don't
   caption.
4. **IPAdapter / InstantID / ControlNet**：降級為開源自架管線的選項，不再是預設建議。

**期望值要誠實**：pure-prompt 一致性約 65–75%，加角色 LoRA 約 85–92%，而**跨風格只有
75–85%**（[Apatero turnaround
指南](https://apatero.com/blog/ai-character-turnaround-sheet-generation-guide-2026)、
[Nowadais](https://www.nowadais.com/ai-character-consistency-guide-consistent-visual/)）。

**跨風格衰減警語（本 pipeline 特別容易踩）**：平面向量 → 3D 玩具渲染 → 絨毛材質屬於跨風格
轉換，衰減最嚴重的一段。做法不是換 seed 或換 LoRA，而是**每一次都重新餵 turnaround sheet 當
ground truth**，並逐項比對身分不變量（見 checklist）。

**turnaround sheet 是 Lane 3 的第一個產出物，不是選配**：一次生成四格拼版（front / 3-4 /
side / back，A-pose、白底、正交、無投影、每視角 ≥2048 px），因為它同時是後續多參考輸入、
LoRA 訓練集、以及 3D／打樣的參考來源。分四次生成必然對不齊。

### 系列 prompt 架構：fixed / variable 雙區塊

做「一整套」（12+1 盲盒、六款貼圖主題、四季節慶版）時，一致性靠的不是運氣而是**鎖死結構
變數、只變主題變數**：

```
[FIXED — 角色 DNA]   頭身比 / 五官與眼睛規格 / 超級符號一句話 / 部位色票 hex / 材質
[FIXED — 產品規格]   打光與背景（白底柔光棚拍）/ 底座形制 / 構圖與裁切 / 無文字約束
[VARIABLE — 本款]    主題 / 服裝 / 輔色 / 手持配件 / 底座裝飾
```

FIXED 兩段逐字複製到每一款的 prompt，只換 VARIABLE。潮玩品類的五個不可省元素：材質
（`glossy vinyl finish` 或 `matte vinyl`）、`oversized head relative to body`、眼睛規格
（`large glossy eyes with star catchlights`）、底座、以及 no-text 約束；配色公式是 1 主色 +
1–2 輔色 + 白／奶油中性色，**避免漸層——扁平微飽和才像塑膠**
（[GPT Image 2 blind-box prompt 指南](https://imini.com/blogs/gpt-image-2-blind-box-prompt)）。
這份 FIXED 區塊直接由 `commercialization.md` 的角色行為設定檔第 6 節（視覺不變量）填寫。

JSON schema 形式的 prompt 也可以，但要誠實看待它的價值：**它讓 prompt 可版控、可被團隊複用**，
沒有證據顯示模型端會因此畫得更好。最終仍轉成自然語言送出。

### Negative prompt 的正確用法（2026 已分流）

一句「加 negative prompt」在 2026 已經是錯的，因為三類工具的機制不同：

- **開源／自架**（SD、FLUX、Qwen-Image）：有真正的 negative 欄位與 CFG，照舊有效。
- **閉源對話式**（GPT Image 2、Nano Banana 系列）：**沒有 negative 欄位**。排除項要寫進正向
  敘述，而且「不要出現 X」有時反而召喚 X ——**改成正面描述替代物**：不寫 "no cluttered
  background"，寫 "clean seamless white studio background"。
- **Midjourney**：用 `--no` 參數。

仍然通用的排除清單（依風格調整）：off-model、inconsistent colors、different character、
extra limbs、realistic。

### 外部向量生成（Recraft 路線）與 SVG 母檔的關係

本 pipeline 的 identity master 是**手工撰寫的 SVG**，這一點不變——因為母檔要能被逐段控制、
diff、與驗證。但 2026 起多了一條可用的外部路徑：Recraft V4 / V4.1 Pro 會**原生輸出具名圖層、
乾淨錨點、可編輯填色的 SVG**（直接以 path 構圖，不是把點陣圖 auto-trace），Pro 版
2048×2048，檔案約 24–144 KB（[Recraft
docs](https://www.recraft.ai/docs/recraft-models/recraft-V4)、[Ropewalk 實測
指南](https://ropewalk.ai/blog/recraft-v4-pro-svg-guide-2026)）。

- **取得向量的三條路，品質分明**：(a) 原生 path 生成（可用作草稿基礎）＞(b) 點陣後
  auto-trace（節點髒、不可維護，**僅限救急**）＞(c) 純手繪（母檔仍走這條）。
- **SVG-friendly 約束詞**：`flat vector illustration`、`limited palette (N colors)`、
  `consistent line weight`、`uniform grid`、`solid fills, no gradients`、`no photorealism`、
  `no fine texture`。
- **已知失敗模式**：寫實光影、漸層網格、大量小字、密集重疊場景——這四項別要求。約 15% 的
  密集構圖需要人工清 path，交付前檢查節點數、圖層命名、色票是否對應品牌色。
- **紀律不變**：外部生成的向量進到本流程後，仍要通過 subtraction、appeal pass 與三項驗證才
  能成為 identity master。工具換了，關卡沒換。
- **⚠️ 先確認方案層級**：Recraft **免費層生成的素材由 Recraft 擁有且禁止商業使用**。要拿來做
  商用母檔基礎前務必確認訂閱層級。各家生圖平台的素材歸屬與補償條款差異極大，見
  `references/ip-protection.md` §8。

### On-model drift checklist

每一張生成圖都對照 flat master 逐項打勾：silhouette 是否吻合？部位色票 hex 是否正確？超級
符號是否存在且未被改動？頭身比是否正確？眼型與髮際線／標誌性配件是否一致？

誠實的警告：**精細的符號細節正是模型最會漂移的地方**。identity-preservation 一代（Nano
Banana / GPT Image 2 級）縮小了差距但沒有消除——實測中 GPT Image 2 在雙參考身分轉移拿 5/5，
Nano Banana 2 只有 3/5，臉部保真會往插畫風漂移（[Vidguru 10 項盲
測](https://www.vidguru.ai/blog/nano-banana-2-vs-gpt-image-2-comparison.html)）。所以是
每一張都檢查，不是抽查。

### Provenance log（確權用，不是選配）

Lane 3 的最後一個產出物。記錄：模型與版本字串、完整 prompt、參數與 seed、**保留與捨棄的輸出
分別是哪些**、哪些區域是人工重畫或 inpaint 的。這只多一個檔案，卻是日後主張著作權時唯一能拿
得出來的東西——**事後重演的生成過程已經在中國法院敗訴過**。這一份紀錄同時服務四個目的（美/韓
證明人類作者、中國證明獨創性、日本反駁依據性、維持平台補償條款資格），細節見
`references/ip-protection.md` §3–§4。

順帶一提，本 pipeline 天然佔優勢：**identity master 是人工重畫的 flat SVG，AI 生圖只是
presentation 層**。這條原本為印刷可重製性而設的紀律，恰好是最強的人類創作貢獻證據——記得在
IP bible 裡明說。

### 提示詞裡的原創性防線

**絕不在提示詞中放入任何品牌名、角色名或在世藝術家姓名**，包括「像 Labubu 那樣」。改用 register
的文字描述（「deadpan、無眉、寬距眼、啞光乙烯基質感」）。理由不只是原創性：模型會在提示詞完全
未提及該 IP 的情況下生出可辨識的知名角色，而 2026 年的判決趨勢正把責任推向**下提示、發布、
變現的那個人**。見 `references/ip-protection.md` §7。

## Lane 4 — 質感印刷 Print textures（水彩／riso／紙紋）

- **Watercolor edge**: `feTurbulence type="fractalNoise" baseFrequency="0.02–0.05"
  numOctaves="3–5"` → `feDisplacementMap scale="5–15"` (subtle) or 20–30 (heavy bleed).
- **Granulation**: second fractalNoise at baseFrequency 0.7–1.0 → feColorMatrix into alpha →
  `feComposite operator="in"` against the shape for interior speckle; pooled-edge darkening =
  inner stroke, same hue, 8–12% opacity, 1–2 blur. Washes = overlapping multiply fills at
  30–60% so overlaps glaze-darken.
- **Paper grain**: fractalNoise baseFrequency 0.04 / numOctaves 5 → `feDiffuseLighting
  surfaceScale=2` + `feDistantLight azimuth=45 elevation=60`, overlaid at 5–10% opacity.
- **Risograph**: 2–3 spot inks (classic: fluoro pink, blue, teal, orange, black), each ink a
  separate layer mixed via multiply (pink×blue→purple); no smooth gradients — tone via
  halftone `<pattern>` (6–10 px cell, circle r 1–4, `patternTransform` rotate 15°/45°/75°
  per ink); misregistration = translate each ink layer 1–3 px (± slight rotation) — a
  feature, not a bug; avoid tints below ~20% (dots break up).
- **Performance**: filters are expensive — cap numOctaves at 5, scope filter regions, apply
  to grouped layers not per-element, prefer `<pattern>` over filters where possible. These
  files rasterize via Chromium, never cairosvg.

## Choosing a lane

- 官網主視覺 / key visual / 開幕海報, anime-adjacent register → cel-shade
- 盲盒/公仔/募資頁 product feel → faux-3D (declare glossy vs matte)
- 出版、選物、文青印刷品 → print textures (riso for edge, watercolor for warmth)
- 客戶團隊自己要量產宣傳圖、要筆觸感 → prompt package (on top of whichever visual lane)
- 客戶團隊要自己出「一整套」（12+1 盲盒、節慶版、多角色場景）→ prompt package，且務必交付
  turnaround sheet 與 fixed/variable 雙區塊模板，否則第三款就開始走鐘

Verification still rules: the silhouette/extension/color tests run on the FLAT master; the
premium file must overlay-match the master's geometry (same shapes under the shading). A
gorgeous render of an unverified design is lipstick on a guess.
