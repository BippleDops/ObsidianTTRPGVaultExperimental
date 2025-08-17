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

def canonicalize(name: str) -> str:
    # Normalize Unicode, collapse spaces, title case except stop-words
    base = name.strip()
    base = re.sub(r"\s+", ' ', base)
    # Leave punctuation like quotes intact
    titled = ' '.join([w.capitalize() if w.lower() not in {'of','the','and','or','a','an','in','on'} else w.lower() for w in re.split(r"(\s+)", base)])
    return titled

def main():
    files = walk_md()
    renames = []
    for p in files:
        dirn = os.path.dirname(p)
        base = os.path.basename(p)
        name = base[:-3]
        canon = canonicalize(name)
        if canon != name:
            newp = os.path.join(dirn, canon + '.md')
            if not DRY_RUN:
                os.makedirs(dirn, exist_ok=True)
                # avoid collision
                if not os.path.exists(newp):
                    os.rename(p, newp)
                    renames.append((os.path.relpath(p, ROOT), os.path.relpath(newp, ROOT)))
            else:
                renames.append((os.path.relpath(p, ROOT), os.path.relpath(newp, ROOT)))
    report = os.path.join(REPORTS_DIR, 'canonical_names.json')
    with open(report,'w',encoding:'utf-8') as f:
        json.dump({'renames': renames, 'dry_run': DRY_RUN}, f, indent=2)
    print(f"canonicalized {len(renames)} filenames; report: {os.path.relpath(report, ROOT)}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os
import re
from typing import Dict, List
from common import (
    ROOT_DIR,
    DATA_DIR,
    list_markdown_files,
    read_file,
    write_file,
    backup_file,
    split_frontmatter,
    build_frontmatter,
    save_json,
    write_report,
    DRY_RUN,
)


def canonical_name(title: str) -> str:
    # Canonicalize by using the case and spacing of the existing filename
    # Also strip extra spaces
    return re.sub(r"\s+", " ", title).strip()


def main():
    files = list_markdown_files(ROOT_DIR)
    mapping: Dict[str, Dict[str, List[str]]] = {}

    # Build initial canonical names from filenames
    for path in files:
        title = os.path.splitext(os.path.basename(path))[0]
        can = canonical_name(title)
        mapping[title] = {"canonical": can, "aliases": []}

    # Collect explicit aliases from frontmatter and unify
    alias_updates = 0
    for path in files:
        md = read_file(path)
        fm, body = split_frontmatter(md)
        title = os.path.splitext(os.path.basename(path))[0]
        aliases = fm.get("aliases") or []
        if isinstance(aliases, list):
            # normalize aliases
            norm_aliases = []
            for a in aliases:
                a2 = canonical_name(str(a))
                if a2 and a2 != title:
                    norm_aliases.append(a2)
            if norm_aliases != aliases:
                fm["aliases"] = norm_aliases
                if not DRY_RUN:
                    backup_file(path)
                    write_file(path, build_frontmatter(fm) + "\n" + body)
                alias_updates += 1
            if title in mapping:
                mapping[title]["aliases"] = norm_aliases

    # Save mapping
    save_json(os.path.join(DATA_DIR, "canonical-names.json"), mapping)

    # Report
    lines: List[str] = [
        "VAULT IMPROVEMENT PHASE 5: Name & Alias Canonicalizer",
        "",
        f"Files scanned: {len(files)}",
        f"Files updated (alias normalization): {alias_updates}",
        f"Canonical names recorded: {len(mapping)}",
    ]
    write_report("canonical_names.md", "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()