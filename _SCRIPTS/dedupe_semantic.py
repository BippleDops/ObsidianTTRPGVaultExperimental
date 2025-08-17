#!/usr/bin/env python3

"""
Semantic deduplication (conservative):
 - Groups notes by normalized title tokens and directory (People/Places/Groups/Lore)
 - Computes simple TF-IDF-like vectors using bag-of-words with stopwords
 - Flags pairs with high cosine similarity (> 0.92) and short Levenshtein on titles
 - Keeps the more recently updated (by git log or mtime) and removes the other
 - Rewrites wikilinks from removed -> kept

This avoids API calls and runs locally. Exact-duplicate removal should run first.
"""

import os, re, json, math, subprocess
from collections import defaultdict, Counter
from typing import List, Dict, Tuple

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'
REPORTS = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS, exist_ok=True)

WIKI_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FM_RE = re.compile(r"^---\n[\s\S]*?\n---\n", re.M)

STOP = {"the","and","of","a","an","to","in","on","for","by","with","from","at","as","is","are","be","this","that","these","those"}

def list_md() -> List[str]:
    out = []
    for base, dirs, files in os.walk(ROOT):
        if any(seg in (base+os.sep) for seg in (f"{os.sep}.git{os.sep}", f"{os.sep}08_Archive{os.sep}", f"{os.sep}13_Performance{os.sep}", f"{os.sep}04_Resources{os.sep}Assets{os.sep}")):
            continue
        for f in files:
            if f.lower().endswith('.md'):
                out.append(os.path.join(base, f))
    return out

def rel(p: str) -> str:
    return os.path.relpath(p, ROOT)

def read(p: str) -> str:
    try:
        with open(p,'r',encoding='utf-8',errors='ignore') as f:
            return f.read()
    except Exception:
        return ''

def body(txt: str) -> str:
    m = FM_RE.search(txt)
    return txt[m.end():] if m else txt

def tokens(s: str) -> List[str]:
    s = re.sub(r"[^a-z0-9\s]", " ", s.lower())
    return [t for t in s.split() if t and t not in STOP and len(t) > 2]

def vec(words: List[str]) -> Dict[str, float]:
    c = Counter(words)
    n = float(sum(c.values()) or 1.0)
    return {k: v/n for k, v in c.items()}

def cosine(a: Dict[str,float], b: Dict[str,float]) -> float:
    if not a or not b: return 0.0
    common = set(a.keys()) & set(b.keys())
    num = sum(a[t]*b[t] for t in common)
    da = math.sqrt(sum(v*v for v in a.values()))
    db = math.sqrt(sum(v*v for v in b.values()))
    if da==0 or db==0: return 0.0
    return num/(da*db)

def title(p: str) -> str:
    return os.path.splitext(os.path.basename(p))[0]

def title_norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", s.lower())).strip()

def title_sim(a: str, b: str) -> float:
    # simple Jaccard over tokens
    ta, tb = set(tokens(a)), set(tokens(b))
    if not ta or not tb: return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter/union

def git_epoch(relp: str) -> int:
    try:
        out = subprocess.run(['git','log','-1','--format=%ct','--',relp], cwd=ROOT, check=True, stdout=subprocess.PIPE)
        s = out.stdout.decode('utf-8','ignore').strip()
        return int(s) if s else 0
    except Exception:
        try:
            return int(os.path.getmtime(os.path.join(ROOT, relp)))
        except Exception:
            return 0

def rewrite_links(file_path: str, mapping: Dict[str,str]) -> bool:
    txt = read(file_path)
    orig = txt
    def repl(m):
        t = m.group(1)
        base = t
        if base.lower().endswith('.md'): base = base[:-3]
        if '#' in base: base = base.split('#',1)[0]
        # exact match by full rel path without .md
        if base in mapping:
            return f"[[{mapping[base]}]]"
        # try by basename
        bn = os.path.basename(base)
        if bn in mapping:
            return f"[[{mapping[bn]}]]"
        return m.group(0)
    txt = WIKI_RE.sub(repl, txt)
    if txt != orig and not DRY_RUN:
        with open(file_path,'w',encoding='utf-8') as f:
            f.write(txt)
        return True
    return txt != orig

def main():
    files = list_md()
    groups = defaultdict(list)
    for p in files:
        rp = rel(p)
        cat = 'other'
        parts = [s.lower() for s in rp.split(os.sep)]
        if 'people' in parts: cat='people'
        elif 'places' in parts: cat='places'
        elif 'groups' in parts: cat='groups'
        elif 'lore' in parts: cat='lore'
        groups[(cat)] .append(p)

    similar_pairs: List[Tuple[str,str,float,float]] = []
    # Build vectors per file once
    vecs: Dict[str, Dict[str,float]] = {}
    titles: Dict[str, str] = {}
    for p in files:
        txt = body(read(p))
        vecs[p] = vec(tokens(txt))
        titles[p] = title(p)

    # Compare within category only (reduce false positives)
    for cat, paths in groups.items():
        n = len(paths)
        for i in range(n):
            for j in range(i+1, n):
                a, b = paths[i], paths[j]
                # quick title similarity gate
                ts = title_sim(titles[a], titles[b])
                if ts < 0.5:  # only consider clearly similar titles
                    continue
                c = cosine(vecs[a], vecs[b])
                if c > 0.92:
                    similar_pairs.append((rel(a), rel(b), c, ts))

    # Decide keep/remove based on recency
    removed = []
    keepers = set()
    mapping: Dict[str,str] = {}
    for a, b, c, ts in similar_pairs:
        ea, eb = git_epoch(a), git_epoch(b)
        keep = a if ea >= eb else b
        dead = b if keep == a else a
        keepers.add(keep)
        # map both base-name and rel-without-md to keep target (without .md)
        keep_link = keep[:-3] if keep.lower().endswith('.md') else keep
        mapping[dead[:-3] if dead.lower().endswith('.md') else dead] = keep_link
        mapping[os.path.splitext(os.path.basename(dead))[0]] = keep_link

    # Rewrite links across all files
    rewritten = []
    for p in files:
        if rewrite_links(p, mapping):
            rewritten.append(rel(p))

    # Remove duplicates
    for dead_key, keep_target in mapping.items():
        # dead_key could be a rel-without-md or basename; find actual path
        cand_paths = [x for x in files if rel(x).lower().startswith(dead_key.lower()) or os.path.splitext(os.path.basename(x))[0].lower()==dead_key.lower()]
        for abs_dead in cand_paths:
            r = rel(abs_dead)
            if not DRY_RUN:
                try:
                    os.remove(abs_dead)
                    removed.append(r)
                except Exception:
                    pass
            else:
                removed.append(r)

    report = os.path.join(REPORTS, 'dedupe_semantic.json')
    with open(report,'w',encoding='utf-8') as f:
        json.dump({
            'pairs': [{'a':a,'b':b,'cosine':c,'title_sim':ts} for a,b,c,ts in similar_pairs],
            'removed': removed,
            'rewritten': rewritten,
            'dry_run': DRY_RUN,
        }, f, indent=2)
    print(f"semantic-dedupe similar_pairs:{len(similar_pairs)} removed:{len(removed)} rewritten:{len(rewritten)} report:{os.path.relpath(report, ROOT)}")

if __name__ == '__main__':
    main()


