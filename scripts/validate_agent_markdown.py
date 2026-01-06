#!/usr/bin/env python3
"""
Convoy Agent Asset Validator
- Frontmatter required keys check for:
  - .agent/rules/*.md
  - .agent/workflows/*.md
- Light Markdown checks (optional but enabled by default in CI):
  - Unbalanced code fences (``` or ~~~)
  - Unclosed frontmatter block
  - (Optional) Unexpanded {{...}} placeholders scan
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8-sig", errors="replace")


def find_frontmatter_block(lines: List[str]) -> Tuple[int, int]:
    """
    Returns (start_index, end_index) for YAML frontmatter block (inclusive bounds of delimiters),
    or (-1, -1) if not found.
    """
    # Find first non-empty line
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return (-1, -1)

    start = i
    # Find closing delimiter
    j = start + 1
    while j < len(lines):
        if lines[j].strip() == "---":
            return (start, j)
        j += 1
    # Unclosed
    return (start, -1)


def parse_frontmatter(lines: List[str], start: int, end: int) -> Dict[str, str]:
    """
    Minimal YAML parser for `key: value` pairs (sufficient for our mandatory keys).
    """
    data: Dict[str, str] = {}
    for line in lines[start + 1 : end]:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if ":" not in s:
            continue
        k, v = s.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def validate_frontmatter(md_path: Path) -> List[str]:
    errors: List[str] = []
    lines = read_text(md_path).splitlines()

    fm_start, fm_end = find_frontmatter_block(lines)
    if fm_start == -1:
        errors.append(
            "missing frontmatter (must start with '---' as first non-empty line)"
        )
        return errors
    if fm_end == -1:
        errors.append("unclosed frontmatter (missing closing '---')")
        return errors

    fm = parse_frontmatter(lines, fm_start, fm_end)

    for k in ("slug", "description", "trigger"):
        if k not in fm or not fm[k].strip():
            errors.append(f"missing required key: {k}")

    slug = fm.get("slug", "").strip()
    if slug and not SLUG_RE.match(slug):
        errors.append(f"invalid slug format: '{slug}' (expected kebab-case)")

    # Soft recommendation: trigger should typically be model_decision, but do not fail if different.
    return errors


def light_markdown_checks(md_path: Path, check_placeholders: bool) -> List[str]:
    """
    Light checks: code fences balance + frontmatter closure + optional placeholders.
    """
    errors: List[str] = []
    text = read_text(md_path)
    lines = text.splitlines()

    # Frontmatter closure (if it starts with ---)
    fm_start, fm_end = find_frontmatter_block(lines)
    if fm_start != -1 and fm_end == -1:
        errors.append("unclosed frontmatter (missing closing '---')")

    # Code fence balance for ``` and ~~~
    def fence_toggle(fence: str) -> None:
        pass

    fence_stack: List[str] = []
    fence_line_re = re.compile(r"^\s*(```+|~~~+)")
    for idx, line in enumerate(lines, start=1):
        m = fence_line_re.match(line)
        if not m:
            continue
        fence = m.group(1)
        fence_type = "```" if fence.startswith("`") else "~~~"

        if not fence_stack:
            fence_stack.append(fence_type)
        else:
            # Close if same type, else treat as nested (rare but possible)
            if fence_stack[-1] == fence_type:
                fence_stack.pop()
            else:
                fence_stack.append(fence_type)

    if fence_stack:
        errors.append(f"unbalanced code fences: {fence_stack} (check ``` / ~~~ pairs)")

    # Optional: unexpanded template placeholders
    if check_placeholders:
        # Allow common mustache in templates under .agent/templates by skipping those paths if desired.
        # Here we only scan non-template paths; caller can control scan scope.
        if re.search(r"\{\{\s*[^}]+\s*\}\}", text):
            errors.append("found unexpanded {{...}} placeholder(s)")

    return errors


def iter_md_files(targets: List[Path]) -> List[Path]:
    files: List[Path] = []
    for t in targets:
        if not t.exists():
            continue
        if t.is_file() and t.suffix.lower() == ".md":
            files.append(t)
        elif t.is_dir():
            files.extend(sorted(t.rglob("*.md")))
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules-dir", type=str, default=".agent/rules")
    ap.add_argument("--workflows-dir", type=str, default=".agent/workflows")
    ap.add_argument(
        "--markdown-scan",
        nargs="*",
        default=[],
        help='Paths to scan for light markdown checks. Example: ".agent README.md docs"',
    )
    ap.add_argument(
        "--check-placeholders",
        action="store_true",
        help="Also fail if unexpanded {{...}} placeholders are found in scanned markdown.",
    )
    args = ap.parse_args()

    rules_dir = Path(args.rules_dir)
    workflows_dir = Path(args.workflows_dir)

    failed = False
    report: List[str] = []

    # Frontmatter checks (rules/workflows)
    for base in (rules_dir, workflows_dir):
        for p in sorted(base.glob("*.md")):
            errs = validate_frontmatter(p)
            if errs:
                failed = True
                for e in errs:
                    report.append(f"[frontmatter] {p.as_posix()}: {e}")

    # Light markdown checks (optional scope)
    scan_targets = [Path(x) for x in args.markdown_scan]
    md_files = iter_md_files(scan_targets)

    for p in md_files:
        # By default, do not treat {{...}} as error for templates
        placeholder_check = args.check_placeholders and (
            ".agent/templates" not in p.as_posix()
        )
        errs = light_markdown_checks(p, check_placeholders=placeholder_check)
        if errs:
            failed = True
            for e in errs:
                report.append(f"[markdown] {p.as_posix()}: {e}")

    if report:
        print("\n".join(report))

    if failed:
        print("\nValidation FAILED.")
        return 1

    print("Validation OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
