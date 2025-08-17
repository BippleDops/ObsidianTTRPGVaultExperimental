#!/usr/bin/env python3

import os, re, sys, json

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'
REPORTS_DIR = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

SKIP_RE = re.compile(r"/(\.git|08_Archive|13_Performance|04_Resources/Assets/Generated)(/|$)")
FM_RE = re.compile(r"^---\n([\s\S]*?)\n---\n", re.M)

CANON = {
    'realm': ['aquabyssos','aethermoor','void','mixed'],
    'type': ['People','Places','Groups','Lore','Quest','Mechanic','Item','Vehicle','Encounter'],
    'status': ['draft','stub','final'],
}

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

def parse_fm(txt):
    m = FM_RE.search(txt)
    if not m:
        return None, None, None
    fm = m.group(1)
    tags = []
    relm = None
    typ = None
    for line in fm.splitlines():
        if line.strip().startswith('tags:'):
            # collect subsequent dash lines until next key
            pass
    # simple parse of inline arrays and dashes
    # tags:
    block = []
    capture = False
    for line in fm.splitlines():
        if re.match(r"^\s*tags\s*:\s*$", line):
            capture = True
            continue
        if capture:
            if re.match(r"^\s*-\s*(.+)$", line):
                block.append(re.match(r"^\s*-\s*(.+)$", line).group(1).strip())
                continue
            if ':' in line:
                capture = False
        m_inline = re.match(r"^\s*tags\s*:\s*\[(.*)\]\s*$", line)
        if m_inline:
            items = [x.strip() for x in m_inline.group(1).split(',') if x.strip()]
            block.extend(items)
    tags = [t.strip().strip("'\"") for t in block]
    # try realm/type keys
    for line in fm.splitlines():
        if re.match(r"^\s*realm\s*:\s*(.+)$", line):
            relm = re.match(r"^\s*realm\s*:\s*(.+)$", line).group(1).strip().strip("'\"")
        if re.match(r"^\s*type\s*:\s*(.+)$", line):
            typ = re.match(r"^\s*type\s*:\s*(.+)$", line).group(1).strip().strip("'\"")
    return fm, tags, {'realm': relm, 'type': typ}

def main():
    files = walk_md()
    problems = []
    fixed = []
    for p in files:
        try:
            with open(p,'r',encoding='utf-8') as f:
                txt = f.read()
        except Exception:
            continue
        fm, tags, keys = parse_fm(txt)
        if fm is None:
            continue
        bad_tags = [t for t in (tags or []) if ' ' in t or t.lower()!=t]
        bad_realm = keys.get('realm') and keys['realm'] not in CANON['realm']
        bad_type = keys.get('type') and keys['type'] not in CANON['type']
        if bad_tags or bad_realm or bad_type:
            problems.append({'file': os.path.relpath(p, ROOT), 'bad_tags': bad_tags, 'bad_realm': bool(bad_realm), 'bad_type': bool(bad_type)})
            if not DRY_RUN:
                new = txt
                if bad_realm:
                    new = new.replace(f"realm: {keys['realm']}", f"realm: aquabyssos")
                if bad_type:
                    new = new.replace(f"type: {keys['type']}", f"type: Lore")
                # normalize tags to kebab-case lower
                if tags:
                    kebab = [re.sub(r"[^a-z0-9]+","-", t.lower()).strip('-') for t in tags]
                    # replace tags block crudely
                    new = re.sub(r"^tags:\n([\s\S]*?)^(\w|---)", lambda m: 'tags:\n' + ''.join(f"- {t}\n" for t in kebab) + m.group(2), new, flags=re.M)
                with open(p,'w',encoding='utf-8') as f:
                    f.write(new)
                fixed.append(os.path.relpath(p, ROOT))
    report = os.path.join(REPORTS_DIR, 'tag_taxonomy.json')
    with open(report,'w',encoding:'utf-8') as f:
        json.dump({'problems': problems, 'fixed': fixed, 'dry_run': DRY_RUN}, f, indent=2)
    print(f"tag taxonomy issues: {len(problems)}; fixed: {len(fixed)}; report: {os.path.relpath(report, ROOT)}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os
from typing import Dict, List, Set
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
    load_json,
    write_report,
    DRY_RUN,
)

DEFAULT_TAXONOMY = {
    "required_frontmatter": ["tags", "type", "world", "status", "created", "updated"],
    "required_tags": ["world", "type", "status"],
    "allowed_status": ["draft", "active", "deprecated", "stub"],
    "allowed_world": ["Aethermoor", "Aquabyssos", "Both"],
}


def normalize_tag(tag: str) -> str:
    return tag.strip().lower().replace(" ", "-")


def main():
    taxonomy_path = os.path.join(DATA_DIR, "tag-taxonomy.json")
    taxonomy = load_json(taxonomy_path, DEFAULT_TAXONOMY)

    files = list_markdown_files(ROOT_DIR)
    changed = 0
    tag_index: Dict[str, List[str]] = {}

    for path in files:
        md = read_file(path)
        fm, body = split_frontmatter(md)
        tags = fm.get("tags") or []
        if not isinstance(tags, list):
            tags = []
        normalized = sorted({normalize_tag(t) for t in tags if str(t).strip()})
        if normalized != tags:
            fm["tags"] = normalized
            changed += 1
            if not DRY_RUN:
                backup_file(path)
                content = build_frontmatter(fm) + "\n" + body
                write_file(path, content)
        for t in normalized:
            tag_index.setdefault(t, []).append(os.path.relpath(path, ROOT_DIR))

    # Save taxonomy (ensure it exists)
    save_json(taxonomy_path, taxonomy)

    # Build report
    lines: List[str] = [
        "VAULT IMPROVEMENT PHASE 5: Tag Taxonomy Standardizer",
        "",
        f"Files scanned: {len(files)}",
        f"Files updated (tag normalization): {changed}",
        "",
        "Top tags (first 200):",
    ]
    items = sorted(((t, len(paths)) for t, paths in tag_index.items()), key=lambda x: -x[1])
    for t, cnt in items[:200]:
        lines.append(f"- {t}: {cnt}")
    write_report("tag_audit.md", "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()