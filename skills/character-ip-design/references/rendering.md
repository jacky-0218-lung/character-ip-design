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
4. **Per-tool parameter blocks**:
   - Midjourney: `--oref <turnaround URL>` (one image) + `--ow` (default 100, keep <400),
     `--sref` for style, fixed seed; restate style at prompt start AND end; note oref is
     incompatible with Fast/Draft modes.
   - Gemini/Nano-banana-class: attach up to ~14 reference images; phrase as "Using the
     attached sheet as [character], keep the [symbol] exactly the same, now show them …".
   - SD/Flux: LoRA route (10–20 images: front/side/back × full/portrait/close, caption
     everything EXCEPT the character — the trigger word is the thing you don't caption) or
     reference-adapter route (IPAdapter/InstantID-class) when there's no training budget.
   - Negative prompts: "off-model, inconsistent colors, different character, extra limbs,
     realistic" (adjust per style).
5. **On-model drift checklist**: silhouette matches? part-anchored hexes right? symbol
   present and unmodified? proportions (head count) right? — with the honest warning that
   fine symbol details are exactly what current models drift on; every generation gets
   checked against the flat master.

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

Verification still rules: the silhouette/extension/color tests run on the FLAT master; the
premium file must overlay-match the master's geometry (same shapes under the shading). A
gorgeous render of an unverified design is lipstick on a guess.
