# Style Library（風格庫）

Style is a register choice, separate from the methodology. The super symbol, subtraction,
appeal budget, and all verifications apply in EVERY style — style decides how the surviving
elements are *drawn*. The default trap is「萬物皆軟糖」: rendering every brief in the same soft
flat-kawaii look. Style must be chosen consciously (the style triptych step), locked before
the hero, and recorded in the design sheet as a 風格規格 (style spec).

## 目錄（Contents）

- Choosing（如何選風格）
- 11 條風格條目：1 軟糖圓潤 · 2 盲盒潮玩 · 3 幾何極簡 · 4 復古橡膠管 · 5 像素 · 6 蠟筆手繪 ·
  7 繪本風 · 8 緩角色 Yuru-chara · 9 昭和レトロ · 10 貼紙塗鴉 · 11 電競狂野
- Style research protocol（用戶點名庫外風格時）
- Style × methodology interactions

## Choosing

- User named a style or reference → use the matching entry below; if not covered (or covered
  thinly), run the **Style research protocol** at the end of this file.
- User didn't specify → shortlist 2–3 entries that fit brand register + application, offer
  them in the intake form, and make the style triptych span genuinely different registers so
  the user compares real options, not palette swaps.
- Fixed schema per entry: 氣質 / 視覺語法 / SVG 執行要訣 / 語感參照 / Right for / Wrong for /
  常見翻車. These are anchors, not prescriptions — commit at 80%, don't average styles.

---

## 1. 軟糖圓潤 Soft flat-kawaii（one option among many — not the default）

- 氣質: 溫暖、安全、萌
- 視覺語法: rounded primitives, 2 頭身, bold warm-dark outline, flat fills + companion shade,
  catchlight + blush
- SVG: one consistent stroke 8–12u @512, `stroke-linejoin/linecap="round"`
- 語感參照: LINE FRIENDS, Sanrio adjacents
- Right for: stickers, kids, F&B loyalty. Wrong for: edgy gaming, luxury, industrial B2B
- 常見翻車: default-picking it without a decision — that is how every mascot converges

## 2. 盲盒潮玩 Blind-box designer toy

- 氣質: 冷面、精品、收藏慾
- 視覺語法: matte flat vinyl look, **no outlines**, head:body ≈ 1:1, no neck; deadpan face —
  large wide-set glossy eyes (dark iris + 1–2 specular dots), no brows, tiny pout or no mouth,
  faint blush; muted sophisticated palette (cream/dusty pink/sage/butter, never loud
  primaries); creepy-cute variant: one unsettling feature (Labubu's serrated grin)
- SVG: `stroke="none"`, flat fills, ONE soft shading pass only (5–12% darker shape under
  chin/head)
- 語感參照: Molly, Labubu register (register only — never their symbols)
- Right for: 潮流品牌、收藏系列、IG 人設. Wrong for: kids education, government
- 常見翻車: adding a big smile or outlines — kills the blank projection-screen quality

## 3. 幾何極簡 Corporate flat / tech mascot

- 氣質: 可靠、工程師友善、可規格化
- 視覺語法: visible primitives (circles, capsules, rounded rects), near-symmetry, flat fills,
  minimal or no outline, 1–3 brand colors + neutrals, one darker flat tone max; huge wide-set
  eyes + simple mouth, zero aggression
- SVG: primitives with named ratios — the construction should read like a spec
- 語感參照: Go gopher, Octocat, Duolingo owl
- Right for: dev tools, SaaS, B2B (deadpan register). Wrong for: craft/handmade brands
- 常見翻車: texture/gradient that dies at 16 px favicon; sneaking in organic sketchiness

## 4. 復古橡膠管 1930s rubber-hose

- 氣質: 復古、彈跳、爵士
- 視覺語法: limbs are unjointed curved tubes (no elbows/knees); pie-cut eyes (tall black oval
  with a wedge notch, NO pupils inside); 3-finger gloves, oversized pill shoes; body = stacked
  circles/pears; everything bounces — S-curve spine, feet mid-hop; palette = aged-paper cream
  (≈#F4E3C1) + sepia-black lines (not pure #000) + 1–2 desaturated accents (dusty
  red/mustard/teal)
- SVG: limbs as single cubic Béziers with thick uniform stroke, `stroke-linecap="round"`;
  pie-cut = black ellipse + background-color wedge path
- 語感參照: Steamboat Willie, Fleischer cartoons, Cuphead (genre, not characters)
- Right for: craft beverage, vintage brands, music venues. Wrong for: clean-tech, medical
- 常見翻車: modern jointed limbs; pupils inside pie eyes; sterile pure black-on-white with no
  aged tint

## 5. 像素 8-bit / 16-bit pixel

- 氣質: 復古遊戲、玩心、社群梗
- 視覺語法: absolute grid discipline; palette caps (8-bit ≈ 3–5 colors + transparency; Game
  Boy = 4 greens #0F380F/#306230/#8BAC0F/#9BBC0E; 16-bit ≤ ~15); outline pure black OR
  "selout" (outline darkens to match adjacent fill); flat color blobs, dithering sparse and
  16-bit only; oversized head, 1–2 px eyes; must read at native 16×16 or 32×32
- SVG: integer-coordinate `<rect>`s (or unioned paths) in a native-size viewBox (16/32/48),
  `shape-rendering="crispEdges"`, scale by width/height only. **Any non-integer coordinate is
  a "mixel" — an instant style break.** With raster tools (PIL) available, authoring the
  native PNG directly is equally valid — keep SVG and PNG masters in sync, and export
  upscales nearest-neighbor at integer multiples only (see output-spec.md Master + Export).
- 語感參照: SMB1 Mario (16×16), Mega Man, GB Kirby
- Right for: indie games, dev communities, retro events. Wrong for: premium print, plush-first
- 常見翻車: mixels, too many colors, pillow-shading, anti-aliased edges

## 6. 蠟筆手繪 Child-crayon / faux-naïve

- 氣質: 童趣、手感、無防備
- 視覺語法: wobbly uneven outlines with overshoot ends and re-stroked passes; fills
  mis-registered (color escapes the lines / leaves white gaps) and scribble-hatched rather
  than solid; tadpole-figure proportions, skewed circles, corner-sun logic; crayon primaries
  (#EE204D/#1F75FE/#1CAC78/#FCE883) on paper white; wobble must be irregular — uniform
  algorithmic wiggle reads fake
- SVG: hand-jittered path nodes (irregular spacing); 2–3 overlapping strokes at 60–80%
  opacity, round caps; fills as separate offset blobs (translate 2–4u, slight rotate) or
  zigzag polyline hatching; optional feTurbulence+feDisplacementMap for tooth
- Pro trick: composition and silhouette stay CONTROLLED; only execution is naive
- 語感參照: Crayon Shin-chan title cards, Oliver Jeffers
- Right for: kids education, family brands, workshops. Wrong for: fintech, security
- 常見翻車: perfect fills inside perfect wobble = instantly fake; forgetting that the
  silhouette still has to pass verification

## 7. 繪本風 Picture-book（Bruna 硬邊 or 水彩軟邊）

- Bruna register: single uniform-weight outline with micro-wobble (slow brush feel); strictly
  frontal or full profile — never 3/4; flat unmodulated fills from a fixed ~6-color palette;
  face = two wide-set black dots + minimal mouth (Miffy's ×); zero shading, white = paper
- 水彩 register: no/broken outline; layered translucent organic blobs (stacked 20–40% opacity
  paths, subtle grain), warm muted palette, cream background
- SVG: Bruna — one stroke ≈2–3% of figure height, irregular nodes; watercolor — opacity
  stacking, no hard geometry
- 語感參照: Miffy; Guri and Gura
- Right for: publishing, baby brands, quiet cafés. Wrong for: esports, tech edge
- 常見翻車: Bruna style at 3/4 angle; adding gradients/shadows

## 8. 緩角色 Yuru-chara / loose mascot

- 氣質: 憨、在地、不完美即魅力
- 視覺語法: one giant sphere/pear (head fused to body — foam-suit logic), no neck, stubby
  wide-set arms, tiny feet; face floats small on a huge blank area; local-motif mashup worn or
  fused (green onions, landmark hat); flat naive colors, thin-or-no outline; slight imperfect
  symmetry (features nudged 1–2% off-center)
- SVG: deliberately simple shapes; nudge transforms for off-center charm
- 語感參照: Kumamon, Funassyi, Hikonyan
- Right for: 地方品牌、觀光、活動. Wrong for: premium/minimal brands
- 常見翻車: over-polishing — sleek geometry and dynamic poses destroy the「緩」; designing a
  body no costume-maker could build

## 9. 昭和レトロ Shōwa retro print

- 氣質: 喫茶店、懷舊、溫柔的舊時光
- 視覺語法: 2–4 spot-color print look with deliberate misregistration (fills offset 1–3u from
  outlines); halftone-dot tints; outline dark brown/navy (≈#3A2A1E), never pure black; aged
  cream ground; palette = cream/vermillion/mustard/olive/chocolate, low-saturation "faded
  print"; chunky rounded figures, oval eyes with big highlights, rosy cheeks, open cheerful
  mouth
- SVG: offset fill groups; `<pattern>` of dots for tints
- 語感參照: Peko-chan, Sato-chan, kissaten menu art
- Right for: 咖啡/甜點/選物店、復古企劃. Wrong for: cutting-edge tech
- 常見翻車: crisp perfect registration + neon colors + pure black = modern flat, not 昭和

## 10. 貼紙塗鴉 Sticker doodle

- 氣質: 聊天室、直播、梗圖友善
- 視覺語法: die-cut white border around the whole silhouette; uniform marker-weight bold dark
  outline; ONE exaggerated emotion per sticker (oversized tears/sweat/anger cross/sparkles);
  flat fills + at most one cel-shade tone; must read at ~120 px on any chat background
- SVG: duplicate the union silhouette underneath with white fill + white stroke ≈8–16u (of
  320u canvas), round joins
- 語感參照: Brown & Cony (deadpan × hyper-expressive pairing)
- Right for: LINE/Telegram sticker packs, stream overlays. Wrong for: print-first brands
- 常見翻車: thin lines that vanish at chat size; skipping the white border (melts into dark
  mode); lukewarm mid-intensity emotions

## 11. 電競狂野 Esports / bold sports mascot

- 氣質: 侵略、速度、隊魂
- 視覺語法: angular grammar — straight edges, sharp points, hard curves; head in 3/4 with
  forward lean, V-brow, often pupil-less glowing eyes; thick outer contour + inner keyline;
  2–3 aggressive colors + black/white; flat hard-edged polygonal cel shadows; badge-compatible
  contained silhouette
- SVG: double-stroke via stacked copies or `paint-order: stroke`; polygon shadow shapes
- 語感參照: classic wolf/lion esports crests
- Right for: teams, gaming gear, events. Wrong for: 溫暖日常品牌
- 常見翻車: gradients + many colors (dies on jerseys/32 px); timid static front pose

---

## Style research protocol（用戶點名庫外風格時）

When the user names a style, era, artist-genre, or reference IP this library doesn't cover
well ("水墨風", "Y2K", "像 Ghibli 那種", "我們美術館的版畫感"):

1. **Research before drawing.** If web tools are available, run 3–6 searches on the style's
   *conventions* (line art, palette, proportions/anatomy, plus one search for its classic
   beginner mistakes). Prefer practitioner guides and formal analyses over image walls. No
   web access → use the nearest library entry and state the approximation openly.
2. **Analyze in this fixed order** (constraints explain conventions): medium constraints →
   line quality (weight, uniformity, taper, wobble, caps) → shape language → proportion
   system → palette discipline (hue count, saturation register, background relationship) →
   rendering model (flat/cel/painterly/textured) → facial encoding (eye spec, mouth spec,
   brow presence) → motif vocabulary → the style's classic beginner mistake.
3. **Write the 風格規格 (style spec)** into the design sheet: 5–8 conventions with concrete
   SVG execution notes, 語感參照 flagships, the failure mode to avoid, and reference sources
   (linked) when researched. The spec is written BEFORE the hero and governs every artifact.
4. **Originality boundary**: genre conventions are learnable and free to adopt (pie-cut eyes,
   sticker borders, foam-suit proportions); a specific IP's symbol combination is not. "Like
   Cuphead" yields the 1930s grammar — never a pie-eyed round-eared mouse in red shorts.

## Style × methodology interactions

- The super symbol must survive the style: pixel symbols read at native grid; crayon symbols
  live in the *silhouette*, since lines wobble.
- Verifications run in-style: silhouette test uses the styled contour; the small-size check
  uses the pixel native size for pixel style; extension variants stay in the locked style.
- The appeal pass adapts: style-native traits (crayon wobble, pixel palette caps, blind-box
  deadpan) are the style, not detail-budget spends; the budget governs *added* charm on top.
- Genre-mandated wear (rubber-hose gloves, yuru-chara local motif) counts as style grammar,
  not welded-on props — but it must stay generic to the genre, never copied from a specific
  IP.
