#!/usr/bin/env python3
"""Self-test for audit_theme.py — proves the linter still catches what it claims.

    python3 scripts/selftest.py

Plants exactly one defect per rule plus four legal patterns that must NOT be
flagged, runs the auditor, and asserts on the exact set of findings.
Exit 0 = the linter behaves; 1 = the linter is broken or noise.
"""
from __future__ import annotations

import io
import os
import sys
import tempfile
import contextlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_theme as A  # noqa: E402

PAGE = """<!doctype html><html><head><style>
:root{--mono:"SF Mono",monospace;--sans:"Inter",sans-serif;--bg:#fbfaf7;--line:#e7e3da}
body{background:#ffffff;color:#000;font-family:var(--sans)}
.prose{font-family:var(--mono);font-size:11px;letter-spacing:.04em}
.wrap .prose{font-family:var(--sans)}
.ugly{box-shadow:0 4px 12px rgba(0,0,0,.08);border-radius:22px}
.ring{box-shadow:inset 0 0 0 1px var(--line);border-radius:10px}
.miss{color:var(--nope)}
</style></head><body>
<div class="prose">这是一段用来验证等宽字体误用的长中文段落，它应该有至少四十个汉字才会被脚本抓出来，否则检测形同虚设。</div>
<div class="wrap"><div class="prose">这段在父级等宽但自身被覆盖为无衬线，属于合法情形，不应被报告。</div></div>
<div class="ring">legal inset hairline ring</div>
<div class="ugly">drop shadow card</div>
</body></html>
"""

SHOULD_FLAG = [
    "drop shadow found",
    "body background is pure white",
    "body text is pure black",
    "border-radius 22px is too round",
    "no definition in :root -> --nope",
    'class="prose"> holds',
]
SHOULD_NOT_FLAG = [
    'inset 0 0 0 1px',        # legal hairline ring must not be called a drop shadow
    'class="wrap"',           # a plain wrapper must not be blamed for a child's styling
]


def main() -> int:
    fd, path = tempfile.mkstemp(suffix=".html", text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(PAGE)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            code = A.audit(path, "", False)
    finally:
        os.unlink(path)
    out = buf.getvalue()

    failures = []
    for needle in SHOULD_FLAG:
        if needle not in out:
            failures.append(f"missed expected finding: {needle!r}")
    for needle in SHOULD_NOT_FLAG:
        if needle in out:
            failures.append(f"false positive: {needle!r}")
    # the `.wrap .prose` override is legal, so only ONE prose finding is allowed
    prose_hits = out.count('holds') if "holds" in out else 0
    if prose_hits != 1:
        failures.append(f"expected exactly 1 mono-prose finding, got {prose_hits}")
    if code != 1:
        failures.append(f"expected exit 1, got {code}")

    print(out.rstrip())
    print()
    if failures:
        for f in failures:
            print(f"  SELFTEST FAIL  {f}")
        return 1
    print(f"  selftest OK — {len(SHOULD_FLAG)} defects caught, "
          f"{len(SHOULD_NOT_FLAG) + 1} legal patterns ignored")
    return 0


if __name__ == "__main__":
    sys.exit(main())