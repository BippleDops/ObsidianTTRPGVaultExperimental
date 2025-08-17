#!/usr/bin/env python3

import os, re, sys, json

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'
REPORTS_DIR = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

SKIP_RE = re.compile(r"/(\.git|08_Archive|13_Performance|04_Resources/Assets/Generated)(/|$)")

def walk_md():
    files = []
    for dp, dn, fn in os.walk(ROOT):
        rel_dp = os.path.relpath(dp, ROOT)
        if SKIP_RE.search('/'+rel_dp.replace('\\','/')+'/'):
            continue
        for n in fn:
            if n.lower().endswith('.md'):
                files.append(os.path.join(dp, n))
    return files

SECTIONS = ['Player-Facing Summary','Lore Details','Adventure Hooks','DM Notes','Cross-References']

def section_present(txt, title):
    return re.search(rf"^##\s+{re.escape(title)}(\n|$)", txt, re.M) is not None

def body_length(txt):
    # strip frontmatter
    m = re.match(r"^---\n[\s\S]*?\n---\n", txt)
    if m:
        txt = txt[m.end():]
    # rough word count
    words = re.findall(r"[A-Za-z0-9']+", txt)
    return len(words)

def main():
    files = walk_md()
    audits = []
    for p in files:
        try:
            with open(p,'r',encoding='utf-8') as f:
                txt = f.read()
        except Exception:
            continue
        present = { s: section_present(txt, s) for s in SECTIONS }
        wc = body_length(txt)
        score = sum(1 for v in present.values() if v) + (1 if wc >= 150 else 0)
        audits.append({
            'file': os.path.relpath(p, ROOT),
            'sections': present,
            'word_count': wc,
            'score': score
        })
    audits.sort(key=lambda x: x['score'])
    report = os.path.join(REPORTS_DIR, 'content_depth_audit.json')
    with open(report,'w',encoding='utf-8') as f:
        json.dump({'audits': audits, 'dry_run': DRY_RUN}, f, indent=2)
    print(f"content depth audited {len(audits)} files; report: {os.path.relpath(report, ROOT)}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os
import re
from typing import List, Tuple
from common import (
    ROOT_DIR,
    list_markdown_files,
    read_file,
    write_file,
    backup_file,
    split_frontmatter,
    build_frontmatter,
    ensure_section,
    write_report,
    DRY_RUN,
)

MAJOR_THRESHOLD = 300
MINOR_THRESHOLD = 150

REQUIRED_SECTIONS_BY_TYPE = {
    "NPC": ["Overview", "Appearance", "Personality", "Goals", "Relationships", "Hooks"],
    "Location": ["Overview", "History", "Layout", "Notables", "Threats", "Hooks"],
}


def count_lines(text: str) -> int:
    return len(text.splitlines())


def ensure_sections_for_type(body: str, etype: str) -> Tuple[str, int]:
    added = 0
    sections = REQUIRED_SECTIONS_BY_TYPE.get(etype, [])
    for s in sections:
        body2, created = ensure_section(body, s)
        if created:
            body = body2 + "\nTODO\n"
            added += 1
    return body, added


def main():
    files = list_markdown_files(ROOT_DIR)
    queued: List[Tuple[str, int]] = []
    scaffolds_added = 0

    for path in files:
        md = read_file(path)
        fm, body = split_frontmatter(md)
        etype = (fm.get("type") or "").strip()
        total_lines = count_lines(md)
        if etype in ("NPC", "Location"):
            # Queue thin files for expansion
            threshold = MAJOR_THRESHOLD if "major" in (" ".join(fm.get("tags", []))).lower() else MINOR_THRESHOLD
            if total_lines < threshold:
                queued.append((os.path.relpath(path, ROOT_DIR), total_lines))
                # Auto-insert scaffolds where safe
                new_body, added = ensure_sections_for_type(body, etype)
                if added > 0 and not DRY_RUN:
                    scaffolds_added += 1
                    backup_file(path)
                    write_file(path, build_frontmatter(fm) + "\n" + new_body)

    lines: List[str] = [
        "VAULT IMPROVEMENT PHASE 5: Content Depth & Hooks Auditor",
        "",
        f"Files scanned: {len(files)}",
        f"Thin files queued for expansion: {len(queued)}",
        f"Files where scaffolds were inserted: {scaffolds_added}",
        "",
        "Queued (first 200):",
    ]
    for rel, n in queued[:200]:
        lines.append(f"- {rel} ({n} lines)")
    if len(queued) > 200:
        lines.append(f"... and {len(queued) - 200} more")

    write_report("depth_audit.md", "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()