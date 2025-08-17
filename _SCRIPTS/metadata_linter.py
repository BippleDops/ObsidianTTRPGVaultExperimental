#!/usr/bin/env python3

import os, re, sys, json

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'
REPORTS_DIR = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

# Skip archives, performance logs, git, and the entire assets area (prompt files/galleries don't require content frontmatter)
SKIP_RE = re.compile(r"/(\.git|08_Archive|13_Performance|04_Resources/Assets)(/|$)")

FM_RE = re.compile(r"^---\n([\s\S]*?)\n---\n", re.M)

REQUIRED_KEYS = ['created','updated']
RECOMMENDED_KEYS = ['tags','type','status']

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

def lint_fm(txt):
    m = FM_RE.search(txt)
    if not m:
        return {'missing_frontmatter': True, 'missing_required': REQUIRED_KEYS}
    fm = m.group(1)
    keys = {}
    for line in fm.splitlines():
        k = line.split(':',1)[0].strip() if ':' in line else None
        if k: keys[k] = True
    missing_required = [k for k in REQUIRED_KEYS if k not in keys]
    missing_recommended = [k for k in RECOMMENDED_KEYS if k not in keys]
    return {'missing_frontmatter': False, 'missing_required': missing_required, 'missing_recommended': missing_recommended}

def main():
    files = walk_md()
    problems = []
    for p in files:
        try:
            with open(p,'r',encoding='utf-8') as f:
                txt = f.read()
        except Exception:
            continue
        res = lint_fm(txt)
        if res['missing_frontmatter'] or res['missing_required'] or res['missing_recommended']:
            problems.append({'file': os.path.relpath(p, ROOT), **res})
            # auto-fix missing frontmatter by inserting minimal block
            if not DRY_RUN and res['missing_frontmatter']:
                with open(p,'w',encoding='utf-8') as f:
                    f.write('---\ncreated: 2024-01-01\nupdated: 2024-01-01\n---\n\n' + txt)
    report = os.path.join(REPORTS_DIR, 'metadata_linter.json')
    with open(report,'w',encoding='utf-8') as f:
        json.dump({'problems': problems, 'count': len(problems), 'dry_run': DRY_RUN}, f, indent=2)
    print(f"metadata linter found {len(problems)} files with issues; report: {os.path.relpath(report, ROOT)}")

if __name__ == '__main__':
    main()