# codex-theme-html-skill

An agent **skill** for building single-file HTML documents that read like Codex / OpenAI-docs:
light warm-white ground, 1px hairline structure, zero drop shadows, generous section rhythm,
four-step grey ink scale, restrained low-saturation semantic accents, one 1080px column.

No build step, no dependencies, no framework. One `.html` file in, one `.html` file out —
plus a linter that checks the aesthetic mechanically instead of by eye.

```
codex-light-doc-ui/
├── SKILL.md                 the skill itself: rules, tokens, checklist, common failures
├── reference/tokens.css     copy-paste `:root` block + base element styles
└── scripts/
    ├── audit_theme.py       linter: 8 structural checks, exit 1 on ERROR
    └── selftest.py          plants one defect per rule, asserts the linter catches all of them
```

---

## Install as a skill

Drop the folder where your agent host looks for skills:

```bash
# Claude Code / agents that read ~/.claude/skills
git clone https://github.com/2441630833/codex-theme-html-skill.git \
  ~/.claude/skills/codex-light-doc-ui

# or project-local
git clone https://github.com/2441630833/codex-theme-html-skill.git \
  <project>/.agents/skills/auto/codex-light-doc-ui
```

No install script, no runtime, nothing to compile. The agent reads `SKILL.md` when the task
matches its `description`, and copies values out of `reference/tokens.css`.

## Use it on a page

```bash
python3 scripts/audit_theme.py page.html                 # lint the inline <style>
python3 scripts/audit_theme.py page.html --css brand.css # also lint an external sheet
python3 scripts/audit_theme.py page.html --verbose       # show passing checks too
python3 scripts/selftest.py                              # prove the linter still works
```

Exit codes: `0` clean, `1` at least one ERROR, `2` bad usage.
On Windows `python` may still be 2.7 — use `python3` or `py -3`.

What it checks:

| # | Check | Fails when |
|---|-------|-----------|
| 1 | flatness | any `box-shadow` other than `none` / 1px inset hairline ring |
| 2 | ground | page background is pure `#fff`, or body text is pure `#000` |
| 3 | geometry | `border-radius` outside 0/2/3/4/6/10/999 (>12px reads consumer-app) |
| 4 | type budget | more than 9 distinct literal font sizes (warn) |
| 5 | tokens | a `var(--x)` that resolves to nothing |
| 6 | mono prose | long CJK text whose cascade-resolved font is the mono stack |
| 7 | contrast | semantic token triads below WCAG AA |
| 8 | structure | unbalanced `div/section/table/span/p` |

---

## The recipe, condensed

| Layer | Value | Why |
|---|---|---|
| Ground | `--bg:#fbfaf7` | pure white glares; warm white reads as paper |
| Ink | `--ink:#191814`, then `--ink-2/3/4` | four grey steps sort rank by luminance, not by jumping sizes |
| Structure | `--line:#e7e3da` hairline, 1px | hierarchy from rules, never from `box-shadow` |
| Type | body 15px / line-height 1.72; scale 15 / 13.5 / 12.5 / 11 | small body, loose leading |
| Column | `max-width:1080px`, `padding:0 40px` | single narrow column; no full-bleed text |
| Rhythm | `section{padding:72px 0 8px}` + `border-top:1px` | one spacing unit for the whole document |
| Corners | `--radius:10px`, `--radius-sm:6px` | near-square, engineering feel |
| Accents | `--L:#4f46a8 --V:#156d78 --A:#8d6316` + `ok/warn/bad` triads | colour only carries meaning, always `fg + bg + line` |
| Nav | `rgba(251,250,247,.86)` + `backdrop-filter:blur(14px)` | sticky, still the same ground |
| Print | dark→white, hide nav/tabs, tables 9pt, `break-inside:avoid` | Ctrl+P gives a usable PDF |

Three non-obvious rules the linter enforces because they caused real regressions:

1. **Never set mono on Chinese prose.** A long CJK sentence in a monospace stack is the single
   most common "why is this text crammed together" bug. Micro-labels only.
2. **`letter-spacing` must stay ≥ 0 for CJK.** Negative tracking on Chinese is unreadable.
3. **Cap the measure at ~74ch** for body copy; on wide grids, keep the cap and let the column shrink.

## 中文速用

- 安装：把整个目录放到 `~/.claude/skills/codex-light-doc-ui`
- 用法：让智能体“用 codex-light-doc-ui 风格做这页”，或手动抄 `reference/tokens.css` 的 `:root`
- 交付前必跑：`python3 scripts/audit_theme.py 你的页面.html`，必须 exit 0
- 回归自检：`python3 scripts/selftest.py`，六条规则植入缺陷必须全部被捕获
- 三条最容易犯的错：等宽字体用在中文长句、纯白底、`box-shadow` 做层级

## Provenance

Distilled from a ~997-line production stylesheet that was applied over two live engineering
documents (867 and 773 DOM nodes; 262 and 246 CSS rules) and passed the linter clean.
Every hex, size and spacing value here was copied from that sheet, not invented.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2025 2441630833.

Use it, fork it, ship it in commercial work; keep the copyright notice. No warranty.