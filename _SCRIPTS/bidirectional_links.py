#!/usr/bin/env python3

import os, re, sys, json

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'
REPORTS_DIR = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

SKIP_RE = re.compile(r"/(\.git|08_Archive|13_Performance|04_Resources/Assets/Generated)(/|$)")

LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

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

def rel_title(path):
    rel = os.path.relpath(path, ROOT)
    return os.path.splitext(rel)[0]

def read(p):
    try:
        with open(p,'r',encoding='utf-8') as f: return f.read()
    except Exception:
        return ''

def write(p,s):
    with open(p,'w',encoding='utf-8') as f: f.write(s)

def ensure_section(body, title, lines):
    hdr = f"## {title}"
    if re.search(rf"^##\s+{re.escape(title)}(\n|$)", body, re.M):
        return body
    block = '\n'.join(f"- {ln}" for ln in lines)
    return body.rstrip() + f"\n\n{hdr}\n\n{block}\n"

def apply_bidirectional(src_path, dst_title):
    txt = read(src_path)
    # preserve frontmatter as-is
    m = re.match(r"^---\n[\s\S]*?\n---\n", txt)
    prefix = ''
    body = txt
    if m:
        prefix = m.group(0)
        body = txt[m.end():]
    line = f"[[{dst_title}]]"
    # avoid duplicates
    if line in body:
        return None
    body = ensure_section(body, 'Cross-References', [line])
    return prefix + body

def main():
    files = walk_md()
    title_to_path = { rel_title(p): p for p in files }
    changed = []
    for p in files:
        txt = read(p)
        for m in LINK_RE.finditer(txt):
            target = m.group(1)
            # normalize title (strip .md)
            if target.lower().endswith('.md'):
                target = target[:-3]
            # if it's a path, keep as is, else try to resolve in map
            if '/' not in target:
                # prefer exact match on rel title
                # scan for matching basename across standard dirs
                matches = [t for t in title_to_path.keys() if t.endswith('/'+target)]
                if matches:
                    target = matches[0]
            dst_path = title_to_path.get(target)
            if not dst_path:
                # attempt fallback for path + basename mismatch
                continue
            src_title = rel_title(p)
            new_txt = apply_bidirectional(dst_path, src_title)
            if new_txt:
                if not DRY_RUN:
                    write(dst_path, new_txt)
                changed.append(os.path.relpath(dst_path, ROOT))
    report = os.path.join(REPORTS_DIR, 'bidirectional_links.json')
    with open(report,'w',encoding='utf-8') as f:
        json.dump({'changed_files': sorted(set(changed)), 'count': len(set(changed)), 'dry_run': DRY_RUN}, f, indent=2)
    print(f"added backlinks in {len(set(changed))} files; report: {os.path.relpath(report, ROOT)}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os
from typing import Dict, List, Set, Tuple
from common import (
    ROOT_DIR,
    list_markdown_files,
    read_file,
    write_file,
    backup_file,
    split_frontmatter,
    build_frontmatter,
    add_backlink,
    find_wiki_links,
    write_report,
    DRY_RUN,
)

# Heuristic skip list (index-like pages)
SKIP_NAMES_CONTAIN = {"index", "campaign_index", "table of contents", "master_index"}
SKIP_DIRS_CONTAIN = {"13_Performance/Indexes", "08_Archive"}
NAV_HUB_TITLES = {"Vault_Navigation_Hub", "Master_Campaign_Index", "Master_Lore_Index"}


def should_skip(path: str) -> bool:
    lower = path.lower()
    if any(s in lower for s in SKIP_NAMES_CONTAIN):
        return True
    if any(s.lower().replace("/", os.sep) in lower for s in SKIP_DIRS_CONTAIN):
        return True
    return False


def extract_title(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def main():
    files = list_markdown_files(ROOT_DIR)
    title_to_path: Dict[str, str] = {}
    for path in files:
        title_to_path[extract_title(path)] = path

    outgoing: Dict[str, Set[str]] = {p: set() for p in files}
    incoming: Dict[str, Set[str]] = {p: set() for p in files}

    for path in files:
        if should_skip(path):
            continue
        md = read_file(path)
        fm, body = split_frontmatter(md)
        src_title = extract_title(path)
        # Don't create backlinks to nav hubs from everything
        if src_title in NAV_HUB_TITLES:
            continue
        links = find_wiki_links(body)
        for t in links:
            if t == src_title:
                continue
            target_path = title_to_path.get(t)
            if not target_path or should_skip(target_path):
                continue
            outgoing[path].add(target_path)
            incoming[target_path].add(path)

    added_backlinks: List[Tuple[str, str]] = []
    for target_path, sources in incoming.items():
        if not sources:
            continue
        target_md = read_file(target_path)
        fm, body = split_frontmatter(target_md)
        changed = False
        for src_path in sorted(sources):
            src_title = extract_title(src_path)
            new_body, added = add_backlink(body, src_title)
            if added:
                body = new_body
                changed = True
                added_backlinks.append((os.path.relpath(target_path, ROOT_DIR), src_title))
        if changed:
            new_content = (build_frontmatter(fm) + "\n" + body) if fm else body
            if not DRY_RUN:
                backup_file(target_path)
                write_file(target_path, new_content)

    # Build report
    lines: List[str] = [
        "VAULT IMPROVEMENT PHASE 5: Bidirectional Link Enforcer",
        "",
        f"Total files scanned: {len(files)}",
        f"Backlinks added: {len(added_backlinks)}",
        "",
        "List of backlinks added (target <- source):",
    ]
    if not added_backlinks:
        lines.append("(none)")
    else:
        for target_rel, src_title in added_backlinks[:2000]:
            lines.append(f"- {target_rel} <- [[{src_title}]]")
        if len(added_backlinks) > 2000:
            lines.append(f"... and {len(added_backlinks) - 2000} more")

    write_report("bidirectional_links.md", "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()