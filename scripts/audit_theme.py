#!/usr/bin/env python3
"""Lint a single-file HTML page against the codex-light-doc-ui rules.

Usage (needs Python 3; on Windows `python` may still be 2.7 -> use `python3`):
    python3 scripts/audit_theme.py <page.html> [--css extra.css] [--verbose]

Exit code 0 = clean, 1 = at least one ERROR, 2 = bad usage.

Checks, in order:
  1. flatness        no drop shadows (only `none` and 1px inset hairline rings)
  2. ground          no pure-white page background, no pure-black body text
  3. geometry        border-radius only 0/2/3/4/6/10/999 (>12px is consumer-app)
  4. type budget     warns above 9 distinct literal font sizes
  5. tokens          every var(--x) resolves to a declaration
  6. mono prose      long CJK text that resolves (cascade-aware) to the mono stack
  7. contrast        WCAG AA on the token triads
  8. structure       balanced div/section/table/span/p

No third-party dependencies. Run it before delivery and after any restyle round
so drift is caught mechanically instead of by eye.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}
PSEUDO = re.compile(r"::?[a-zA-Z-]+(?:\([^)]*\))?")
AT_BLOCK = re.compile(r"@(?:media|supports|container|layer|print)\b[^{]*\{")

ALLOWED_RADII = {"0", "2px", "3px", "4px", "6px", "10px", "999px", "50%"}
MONO_PROSE_LIMIT = 40          # CJK chars in a mono block that count as "prose"


# --------------------------------------------------------------------------- css

def strip_at_blocks(css: str) -> str:
    """Drop @media/@supports/@print blocks so flat rule parsing stays sane."""
    out, i = [], 0
    while True:
        m = AT_BLOCK.search(css, i)
        if not m:
            out.append(css[i:])
            break
        out.append(css[i:m.start()])
        depth, j = 0, m.end() - 1
        while j < len(css):
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        i = j + 1
    return "".join(out)


def parse_rules(css: str):
    """-> list of (chain, decls, order); chain = list of class-tuples, subject last."""
    rules = []
    for order, (sel, body) in enumerate(re.findall(r"([^{}]+)\{([^{}]*)\}", css)):
        if sel.strip().startswith("@"):
            continue
        for part in sel.split(","):
            part = PSEUDO.sub("", part.strip())
            compounds = [c for c in re.split(r"\s+|[>+~]", part) if c]
            classes = [tuple(re.findall(r"\.([A-Za-z0-9_-]+)", c)) for c in compounds]
            if any(classes):
                rules.append((classes, body, order))
    return rules


def decl(body: str, prop: str) -> str | None:
    m = re.search(rf"(?:^|[;{{\s]){prop}\s*:\s*([^;}}]+)", body)
    return m.group(1).strip() if m else None


def shadow_ok(value: str) -> bool:
    """Only `none` and inset hairline rings (0 blur, <=1px spread) are legal."""
    v = value.strip().lower()
    if v in {"none", "0", "unset", "initial"}:
        return True
    for layer in v.split(","):
        if "inset" not in layer:
            return False
        nums = [float(x) for x in re.findall(r"(-?\d+(?:\.\d+)?)(?:px)?(?![%\d.])", layer)]
        if len(nums) < 3:
            return False
        blur = nums[2]
        spread = nums[3] if len(nums) > 3 else 0.0
        if blur != 0 or spread > 1.0:
            return False
    return True


# --------------------------------------------------------------------------- dom

class Dom(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.nodes: list[dict] = []
        self.stack: list[int] = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        classes = set()
        for k, v in attrs:
            if k == "class" and v:
                classes = set(v.split())
        self.nodes.append({
            "tag": tag,
            "classes": classes,
            "parent": self.stack[-1] if self.stack else None,
            "anc": [self.nodes[i]["classes"] for i in self.stack],
            "text": [],
        })
        self.stack.append(len(self.nodes) - 1)

    def handle_startendtag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        for depth in range(len(self.stack) - 1, -1, -1):
            if self.nodes[self.stack[depth]]["tag"] == tag:
                del self.stack[depth:]
                return

    def handle_data(self, data):
        for idx in self.stack:
            self.nodes[idx]["text"].append(data)


def selector_matches(chain, node) -> bool:
    if not set(chain[-1]) <= node["classes"]:
        return False
    anc = node["anc"]
    idx = len(anc) - 1
    for compound in reversed(chain[:-1]):
        found = False
        while idx >= 0:
            if set(compound) <= anc[idx]:
                found = True
                idx -= 1
                break
            idx -= 1
        if not found:
            return False
    return True


def resolve(nodes: list[dict], rules, prop: str) -> list[str | None]:
    """Cascade-aware property resolution: inheritance + specificity + order."""
    own: list[tuple[tuple[int, int], str] | None] = [None] * len(nodes)
    for i, node in enumerate(nodes):
        if not node["classes"]:
            continue
        best = None
        for chain, body, order in rules:
            value = decl(body, prop)
            if value is None:
                continue
            if not selector_matches(chain, node):
                continue
            key = (sum(len(c) for c in chain), order)
            if best is None or key > best[0]:
                best = (key, value)
        own[i] = best
    resolved: list[str | None] = [None] * len(nodes)
    for i in range(len(nodes)):
        if own[i]:
            resolved[i] = own[i][1]
            continue
        parent = nodes[i]["parent"]
        if parent is not None:
            resolved[i] = resolved[parent]
    return resolved


# --------------------------------------------------------------------------- audit

def contrast(a: str, b: str) -> float:
    def lum(h: str) -> float:
        h = h.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        ch = []
        for k in (0, 2, 4):
            v = int(h[k:k + 2], 16) / 255.0
            ch.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
        return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def audit(path: str, extra_css: str, verbose: bool) -> int:
    html = open(path, encoding="utf-8").read()
    inline = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))
    # strip CSS comments first: a `/* ... */` before a rule would otherwise be
    # swallowed into the selector text (and fake specificity / fake font sizes)
    raw = re.sub(r"/\*.*?\*/", "", inline + "\n" + extra_css, flags=re.S)
    css = strip_at_blocks(raw)
    rules = parse_rules(css)

    errors: list[str] = []
    warns: list[str] = []

    # 1 flatness
    for body in (b for _, b, _ in rules):
        sh = decl(body, "box-shadow")
        if sh and not shadow_ok(sh):
            errors.append(f"drop shadow found (system is flat): box-shadow:{sh}")

    # 2 ground
    body_decl = next((b for c, b, _ in rules if c == [()] or "body" in str(c)), None)
    m = re.search(r"(?:^|[;{\s])body\s*\{([^}]*)\}", css)
    if m:
        b = m.group(1)
        bg = decl(b, "background") or decl(b, "background-color")
        if bg and bg.lower() in {"#fff", "#ffffff", "white"}:
            errors.append("body background is pure white; use --bg (#fbfaf7)")
        fg = decl(b, "color")
        if fg and fg.lower() in {"#000", "#000000", "black"}:
            errors.append("body text is pure black; use --ink (#191814)")

    # 3 geometry
    for body in (b for _, b, _ in rules):
        r = decl(body, "border-radius")
        if not r:
            continue
        for value in r.split():
            px = re.match(r"^(\d+(?:\.\d+)?)px$", value)
            if px and float(px.group(1)) > 12 and value not in ALLOWED_RADII:
                errors.append(f"border-radius {value} is too round; allowed 4/6/10/999")

    # 4 type budget
    sizes = Counter()
    for body in (b for _, b, _ in rules):
        s = decl(body, "font-size")
        if s:
            sizes[s] += 1
    literal = [s for s in sizes if re.match(r"^\d+(?:\.\d+)?(?:px|rem|em)$", s)]
    if len(literal) > 9:
        warns.append(f"{len(literal)} distinct literal font sizes; the system allows ~7")
    if verbose:
        shown = sorted(literal, key=lambda s: float(re.sub(r"[^\d.]", "", s) or 0))
        print("  font sizes:", ", ".join(shown))

    # 5 tokens resolve
    defined = set(re.findall(r"(?:^|[;{\s])(--[A-Za-z0-9_-]+)\s*:", css, re.M))
    used = set(re.findall(r"var\(\s*(--[A-Za-z0-9_-]+)\s*\)", css))
    missing = sorted(used - defined)
    if missing:
        errors.append("var() with no definition in :root -> " + ", ".join(missing))

    # 6 mono prose (cascade-aware, so overrides are respected)
    dom = Dom()
    dom.feed(html)
    fonts = resolve(dom.nodes, rules, "font-family")
    hits = 0
    for node, family in zip(dom.nodes, fonts):
        if not family or ("--mono" not in family and "monospace" not in family):
            continue
        text = re.sub(r"\s+", " ", "".join(node["text"])).strip()
        cjk = len(CJK.findall(text))
        if cjk < MONO_PROSE_LIMIT:
            continue
        hits += 1
        if hits <= 6:
            owner = ",".join(sorted(node["classes"])) or node["tag"]
            errors.append(f"<{node['tag']} class=\"{owner}\"> holds {cjk} CJK chars in mono; "
                          f"prose must be --sans 13.5-14.5px (excerpt: {text[:26]}...)")
    if hits > 6:
        errors.append(f"...and {hits - 6} more mono prose blocks")

    # 7 contrast on the token triads
    pairs = [("#191814", "#fbfaf7", 4.5, "ink"),
             ("#45423b", "#fbfaf7", 4.5, "ink-2"),
             ("#6f6a60", "#fbfaf7", 4.5, "ink-3"),
             ("#938d82", "#fbfaf7", 3.0, "ink-4 (decorative only)"),
             ("#4f46a8", "#f5f4fc", 4.5, "L"),
             ("#156d78", "#f1f7f8", 4.5, "V"),
             ("#8d6316", "#faf5e9", 4.5, "A"),
             ("#2c6b4d", "#f1f6f2", 4.5, "ok"),
             ("#a2402f", "#fbf3f1", 4.5, "bad")]
    for fg, bg, floor, name in pairs:
        # only grade tokens this page actually declares, otherwise every page
        # gets a warning about a colour it never uses
        if fg.lower() not in css.lower():
            continue
        ratio = contrast(fg, bg)
        if ratio < floor:
            errors.append(f"contrast {name} {fg} on {bg} = {ratio:.2f} < {floor}")
        elif ratio < 4.5:
            warns.append(f"contrast {name} {fg} on {bg} = {ratio:.2f} — below AA 4.5; "
                         f"use --ink-3 (#6f6a60, 5.15) for text that carries information")
        elif verbose:
            print(f"  contrast {name} {fg} on {bg} = {ratio:.2f}")

    # 8 structure
    for tag in ("div", "section", "table", "span", "p"):
        opens = len(re.findall(rf"<{tag}\b", html, re.I))
        closes = len(re.findall(rf"</{tag}>", html, re.I))
        if opens != closes:
            errors.append(f"unbalanced <{tag}>: {opens} open / {closes} close")

    print(f"\n=== {path} ===")
    print(f"  dom nodes: {len(dom.nodes)}   css rules: {len(rules)}")
    for w in warns:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    if not errors:
        print("  OK - no violations of codex-light-doc-ui")
    return 1 if errors else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--css", default="", help="extra stylesheet to lint alongside the inline <style>")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    if sys.version_info < (3, 7):
        print("needs Python 3.7+; on Windows use `python3`", file=sys.stderr)
        return 2
    extra = open(a.css, encoding="utf-8").read() if a.css else ""
    return audit(a.page, extra, a.verbose)


if __name__ == "__main__":
    sys.exit(main())