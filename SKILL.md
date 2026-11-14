---
name: codex-light-doc-ui
description: "Use when a page must look like a Codex/OpenAI-docs style: light warm-white ground, 1px hairline structure, no shadows, generous 72px section rhythm, 4-level ink grey, restrained low-saturation semantic accents, single 1080px column. Applies to tech briefs, engineering docs, architecture explainers, and reports that should feel calm, precise and 'well-made' rather than flashy."
---

# Codex-style Light Document UI

A restrained, typographic design system for engineering documents. The look comes from
**structure and subtraction**, not decoration: hairline rules instead of shadows, a warm
off-white ground instead of pure white, a four-step grey ink scale instead of black+grey,
and one narrow column with large vertical breathing room.

Ground truth for every value below is `reference/tokens.css` in this skill, distilled from a
~997-line production stylesheet and validated against two live engineering documents.
Prefer copying from it over retyping numbers.

## When to use

Use when ANY of these is true:

- The user asks for "简洁大气" / "像 Codex 生成的 UI" / "像 OpenAI 文档" / "engineering doc look".
- The deliverable is a technical document page: tech brief, architecture note, design review, report, spec.
- The page will be printed to PDF or read for 10+ minutes — calmness beats impact.
- An existing page **already has dark/high-contrast styling** and the user says it feels "挤" (cramped), noisy, or amateur.

Do NOT use when:

- The deliverable is a landing page, pitch deck, or marketing page — that needs a hero moment, larger type, and images. This system deliberately has no focal flourish.
- The brief explicitly asks for dark mode, neon, glassmorphism, or "科技感大屏". Mixing those in destroys the look; pick one direction.
- The content is a dashboard/console with dense repeated widgets. Hairline + 72px rhythm wastes vertical space there.

## Non-negotiable principles (the whole look in 6 lines)

1. **Warm off-white ground.** `#fbfaf7`, never `#fff`. Paper, not screen.
2. **Lines, not shadows.** Structure = `1px solid var(--line)`. `box-shadow` appears zero times.
3. **Four-step ink, not two.** `#191814 / #45423b / #6f6a60 / #938d82`. Hierarchy by luminance, not by font-size jumps or underlines.
4. **Small type, generous leading.** Body 15px / 1.72. Big leading is what reads as "大气".
5. **One column, capped.** 1080px max, 40px gutters. Never full-bleed text.
6. **Colour only carries meaning.** Semantic accents are desaturated (L/V/A, ok/warn/bad) and always come as a **triad**: `fg + bg + line`. No decorative high-saturation anywhere.

## Tokens

Copy verbatim. Full block also in `reference/tokens.css`.

```css
:root{
  /* ground */
  --bg:#fbfaf7; --bg-2:#f5f3ee;
  --surface:#ffffff; --surface-2:#f8f7f3;
  /* hairlines — 3 weights only */
  --line:#e7e3da; --line-2:#d8d3c8; --line-3:#c3bdb0;
  /* ink — 4 steps only */
  --ink:#191814; --ink-2:#45423b; --ink-3:#6f6a60; --ink-4:#938d82;
  /* semantics — always fg/bg/line triads */
  --ok:#2c6b4d;   --ok-bg:#f1f6f2;   --ok-line:#cfe0d5;
  --warn:#8a6118; --warn-bg:#fbf6ea; --warn-line:#e8dcc0;
  --bad:#a2402f;  --bad-bg:#fbf3f1;  --bad-line:#e8d3ce;
  --L:#4f46a8; --L-bg:#f5f4fc;
  --V:#156d78; --V-bg:#f1f7f8;
  --A:#8d6316; --A-bg:#faf5e9;
  /* geometry — near-square */
  --radius:10px; --radius-sm:6px; --radius-pill:999px;
  --sans:"Inter","SF Pro Text",system-ui,-apple-system,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  --mono:"SF Mono","JetBrains Mono","Cascadia Mono",ui-monospace,"DejaVu Sans Mono",Consolas,monospace;
}
```

Why these exact hexes (do not "improve" them):

| Choice | Reason |
|---|---|
| `#fbfaf7` not `#fff` | Pure white at 15px causes halation on LCD; warm off-white reads as paper and makes hairline `#e7e3da` visible. |
| ink `#191814` not `#000` | Black-on-warm-white looks harsh; `#191814` keeps the warm cast so the whole page feels one material. |
| accents at ~40% saturation | `#4f46a8 / #156d78 / #8d6316` are dark enough for 4.5:1 on tinted backgrounds, so they can be used for text, not just dots. |
| 3 hairline weights | One for structure, one for interactive (`a` border), one for emphasis (table head). More than 3 = the page looks dirty. |

## Type scale

```css
body{font-size:15px; line-height:1.72;
     font-feature-settings:"ss01" 1;
     -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;}

.hero h1{margin:0 0 20px; font-size:clamp(29px,3.9vw,44px); line-height:1.18;
         font-weight:600; letter-spacing:-.028em; text-wrap:balance;}
.hero h1 em{display:block; font-size:clamp(15px,1.5vw,18px); line-height:1.6;
            font-weight:400; letter-spacing:-.005em; color:var(--ink-2);
            margin-top:14px; max-width:52ch;}
.hero h1 .hl{background:linear-gradient(transparent 62%,var(--V-bg) 62%);
             box-shadow:inset 0 -1px 0 var(--V);}      /* only "highlight" allowed */

.sec-head h2{font-size:clamp(21px,2.3vw,26px); line-height:1.36;
             font-weight:600; letter-spacing:-.02em; text-wrap:balance;}
.sec-desc,.sec-sub{font-size:14.5px; line-height:1.85; color:var(--ink-2);
                   max-width:78ch; margin:0 0 30px 42px;}  /* 42px = align under .sec-num */
h3{font-size:17px; line-height:1.45; font-weight:600; letter-spacing:-.012em; margin:0 0 10px;}
h4{font-size:15px; line-height:1.5;  font-weight:600; letter-spacing:-.012em; margin:0 0 10px;}
p{margin:0 0 14px; color:var(--ink-2);}
.sub{font-size:13.5px; color:var(--ink-3); font-family:var(--mono); line-height:1.9;}
```

Rules that matter more than the numbers:

- **Only 5 text sizes exist**: 44/26/17/15/13.5 (+11 ~ 12.5 for meta labels). Adding a 6th is the moment it turns amateur.
- Negative tracking is mandatory above 17px (`-.012em` … `-.028em`); at 15px body it must be `0` or positive.
- `text-wrap:balance` on every heading ≥ 21px. This alone removes most "ugly widow word" problems in Chinese and English.
- Measure caps: `.hero em` 52ch, `.sec-desc` 78ch, paragraph max-width ≈ 74ch. Chinese text at 15px wants ~34–40 chars per line.
- `em` is styled as **normal, ink-2** — never italics. Italic serif in CJK falls back to fake obliques.

## Layout

```css
.wrap{width:100%; max-width:1080px; margin:0 auto; padding:0 40px;}
section{padding:72px 0 8px; border-top:1px solid var(--line); scroll-margin-top:88px;}
section:first-of-type{border-top:0}
footer{margin-top:72px; border-top:1px solid var(--line);
       padding:32px 0 64px; color:var(--ink-4); font-size:12.5px; line-height:1.8;}
.hr{height:1px; background:var(--line); border:0; margin:40px 0;}
```

- **72px top padding on every section** is the single biggest contributor to the "大气" feel. Do not reduce to 40–48px to "save space"; that is what makes it look like a blog post.
- Sections are separated by a **full-width hairline**, not by gaps alone. The line tells the eye "new chapter" without a box.
- `scroll-margin-top:88px` = sticky nav (56px min-height) + breathing room. Without it, anchor jumps hide the heading under the nav.
- Nav is sticky, translucent, and quiet:
  ```css
  .nav,.topbar{position:sticky; top:0; z-index:50;
    background:rgba(251,250,247,.86);
    -webkit-backdrop-filter:saturate(180%) blur(14px); backdrop-filter:saturate(180%) blur(14px);
    border-bottom:1px solid var(--line);}
  .nav-in,.topbar-in{display:flex; align-items:center; gap:2px; flex-wrap:wrap;
    min-height:56px; padding-top:8px; padding-bottom:8px;}
  ```
  The alpha must match `--bg`'s RGB (251,250,247). If you change the ground, recompute it or the nav will show a seam.

## Component patterns

**Section head** — number is a mono micro-label, 42px column, heading starts after it:

```html
<div class="sec-head"><span class="sec-num">03</span><h2>双通路动作策略</h2></div>
<p class="sec-desc">…</p>
```

**Card** — surface + hairline, radius 10px, no shadow, padding 22–26px:

```css
.card{background:var(--surface); border:1px solid var(--line);
      border-radius:var(--radius); padding:24px 26px;}
.card + .card{margin-top:16px}
```

**Table** — the hairline treatment is what makes tables look "designed":

```css
.tbl-wrap{overflow-x:auto; border:1px solid var(--line); border-radius:var(--radius);
          background:var(--surface);}
table{width:100%; border-collapse:collapse; font-size:13.5px; line-height:1.6;}
th{font-size:11px; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
   color:var(--ink-3); text-align:left; padding:12px 14px;
   border-bottom:1px solid var(--line-2); background:var(--surface-2);}
td{padding:12px 14px; border-bottom:1px solid var(--line); color:var(--ink-2); vertical-align:top;}
tbody tr:last-child td{border-bottom:0}
td:first-child{color:var(--ink); font-weight:600}   /* first column = row label */
```

Uppercase mono `th` at 11px with `.14em` tracking is the signature detail. Keep it.

**Code** — inline vs block, both on `--surface-2`, never on pure white:

```css
code{font-family:var(--mono); font-size:12.5px; background:var(--surface-2);
     border:1px solid var(--line); border-radius:4px; padding:1.5px 5px; color:var(--ink);}
pre{background:var(--surface-2); border:1px solid var(--line); border-radius:var(--radius);
    padding:16px 18px; overflow-x:auto; font-size:12.5px; line-height:1.7;}
pre code{background:none; border:0; padding:0; font-size:inherit}
```

**Tag / badge** — mono, 11px, `.14em`, triad colours, pill radius only here:

```css
.tag{display:inline-block; font-family:var(--mono); font-size:11px; font-weight:500;
     letter-spacing:.06em; padding:2px 8px; border-radius:var(--radius-pill);
     color:var(--ink-3); background:var(--surface-2); border:1px solid var(--line);
     white-space:nowrap;}
```

Links: `a{color:var(--V); text-decoration:none; border-bottom:1px solid var(--line-2);}`
and on hover swap to `var(--V)`. Underline-as-hairline is the only "underline" the system allows.

## Anti-patterns — these are exactly what makes it look AI-generated

| Don't | Why it breaks this look |
|---|---|
| `box-shadow: 0 4px 12px rgba(0,0,0,.08)` on cards | The whole system is 2D. One shadow and it becomes a 2019 Bootstrap page. |
| `border-radius:20px` cards, pill-shaped everything | Near-square (6–10px) reads engineering; 20px+ reads consumer app. Pill is reserved for tags. |
| `#fff` background + `#000` text | Glare. Also makes hairlines invisible → layout collapses into floating text. |
| More than 3 grey hairline weights, or `opacity:.5` borders | Opacity borders composite differently per background and look muddy. Use solid tokens. |
| Gradient hero, glassmorphism cards, neon glow, 3-col icon grid | Explicit "AI slop" tells. If the user wants them, this skill is the wrong tool. |
| `justify` text, or centring long paragraphs | CJK + justify = rivers. This system is left-aligned throughout except `.hero`. |
| Saturated brand colour used decoratively | Colour here is a *label*, not a mood. |
| Compressing sections to fit more content | Content that does not fit should be cut, not squeezed. 72px is the budget. |
| **Long CJK sentences set in `--mono` at 11–12px** | The #1 real-world defect seen with this theme: micro-label typography applied to full paragraphs. Chinese in a mono stack falls back to a mismatched face, gains fake tracking, and reads as a crammed wall. `.job`, `.desc`, `.note` style blocks must be `--sans` at 13.5–14.5px / 1.85+. |
| Negative `letter-spacing` below 15px | Destroys CJK legibility immediately. |

## Print / PDF

```css
@media print{
  body{background:#fff; color:#000; font-size:10.5pt}
  .nav,.topbar,.tabs{display:none}          /* nav and tab bars are meaningless on paper */
  .card,.tbl-wrap,pre,table{break-inside:avoid}
  h2,h3,h4{break-after:avoid}               /* never leave a heading alone at page bottom */
  a{color:inherit; border-bottom:0}
  section{padding:18pt 0 0; border-top:1px solid #ddd}
}
```

Also set `color-scheme: light` on `:root` so form controls and scrollbars match, and add
`@media (prefers-reduced-motion: reduce)` to kill any reveal animation.

## Dark mode (derived, not from the reference file)

Only add if asked. Invert the ground and lighten the ink; keep the same triads, do **not**
just flip values:

```css
@media (prefers-color-scheme: dark){
  :root{--bg:#131210; --bg-2:#191816; --surface:#1c1b18; --surface-2:#22211d;
        --line:#2e2c27; --line-2:#3b3832; --line-3:#4a463e;
        --ink:#f2efe8; --ink-2:#c9c4b8; --ink-3:#9c978b; --ink-4:#726d63;
        --L:#a99cf7; --V:#63c3cd; --A:#d9a95a;
        --ok:#6fbf93; --warn:#d9a44e; --bad:#e08170;}
  .nav,.topbar{background:rgba(19,18,16,.86)}
}
```

Always re-measure contrast after this — dark accents need ≥4.5:1 on `--bg`, which usually
means lightening to ~70% lightness, not reusing the light-mode hex.

## Procedure

1. **Find or build the token block first.** Never hardcode a hex in a component rule. If the page already has `:root`, *replace* it; do not append a second parallel system (two token sets = the page looks stitched).
2. **Strip ornament before adding typography.** Delete shadows, gradients, large radii, decorative icons. Most "ugly" pages become 70% better at this step alone.
3. **Apply layout**: `.wrap` 1080/40, `section` 72px + hairline, sticky translucent nav with a matching alpha.
4. **Apply the type scale exactly**, including negative tracking and `text-wrap:balance`.
5. **Convert components in this order**: headings → paragraphs → tables → code → tags → footer. Tables and code blocks carry the most perceived craft.
6. **Verify, don't eyeball.** Run the bundled auditor:

   ```bash
   python3 scripts/audit_theme.py path/to/page.html --verbose
   # extra stylesheet not inlined? add --css path/to/theme.css
   ```

   It parses the inline `<style>`, builds the real DOM (inheritance + specificity + rule order,
   so a later `.layer .job{font-family:var(--sans)}` is correctly seen as overriding an earlier
   `.layer .job{font-family:var(--mono)}`), then reports:
   `drop shadows · pure white/black · radius > 12px · dangling var() · mono-on-CJK prose · AA contrast · unbalanced tags`.
   Exit 0 = clean. `ink-4` is graded **decorative only** (3.16:1): fine for footers and section
   numbers, but any text that carries information must be `--ink-3` (5.15:1). Above 9 literal
   font sizes it only warns — that number is usually accumulated technical debt from several
   restyle rounds, and clearing it means consolidating rules, not adding an override.

   Then confirm the page opens offline and prints to one PDF with no heading orphaned at a page break.

   Caveats: it does not evaluate media-query conditions, inline `style=` attributes, or `#id`
   selectors. Treat it as a fast regression net, not a browser.

   <!-- regression corpus: the two pages this skill was extracted from — 867 and 773 DOM
        nodes, 262 and 246 rules — both pass clean. A synthetic page with one planted defect
        per rule must fail on all six; if it ever passes, the linter is broken, not the page. -->
7. **Report the delta**, not the CSS: which tokens changed, which ornament was removed, what is now unbroken at print. Keep a `*.before-*.html` backup so the user can diff.

## Verification checklist

- [ ] Zero `box-shadow` in the stylesheet (except the single `.hl` inset highlight).
- [ ] Backgrounds only from `--bg / --surface / --surface-2 / *-bg`; no `#fff` page ground, no `#000` text.
- [ ] Radii only 4 / 6 / 10 / 999.
- [ ] Distinct literal `font-size` values ≤ 9 (target 7; the auditor warns above 9).
- [ ] Every `var(--x)` used has a `--x` in `:root` (no dangling token).
- [ ] Every semantic colour used in a triad (fg + bg + line), never a bare hex.
- [ ] Long prose blocks are `--sans`; mono is confined to labels, numbers, code, and identifiers.
- [ ] Body contrast ≥ 4.5:1 against its background; label/meta ≥ 4.0:1.
- [ ] At 1440 / 1024 / 768 wide: no horizontal scroll, no nav overlap on anchor jump.
- [ ] `Ctrl+P` preview: no mid-card page break, no orphaned heading.

## Files in this skill

| Path | Role |
|---|---|
| `SKILL.md` | This document — decision rules, tokens, patterns, anti-patterns, procedure |
| `reference/tokens.css` | Copy-paste token block + base layer + components + print sheet, values already verified |
| `scripts/audit_theme.py` | Python 3 linter (no deps). Run before delivery and after every restyle round |
| `scripts/selftest.py` | Runs the linter against a page with one planted defect per rule. If this ever passes while flagging nothing, the linter is broken — run it after editing either script |

## Provenance

Extracted from a real production stylesheet (~997 lines) that was applied over two live
engineering documents. Every hex, size and spacing value above was copied
from that file, not invented. The audit script is the same one used to catch the two real
defects that the eye missed: long CJK paragraphs silently set in `--mono` (a micro-label style
applied to sentences), and print-time heading orphans.

When a page and this document disagree, trust the page only if the page looks right — then
update this file. Never keep two token systems alive "temporarily"; that is how a page ends up
with 22 distinct font sizes.