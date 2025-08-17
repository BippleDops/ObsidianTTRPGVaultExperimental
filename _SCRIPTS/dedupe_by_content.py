#!/usr/bin/env python3

import os, sys, re, json, hashlib, subprocess
import time

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'
REPORTS_DIR = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

SKIP_DIRS = {
    f"{os.sep}.git{os.sep}", f"{os.sep}.obsidian{os.sep}", f"{os.sep}node_modules{os.sep}",
    f"{os.sep}08_Archive{os.sep}", f"{os.sep}13_Performance{os.sep}", f"{os.sep}04_Resources{os.sep}Assets{os.sep}Generated{os.sep}",
    f"{os.sep}scripts{os.sep}", f"{os.sep}reports{os.sep}", f"{os.sep}backups{os.sep}"
}

def is_skipped(path: str) -> bool:
    p = path + ('' if path.endswith(os.sep) else os.sep)
    for s in SKIP_DIRS:
        if s in p:
            return True
    return False

def walk_md_files(root: str):
    for base, dirs, files in os.walk(root):
        # Skip unwanted directories early
        skip = False
        for s in SKIP_DIRS:
            if s in (base + os.sep):
                skip = True
                break
        if skip:
            continue
        for f in files:
            if f.lower().endswith('.md'):
                yield os.path.join(base, f)

def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1<<20), b''):
            h.update(chunk)
    return h.hexdigest()

FM_RE = re.compile(r"^---\n[\s\S]*?\n---\n", re.M)

def read_text(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def body_of(text: str) -> str:
    m = FM_RE.search(text)
    if m:
        text = text[m.end():]
    return '\n'.join(line.rstrip() for line in text.splitlines()).strip()

def body_hash(path: str) -> str:
    try:
        txt = read_text(path)
    except Exception:
        return ''
    b = body_of(txt)
    return hashlib.sha256(b.encode('utf-8', errors='ignore')).hexdigest()

def rel(path: str) -> str:
    return os.path.relpath(path, ROOT)

def git_last_commit_epoch(rel_path: str) -> int:
    try:
        out = subprocess.run(['git','log','-1','--format=%ct','--',rel_path], cwd=ROOT, check=True, stdout=subprocess.PIPE)
        s = out.stdout.decode('utf-8', errors='ignore').strip()
        return int(s) if s else 0
    except Exception:
        try:
            return int(os.path.getmtime(os.path.join(ROOT, rel_path)))
        except Exception:
            return 0

def recent_repo_epochs(n: int = 10) -> set[int]:
    try:
        out = subprocess.run(['git','log', f'-n{n}','--format=%ct'], cwd=ROOT, check=True, stdout=subprocess.PIPE)
        return {int(x) for x in out.stdout.decode('utf-8', errors='ignore').split() if x.strip()}
    except Exception:
        return set()

def score_canonical(rel_path: str, recent_set: set[int]) -> tuple:
    # Higher score is better; we'll sort reverse
    p = rel_path
    t = git_last_commit_epoch(rel_path)
    in_recent = 1 if t in recent_set else 0
    core_bonus = 1 if p.startswith('02_Worldbuilding'+os.sep) else 0
    non_archive = 1 if not p.startswith('08_Archive'+os.sep) else 0
    no_suffix_two = 1 if ' 2.md' not in p else 0
    neg_len = -len(p)
    return (in_recent, t, core_bonus, non_archive, no_suffix_two, neg_len, p)

def choose_canonical(paths: list[str], recent_set: set[int]) -> str:
    return sorted(paths, key=lambda x: score_canonical(x, recent_set), reverse=True)[0]

def run_git(args: list[str]):
    if DRY_RUN:
        return
    subprocess.run(['git'] + args, cwd=ROOT, check=True)

WIKI_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

def normalize_wikilink_target(t: str) -> str:
    # Strip anchors and .md for matching
    if '#' in t:
        t = t.split('#',1)[0]
    if t.lower().endswith('.md'):
        t = t[:-3]
    return t

def main():
    # Build content hash map (body only)
    hash_to_paths: dict[str, list[str]] = {}
    for abs_path in walk_md_files(ROOT):
        r = rel(abs_path)
        try:
            h = body_hash(abs_path)
        except Exception:
            continue
        hash_to_paths.setdefault(h, []).append(r)

    # Determine canonical keep and duplicates
    mapping_dead_to_canon: dict[str, str] = {}
    groups = []
    recent_set = recent_repo_epochs(10)
    for h, paths in hash_to_paths.items():
        if len(paths) > 1:
            keep = choose_canonical(paths, recent_set)
            dups = [p for p in paths if p != keep]
            for d in dups:
                mapping_dead_to_canon[d] = keep
            groups.append({'hash': h, 'keep': keep, 'dups': dups})

    # Rewrite wikilinks across vault for explicit path targets
    changed_files = []
    removed_basename_to_canon: dict[str, str] = {os.path.splitext(os.path.basename(k))[0]: v for k, v in mapping_dead_to_canon.items()}
    for abs_path in walk_md_files(ROOT):
        r = rel(abs_path)
        try:
            txt = open(abs_path, 'r', encoding='utf-8').read()
        except Exception:
            continue
        orig = txt
        def repl(m):
            target = m.group(1)
            norm = normalize_wikilink_target(target)
            # Build candidate keys that may match mapping (with and without .md)
            # Attempt full relative path match first
            cand_rel = norm
            if not cand_rel.lower().endswith('.md'):
                cand_rel_md = cand_rel + '.md'
            else:
                cand_rel_md = cand_rel
                cand_rel = cand_rel[:-3]
            # If target contains '/', we can try direct mapping
            new_target = None
            if '/' in norm and (cand_rel_md in mapping_dead_to_canon or cand_rel in {k[:-3] for k in mapping_dead_to_canon}):
                key = cand_rel_md if cand_rel_md in mapping_dead_to_canon else (cand_rel + '.md')
                canon = mapping_dead_to_canon.get(key)
                if canon:
                    new_target = canon[:-3] if canon.lower().endswith('.md') else canon
            else:
                # bare title case
                canon = removed_basename_to_canon.get(norm)
                if canon:
                    new_target = canon[:-3] if canon.lower().endswith('.md') else canon
            # Replace preserving alias if any (we ignored alias, so just rebuild minimal link)
            if new_target:
                return f"[[{new_target}]]"
            return m.group(0)
        txt = WIKI_RE.sub(repl, txt)
        # also rewrite markdown links to .md
        def repl_md(m):
            label, url = m.group(1), m.group(2)
            if url.lower().endswith('.md'):
                if url in mapping_dead_to_canon:
                    return f'[{label}]({mapping_dead_to_canon[url]})'
                bn = os.path.splitext(os.path.basename(url))[0]
                canon = removed_basename_to_canon.get(bn)
                if canon:
                    return f'[{label}]({canon})'
            return m.group(0)
        txt = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_md, txt)
        if txt != orig:
            if not DRY_RUN:
                with open(abs_path, 'w', encoding='utf-8') as f:
                    f.write(txt)
            changed_files.append(r)

    # Remove duplicate files
    removed = []
    for dead, canon in mapping_dead_to_canon.items():
        if not DRY_RUN:
            try:
                run_git(['rm', '-f', '--', dead])
                removed.append(dead)
            except Exception:
                pass
        else:
            removed.append(dead)

    report_path = os.path.join(REPORTS_DIR, 'dedupe_by_content.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'groups': groups,
            'removed': removed,
            'rewritten_files': changed_files,
            'dry_run': DRY_RUN
        }, f, indent=2)
    print(f"content-dedupe groups:{len(groups)} removed:{len(removed)} rewritten:{len(changed_files)} report:{os.path.relpath(report_path, ROOT)}")

if __name__ == '__main__':
    main()


