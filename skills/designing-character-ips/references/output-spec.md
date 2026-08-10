# Output Spec（SVG 規範與 IP 設計書結構）

## 目錄（Contents）

- SVG conventions（SVG 規範）
- File set to deliver（交付檔案清單）
- Master + Export（母檔與輸出格式）
- IP design sheet structure（設計書／IP bible 結構）
- Delivery（交付方式）

## SVG conventions

Consistency here is what makes the character redrawable and the tests executable. **These are
the defaults — the locked style's 執行要訣 (style-library.md or a researched style spec)
overrides line, fill, and shading rules where they conflict** (pixel style demands crispEdges
integer rects; crayon demands wobbled multi-pass strokes and misregistered fills; blind-box
demands strokeless matte). What never changes: named groups, no embedded raster, transparent
background, and the file set below.

- `viewBox="0 0 512 512"`, transparent background, character centered with ~8% margin.
- **Flat fills** by default — no gradients, no texture. (A gradient breaks silkscreen and
  embroidery reproduction on merch.) But flat ≠ single-tone: the 4-role palette from
  `appeal.md` applies — companion-shade patches (inner ear, belly), warm accent areas, and a
  flat ground-shadow ellipse in scenes/mocks are allowed and encouraged. Only the identity
  hero stays shadow-free.
- Strokes: either strokeless (pure flat shapes) or one consistent outline weight throughout
  (8–12 units at 512, warm dark rather than pure black, `stroke-linejoin="round"`,
  `stroke-linecap="round"`). Never mix. A bold consistent outline is strongly recommended for
  sticker and kids briefs — it is what keeps characters legible at 100 px.
- Structure the file with named groups so variants are mechanical edits:

  ```xml
  <g id="body">…</g>
  <g id="symbol">…</g>   <!-- the super symbol geometry, isolated -->
  <g id="face">…</g>     <!-- the parts that move in extension variants -->
  ```

- Prefer primitives (`circle`, `ellipse`, `rect rx=`) and few-node paths over complex paths.
- No `<text>` elements inside the character; no embedded raster images. If you label grid or
  scene cells with CJK `<text>` baked into a master SVG, note it renders as tofu in cairosvg —
  render those via headless Chromium, or keep the labels in the HTML sheet rather than the
  master SVG.

## File set to deliver

Use the character's working name (romanized, kebab-case) as the base:

| File | Content |
|------|---------|
| `<name>.svg` | Hero: front-facing base character, color |
| `<name>-silhouette.svg` | All-black duplicate (see verification-tests.md) |
| `<name>-extensions.svg` | Grid: expression variants + dynamic poses, each labeled with use |
| `<name>-scene.svg` | The character-at-work scene (props/context live here) |
| `<name>-design-sheet.html` | Self-contained design sheet / IP bible, all SVGs inlined |
| `<name>-premium.svg` + `.png` | (premium briefs) Rendered key visual per rendering.md — PNG via headless Chromium, since filters die in cairosvg |
| `<name>-prompt-package.md` | (when requested) AI-generation prompt package per rendering.md |

For 貼圖 briefs, add the sticker set as individual cells or one sheet (LINE spec: main
240×240, stickers up to 370×320, tab 96×74 — note the spec in the sheet even if delivering
SVG masters).

## Master + Export（母檔與輸出格式）

SVG is the **master format**, not the only format. It stays the source of truth because it is
resolution-independent, mechanically recolorable, diff-able, and it makes the verifications
executable (a silhouette test is one fill change). But surfaces have native formats, and a
deliverable that stops at SVG pushes conversion work onto the user. **Export from the masters
to whatever each surface actually ingests**, whenever rendering tools are available:

| Surface | Deliver |
|---------|---------|
| LINE/Telegram stickers | Transparent PNG at spec (LINE: 370×320 max, ≤1MB, main 240×240, tab 96×74) |
| App/Discord/community icon | PNG 512 + 128 + 48 (circle-crop-safe for Discord); ICO or 32/16 PNG for favicon |
| Stream overlay / web hero | Transparent PNG at 2×; optional light animation (see below) |
| Print (cup, coaster, apron, standee) | High-res PNG (≥300 dpi at physical size) or PDF; one-color plate version; note CMYK/Pantone approximations in the sheet |
| Pixel style | Native-size PNG + nearest-neighbor upscales (×4/×8/×16); GIF for animated sprites |
| Plush/vendor | Dimensioned spec sheet (PNG/PDF) with callouts |

Tooling: check what's installed and use what's there — `cairosvg`/`resvg`/Inkscape or headless
Chromium for SVG→PNG (Chromium handles CJK fonts and filters most faithfully); PIL/Pillow for
pixel-native authoring and nearest-neighbor scaling; PIL or ffmpeg for GIF assembly. Install
quietly if missing and permitted. If NO raster tooling is available, deliver SVG masters +
the self-contained HTML sheet (browsers render those anywhere) and state which exports the
user still needs, with exact sizes.

**Pixel style caveat**: author at the native grid; export nearest-neighbor at integer
multiples only. Never let a scaler smooth pixel art.

**Light animation is in scope** when the surface benefits (stream badge blink, neon flicker,
sticker shake): 2–4 frame GIF from SVG frame exports, or SMIL/CSS animation inside the
SVG/HTML sheet. Keep loops subtle and ≤ 4 frames — character animation beyond that is a
different discipline; don't wander into it uninvited.

## IP design sheet structure（設計書／IP bible 結構）

Use this exact section order, in the user's language. Quick-mascot briefs use the core
sections; full-pipeline briefs (scope ladder) add the ⊕ sections from Phase 1 and Phase 3:

```
# <角色名> — IP 設計書 / IP Bible

⊕ ## 市場分析報告      （market-research.md 模板：概況/競品地圖/受眾/空白定位/商標初檢/文化檢核）
⊕ ## 定位宣言與敘事教義 （white-space 定位一句話 · Sanrio 極簡投射 vs San-X 微敘事的選擇與理由）
⊕ ## 世界觀             （一句話設定/世界規則/基調/配角掛鉤/kept mystery）
⊕ ## 角色深度設定       （價值觀/渴望/害怕/習慣/關係/說話方式/行為規則/禁忌清單/反差/口頭禪）

## 定位摘要
品牌/產品一句話 · 受眾 · 個性三關鍵詞 · 主要應用場景 ·（完整 pipeline）空白定位一句話引用
·（快速吉祥物 briefs）市場快照：2–3 句競品/motif 快掃與撞名/撞motif 檢查就放這裡，不另開報告
（若有假設，在此標明「以下為假設」）

## 風格規格（Style Spec）
所選風格與一句話理由 · 風格三聯圖的取捨紀錄 · 5–8 條視覺語法（線條/形狀/比例/色彩/上色模型/
五官編碼）· SVG 執行要訣 · 語感參照 · 該風格的經典翻車點 ·（若經網路研究）參考來源連結 ·
（精緻完成度時）渲染規格：所選 lane、光源方向、陰影色相偏移/材質宣告/紋理參數等關鍵數值

## 超級符號（Super Symbol）
一句話定義 + 幾何描述 + 所選放大軸（五官/形態/色彩）+ 為什麼選這條軸（2–3 句）+
一個反差（the gap）

## 性格卡（Persona）
個性三關鍵詞 · 一句帶掙扎感的小傳 · 口頭禪一句 · 喜歡/害怕各一（選填）

## 造型規格
頭身比 · 構成幾何（圓/膠囊/圓角矩形…）· 關鍵比例（符號相對頭部的尺寸）·
延展時不可變動的是「符號幾何＋比例」，不是凍結整條輪廓

## 色彩系統
四個色彩角色（主色/深一階同色/五官深色/暖彩點綴）各附 hex；面積配比（60-30-10；
色彩軸角色才適用 70%+ 單色規則）；灰階/單色印刷時的處理方式

## 驗證結果
剪影測試（全尺寸 + 64px，附圖與判定）· 延展測試（變體網格，附圖與判定）·
色彩測試（換色或灰階，附圖與判定）· 若有修訂，附 before/after

## 延展示範
表情/姿勢變體（含動態姿勢，附用途標註）· 角色工作情境圖（character-at-work scene）·
一項以上應用示意（貼圖/杯印/icon）

## 使用守則（Don'ts）
5–8 條，每條一行。Don'ts 只保護「符號」：最小使用尺寸、不可改變符號比例、不可鏡射符號、
不可在基底身體上加道具服飾、（色彩軸角色）不可替換主色等。**不要**寫出禁止表達的規則——
不設全面旋轉角度上限、不凍結眼睛尺寸，姿勢與表情本來就該自由。

## 方向附錄（未選的方向與風格）
概念發散未被選擇的兩個方向縮圖 + 各一句 pitch，以及**風格三聯圖**（同一概念的三種風格版本
＋各自的取捨與推薦理由）——讓業主看見所有取捨，也保留改選的可能

## 命名候選（若角色未命名）
2–3 個名字候選，各附一句理由——名字應呼應超級符號或反差，而不是呼應行業；
已通過商標初檢者標注（附非法律意見聲明）

⊕ ## 系列規劃          （變體軸/12+1 慣例（盲盒）/配角擴充掛鉤/延展性測試：三個不需新符號的第二彈主題）
⊕ ## 商業化 Roadmap    （commercialization.md：商標→貼圖+社群→小物→絨毛盲盒→授權聯名，各階附 gate 條件，分 0–3月/3–12月/12月+）
⊕ ## 內容支柱          （3–4 個，各附示範貼文與頻率）
⊕ ## KPI               （5–7 個指標＋檢查週期）
⊕ ## 商品化檢核        （印刷/絨毛/公仔可行性 gate 的通過狀況）
⊕ ## 授權就緒度        （licensing style guide 已備/待補清單）
⊕ ## 確權與合規        （ip-protection.md §10：著作權現況/創作歷程留存/商標佈局/外觀設計專利
                       時點/生圖工具與條款/AI 標示/公開前待辦。任何用到 AI 生圖的案子必附）
```

## Delivery

- Send the design sheet HTML and the hero SVG via the available file-delivery tool; mention
  the other files in one line.
- Keep the chat message short: the sheet speaks for itself. One or two sentences on the chosen
  axis/style and the one design decision most worth the user's attention.
- If any verification came out marginal, say so in the chat message too — don't let a marginal
  result hide in the sheet.
