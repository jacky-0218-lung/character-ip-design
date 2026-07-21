# Verification Tests（三項驗證的執行細節）

These tests are the difference between a designed IP and a drawn one. Each produces a real
artifact that goes into the design sheet. Run all three; report results honestly, including
marginal passes and the revisions they triggered.

## 1. Silhouette test（剪影測試）

**Claim being tested**: strip every element — only a black shape remains — and the character is
still identified in one second.

**Procedure**

1. Duplicate the hero SVG.
2. Set every `fill` to `#000` and remove or blacken internal strokes/details, so only the
   outer contour (plus any *holes* fully enclosed by the contour, like the gap between ear and
   head) remains visible.
3. Render the silhouette beside the color hero at two sizes: full size (~512 px) and small
   (~64 px, favicon scale; for pixel style use the native grid size). Embed both in the sheet.

**Pass criteria** — all three:

- **Self-identity**: someone who saw the color version once can pick this silhouette out and
  name it. Practical proxy: the super symbol is clearly legible in the black shape.
- **Distinctness**: not confusable with a famous IP silhouette. Run these quick collision
  checks — round head + two round ears → Mickey risk; cat contour + head-bow → Hello Kitty
  risk; long vertical ears + dot face → Miffy risk; pear body + center seam → Doraemon risk.
  If a collision appears, adjust proportion or angle of the symbol, not by adding elements.
- **Small-size survival**: at 64 px the symbol still reads. If it vanishes, amplify scale or
  purify geometry.

**Note for facial-axis and color-axis symbols**: a facial symbol (e.g., missing mouth) may not
survive in the silhouette itself — that is acceptable *if* the overall contour is still
distinctive and ownable (Hello Kitty's silhouette works via head-bow and proportions). In that
case say so explicitly in the design sheet, and hold the *contour* to the distinctness and
small-size bars. A color symbol must likewise be backed by a clean, ownable contour, because
color disappears in silhouette by definition.

## 2. Extension test（延展測試）

**Claim being tested**: the symbol is infinitely extensible — expressions, poses, and
applications don't erode it.

**Procedure**

1. Produce a variant set scaled to the brief's top application:
   - 貼圖/chat brief → 6–8 expression stickers (混合禮貌用語與日常情境; include text-free
     poses) + 3–4 labeled poses with usage notes;
   - other briefs → ≥ 4 expression variants + 2 poses + 1 in-context **character-at-work
     scene** (props in hand or beside — the barista actually pouring; real scene, not a bare
     white card).
2. Consistency rule while drawing variants: **the super symbol and the proportion ratios stay
   constant — but the body may bend, tilt, and turn.** At least 2 variants must show a clear
   **line of action** (head/body tilt ≥ 8° or clearly asymmetric limbs). Off-model policing
   means protecting the symbol's geometry and the head-body ratio, NOT freezing one contour —
   six copies of an identical byte-frozen body is a failed extension test by monotony.
3. Arrange the variants in one grid image/SVG for the design sheet, each cell labeled with its
   use (早安貼圖 / 官網 hero / icon…).

**Pass criteria**: cover the variants' faces or captions — every variant is still obviously the
same character; the symbol is present and unmodified in each; and the set contains at least
one genuinely dynamic pose and one in-context scene.

## 3. Color test（色彩測試）

Two different claims depending on the chosen axis:

**If color IS the axis** — swapping the dominant hue should *break* identity.

1. Duplicate the hero; replace the signature hue with a distant hue (e.g., 薄荷綠 → 橘).
2. Pass = the swapped version genuinely reads as "a different character". If it still reads as
   the same character, the color wasn't carrying the identity — either commit the color harder
   (≥ ~70% of body area, more distinctive hue) or admit the real symbol lies elsewhere and
   re-choose the axis.

**If color is NOT the axis** — the character must survive without color.

1. Produce a grayscale version of the hero.
2. Pass = still immediately recognizable. Failure means the shape/face isn't doing the work
   and the design is secretly leaning on palette — return to subtraction and strengthen the
   symbol.

## Rendering notes（在這個環境怎麼跑）

- The cheapest reliable path: build the design sheet as a single self-contained HTML file with
  all SVG variants inlined side by side — the browser does the rendering, nothing to install.
- Small-size check: place a 64×64 copy of the silhouette in the sheet (`width="64"`), don't
  just claim it scales.
- Grayscale: either duplicate the SVG with gray fills, or wrap a copy in
  `<filter><feColorMatrix type="saturate" values="0"/></filter>` — the explicit duplicate is
  more portable.
- If a raster copy is explicitly needed (e.g., the user wants a PNG), convert with a locally
  available tool (`cairosvg`, `resvg`, or headless Chromium); otherwise SVG + HTML is enough.

## Reporting

In the design sheet's 驗證結果 section, show each test's artifact with a one-line verdict:
pass / marginal / fail-then-revised. If a test forced a revision, show the before and after in
one row — this is the most persuasive part of the whole deliverable, do not hide it.
