#!/usr/bin/env python3

import os, re, json, sys

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'

TOPS = [d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d))]
FOCUS_DIRS = [d for d in TOPS if re.match(r'^(?:0[1-8]_|1-)', d)]

IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
TOP_NAME_TOKENS = [
    '01_Adventures','01_Campaigns','02_Worldbuilding','03_Mechanics','04_Resources',
    '05_Templates','06_GM_Resources','07_Player_Resources','08_Archive'
]

def list_md_files():
    files = []
    for top in FOCUS_DIRS:
        for dp, dn, fn in os.walk(os.path.join(ROOT, top)):
            for n in fn:
                if n.lower().endswith('.md'):
                    files.append(os.path.join(dp, n))
    return files

def is_suspicious(path: str) -> bool:
    base = os.path.basename(path)
    name = os.path.splitext(base)[0]
    lower = name.lower()
    # 1) template placeholders
    if '<%' in name and '%>' in name:
        return True
    # 2) trailing " 2" duplicates
    if re.search(r'\b2$', name) or re.search(r'\s2$', name) or ' 2.' in base:
        return True
    # 3) embedded image extension in title
    if any(ext in name.lower() for ext in ['.png','.jpg','.jpeg','.webp','.gif']):
        return True
    # 4) names that are actually top-level dir tokens
    if any(tok.replace('_',' ') in name for tok in TOP_NAME_TOKENS):
        return True
    # 5) obvious typos per user: 'abolet' in Lore duplicates
    if '02_Worldbuilding'+os.sep+'Lore'+os.sep in path and 'abolet' in lower:
        return True
    # 6) stray short tokens ending with punctuation like 'pn' from copy mishaps
    if name.endswith('pn') and '02_Worldbuilding'+os.sep+'Lore'+os.sep in path:
        return True
    return False

def main():
    files = list_md_files()
    suspicious = [os.path.relpath(p, ROOT) for p in files if is_suspicious(p)]
    for rel in suspicious:
        abs_path = os.path.join(ROOT, rel)
        if not DRY_RUN:
            try:
                os.remove(abs_path)
                print(f"deleted: {rel}")
            except Exception as e:
                print(f"failed_delete: {rel} -> {e}")
        else:
            print(f"would_delete: {rel}")
    report = os.path.join(ROOT, '08_Archive', 'reports', 'clean_misplaced_notes.json')
    os.makedirs(os.path.dirname(report), exist_ok=True)
    with open(report, 'w', encoding='utf-8') as f:
        json.dump({'deleted': None if DRY_RUN else suspicious, 'preview': suspicious if DRY_RUN else None}, f, indent=2)
    print(f"suspicious_count: {len(suspicious)} report:{os.path.relpath(report, ROOT)} dry_run:{DRY_RUN}")

if __name__ == '__main__':
    main()


