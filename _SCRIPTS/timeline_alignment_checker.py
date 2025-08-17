#!/usr/bin/env python3

import os, re, sys, json, datetime

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'
REPORTS_DIR = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

SKIP_RE = re.compile(r"/(\.git|08_Archive|13_Performance|04_Resources/Assets/Generated)(/|$)")
FM_RE = re.compile(r"^---\n([\s\S]*?)\n---\n", re.M)

DATE_RE = re.compile(r"\b(\d{4})[-/](\d{1,2})[-/](\d{1,2})\b")

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

def parse_fm_dates(txt):
    m = FM_RE.search(txt)
    if not m:
        return None, None
    fm = m.group(1)
    created = None
    updated = None
    for line in fm.splitlines():
        if line.lower().startswith('created:'):
            created = line.split(':',1)[1].strip()
        if line.lower().startswith('updated:'):
            updated = line.split(':',1)[1].strip()
    return created, updated

def main():
    files = walk_md()
    issues = []
    for p in files:
        try:
            with open(p,'r',encoding='utf-8') as f:
                txt = f.read()
        except Exception:
            continue
        created, updated = parse_fm_dates(txt)
        # find inline dates in body that are outside created/updated range
        body = re.sub(r"^---[\s\S]*?---\n", '', txt)
        body_dates = [m.group(0) for m in DATE_RE.finditer(body)]
        # Simple heuristic: if many dates exist and appear before created, warn
        warn = False
        if created:
            try:
                c = datetime.date.fromisoformat(created.strip().strip("'\""))
                for d in body_dates:
                    y,mn,dd = map(int, d.replace('/','-').split('-'))
                    dt = datetime.date(y,mn,dd)
                    if dt < c.replace(year=c.year-200):
                        # unrealistic ancient date vs created—flag
                        warn = True
                        break
            except Exception:
                pass
        if warn:
            issues.append({'file': os.path.relpath(p, ROOT), 'body_dates': body_dates[:10]})
    report = os.path.join(REPORTS_DIR, 'timeline_alignment_checker.json')
    with open(report,'w',encoding='utf-8') as f:
        json.dump({'issues': issues, 'dry_run': DRY_RUN}, f, indent=2)
    print(f"timeline alignment checked {len(files)} files; issues: {len(issues)}; report: {os.path.relpath(report, ROOT)}")

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
    write_report,
)

RELATIVE_TIME_PATTERNS = [
    re.compile(r"\b(\d{1,4})\s+years?\s+ago\b", re.IGNORECASE),
    re.compile(r"\bYear\s+(\d{1,4})\b", re.IGNORECASE),
]

REFERENCE_EVENTS = {
    "Great Crystallization": 500,  # approx years ago
    "The Drowning": None,  # Uses AS/BS; manual alignment required
}


def main():
    files = list_markdown_files(ROOT_DIR)
    flagged: List[Tuple[str, str]] = []

    for path in files:
        md = read_file(path)
        for pat in RELATIVE_TIME_PATTERNS:
            for m in pat.finditer(md):
                snippet = md[max(0, m.start()-40): m.end()+40].replace("\n", " ")
                flagged.append((os.path.relpath(path, ROOT_DIR), snippet))

    lines: List[str] = [
        "VAULT IMPROVEMENT PHASE 5: Timeline Alignment Checker",
        "",
        f"Files scanned: {len(files)}",
        f"Relative time references flagged: {len(flagged)}",
        "",
        "Examples (first 200):",
    ]
    for rel, snip in flagged[:200]:
        lines.append(f"- {rel}: ...{snip}...")
    if len(flagged) > 200:
        lines.append(f"... and {len(flagged) - 200} more")

    write_report("timeline_conflicts.md", "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()