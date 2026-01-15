#! /usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Optional

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

RULES_BEGIN = "<!-- BEGIN: AUTO-GENERATED RULES -->"
RULES_END = "<!-- END: AUTO-GENERATED RULES -->"
WF_BEGIN = "<!-- BEGIN: AUTO-GENERATED WORKFLOWS -->"
WF_END = "<!-- END: AUTO-GENERATED WORKFLOWS -->"
SKILLS_BEGIN = "<!-- BEGIN: AUTO-GENERATED SKILLS -->"
SKILLS_END = "<!-- END: AUTO-GENERATED SKILLS -->"


def read_text(path: Path) -> str:
    # UTF-8 BOM 対策
    return path.read_text(encoding="utf-8-sig", errors="replace")


def find_frontmatter(lines: List[str]) -> Tuple[int, int]:
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return (-1, -1)
    start = i
    j = start + 1
    while j < len(lines):
        if lines[j].strip() == "---":
            return (start, j)
        j += 1
    return (start, -1)


def parse_frontmatter(lines: List[str], start: int, end: int) -> Dict[str, str]:
    """
    必須キーだけ確実に取れればよい前提の軽量パーサ。
    - key: value
    - key: "value"
    - key: >-  (複数行) をサポート
    """
    data: Dict[str, str] = {}
    i = start + 1
    while i < end:
        raw = lines[i]
        s = raw.strip()
        i += 1
        if not s or s.startswith("#"):
            continue
        if ":" not in s:
            continue

        k, v = s.split(":", 1)
        key = k.strip()
        val = v.strip()

        # block scalar
        if val in (">-", ">", "|-", "|"):
            block_lines: List[str] = []
            # YAMLの慣例：次行以降のインデントがブロック
            while i < end:
                ln = lines[i]
                if ln.strip() == "":
                    block_lines.append("")
                    i += 1
                    continue
                if re.match(r"^\s+", ln):
                    block_lines.append(ln.strip())
                    i += 1
                else:
                    break
            # > の場合は改行をスペース結合、| の場合は改行保持…だがここでは実務上 > と同等でよい
            joined = " ".join([x for x in block_lines if x is not None]).strip()
            data[key] = joined
            continue

        # strip quotes
        val = val.strip().strip('"').strip("'")
        data[key] = val

    return data


@dataclass
class AgentDoc:
    slug: str
    description: str
    trigger: str
    file: str


def load_agent_docs(dir_path: Path, kind: str) -> List[AgentDoc]:
    docs: List[AgentDoc] = []
    
    # Skills are typically in subdirectories: skills/<skill-name>/SKILL.md
    if kind == "skills":
        patterns = ["*/SKILL.md", "*.md"]
    else:
        patterns = ["*.md"]

    files = []
    for pat in patterns:
        files.extend(dir_path.glob(pat))
    
    # Dedup files (in case *.md catches what */SKILL.md caught if structure varies)
    files = sorted(list(set(files)))

    for md in files:
        if md.name.startswith("_"): continue

        lines = read_text(md).splitlines()
        s, e = find_frontmatter(lines)
        if s == -1 or e == -1:
            # INDEX生成では「無視」ではなく、空欄で拾うと事故が残るため例外にする
            raise SystemExit(
                f"[index-gen] missing/unclosed frontmatter: {md.as_posix()}"
            )

        fm = parse_frontmatter(lines, s, e)
        
        # Skill uses 'name' instead of 'slug'
        if kind == "skills":
            slug = fm.get("name", "").strip() or fm.get("slug", "").strip()
        else:
            slug = fm.get("slug", "").strip()

        desc = fm.get("description", "").strip()
        trig = fm.get("trigger", "").strip()

        if (
            not slug
            or not desc
            or (kind == "workflows" and not trig)
            # kind="rules" requires no trigger
            # kind="skills" requires no trigger
        ):
            print(f"[index-gen] WARNING: required keys missing in {md.as_posix()} (slug/name/description/trigger). Skipping.")
            continue

        if not SLUG_RE.match(slug):
            raise SystemExit(
                f"[index-gen] invalid slug/name format in {md.as_posix()}: {slug}"
            )

        rel = md.as_posix().replace("\\", "/")
        # Make path relative to project root if possible, currently it is relative to cwd (project root)
        # dir_path passed in main is .agent/rules etc.
        # md is .agent/skills/core-components/SKILL.md
        
        docs.append(AgentDoc(slug=slug, description=desc, trigger=trig, file=rel))
    return sorted(docs, key=lambda d: d.slug)


def md_table_rules(docs: List[AgentDoc]) -> str:
    lines = ["| slug | description | file |", "| --- | --- | --- |"]
    for d in docs:
        lines.append(f"| {d.slug} | {d.description} | {d.file} |")
    return "\n".join(lines)


def md_table_workflows(docs: List[AgentDoc]) -> str:
    lines = ["| slug | description | trigger | file |", "| --- | --- | --- | --- |"]
    for d in docs:
        lines.append(f"| {d.slug} | {d.description} | {d.trigger} | {d.file} |")
    return "\n".join(lines)


def md_table_skills(docs: List[AgentDoc]) -> str:
    lines = ["| name | description | file |", "| --- | --- | --- |"]
    for d in docs:
        lines.append(f"| {d.slug} | {d.description} | {d.file} |")
    return "\n".join(lines)


def replace_block(text: str, begin: str, end: str, replacement_inner: str) -> str:
    if begin not in text or end not in text:
        # For skills, it might be missing initially, let's allow appending if missing?
        # For now, strict: must exist.
        return text 
    pre, rest = text.split(begin, 1)
    mid, post = rest.split(end, 1)
    # begin/end は残し、中身だけ差し替える
    return pre + begin + "\n" + replacement_inner + "\n" + end + post


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default=".agent/INDEX.md")
    ap.add_argument("--rules-dir", default=".agent/rules")
    ap.add_argument("--workflows-dir", default=".agent/workflows")
    ap.add_argument("--skills-dir", default=".agent/skills")
    ap.add_argument("--write", action="store_true", help="write changes to INDEX.md")
    args = ap.parse_args()

    index_path = Path(args.index)
    rules_dir = Path(args.rules_dir)
    wf_dir = Path(args.workflows_dir)
    skills_dir = Path(args.skills_dir)

    index_text = read_text(index_path)

    rules = load_agent_docs(rules_dir, "rules")
    wfs = load_agent_docs(wf_dir, "workflows")
    skills = []
    if skills_dir.exists():
        skills = load_agent_docs(skills_dir, "skills")

    rules_table = md_table_rules(rules)
    wf_table = md_table_workflows(wfs)
    skills_table = md_table_skills(skills)

    out = index_text
    
    if RULES_BEGIN in out:
        out = replace_block(out, RULES_BEGIN, RULES_END, rules_table)
    
    if WF_BEGIN in out:
        out = replace_block(out, WF_BEGIN, WF_END, wf_table)
        
    if SKILLS_BEGIN in out:
        out = replace_block(out, SKILLS_BEGIN, SKILLS_END, skills_table)
    else:
        # If skills block is missing, insert it after workflows
        if WF_END in out and skills:
            # Insert after WF_END
            # Assuming typical layout: ... WF_END ... table ... \n\n --- \n\n ## Rules ...
            pass # Creating the block in INDEX.md manually is safer via task
    
    if args.write:
        index_path.write_text(out, encoding="utf-8", newline="\n")
        print("INDEX updated.")
        return 0

    if out != index_text:
        print("[index-gen] INDEX.md is out of date. Run with --write.")
        return 1

    print("INDEX is up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
