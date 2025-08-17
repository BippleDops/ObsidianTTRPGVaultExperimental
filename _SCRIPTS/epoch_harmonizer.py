#!/usr/bin/env python3

import os, re, sys, json, datetime

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'
REPORTS_DIR = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

SKIP_RE = re.compile(r"/(\.git|08_Archive|13_Performance|04_Resources/Assets/Generated)(/|$)")
FM_RE = re.compile(r"^---\n([\s\S]*?)\n---\n", re.M)

def parse_epoch(s: str):
    if s is None: return None
    try:
        s2 = s.strip().strip("'").strip('"')
        if not s2: return None
        # Numeric? seconds or milliseconds
        if re.fullmatch(r"\d+", s2):
            v = int(s2)
            if v > 10_000_000_000: # milliseconds
                v = v // 1000
            if v < 0:
                return None
            return datetime.datetime.utcfromtimestamp(v)
    except Exception:
        return None
    return None

def parse_date(s: str):
    if not s: return None
    s2 = s.strip().strip("'").strip('"')
    if not s2: return None
    # date first
    for fmt in ('%Y-%m-%d', '%Y/%m/%d'):
        try: return datetime.datetime.strptime(s2, fmt)
        except Exception: pass
    # iso
    try:
        return datetime.datetime.fromisoformat(s2.rstrip('Z'))
    except Exception:
        pass
    return parse_epoch(s2)

def normalize_fm_dates(fm_text: str):
    lines = fm_text.splitlines()
    key_positions = {}
    for i, l in enumerate(lines):
        m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_\-]*):\s*(.*)$", l)
        if m: key_positions[m.group(1).lower()] = (i, m.group(1), m.group(2))
    created_dt = parse_date(key_positions.get('created', (None,None,None))[2]) if 'created' in key_positions else None
    updated_dt = parse_date(key_positions.get('updated', (None,None,None))[2]) if 'updated' in key_positions else None
    # fallbacks: created_epoch / updated_epoch
    if not created_dt and 'created_epoch' in key_positions:
        created_dt = parse_epoch(key_positions['created_epoch'][2])
    if not updated_dt and 'updated_epoch' in key_positions:
        updated_dt = parse_epoch(key_positions['updated_epoch'][2])

    changed = False
    def set_or_add(key, dt):
        nonlocal lines, changed
        # dt can be datetime or date; normalize to date
        iso = (dt.date() if hasattr(dt, 'date') else dt).isoformat()
        if key in key_positions:
            i, orig_key, _ = key_positions[key]
            new_line = f"{orig_key}: {iso}"
            if lines[i] != new_line:
                lines[i] = new_line
                changed = True
        else:
            lines.append(f"{key}: {iso}")
            changed = True

    # compare on date granularity to avoid tz issues
    if created_dt:
        cdate = created_dt.date()
        set_or_add('created', cdate)
    if updated_dt:
        udate = updated_dt.date()
        if created_dt and udate < created_dt.date():
            udate = created_dt.date()
        set_or_add('updated', udate)

    # if epoch keys exist, remove them in apply mode
    removed_epoch = False
    for k in ['created_epoch','updated_epoch']:
        if k in key_positions:
            i = key_positions[k][0]
            if not DRY_RUN:
                lines.pop(i)
                removed_epoch = True
    if removed_epoch: changed = True

    return '\n'.join(lines), changed

def process_file(fp: str):
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            txt = f.read()
    except Exception:
        return None
    m = FM_RE.search(txt)
    if not m:
        return None
    new_fm, changed = normalize_fm_dates(m.group(1))
    if not changed:
        return None
    new_txt = txt[:m.start()] + f"---\n{new_fm}\n---\n" + txt[m.end():]
    return new_txt

def main():
    changed_files = []
    for dp, dn, fn in os.walk(ROOT):
        rel_dp = os.path.relpath(dp, ROOT)
        if SKIP_RE.search('/'+rel_dp.replace('\\','/')+'/'):
            continue
        for name in fn:
            if not name.lower().endswith('.md'):
                continue
            fp = os.path.join(dp, name)
            new = process_file(fp)
            if new is None:
                continue
            if not DRY_RUN:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new)
            changed_files.append(os.path.relpath(fp, ROOT))
    report = os.path.join(REPORTS_DIR, 'epoch_harmonizer.json')
    with open(report, 'w', encoding='utf-8') as f:
        json.dump({'changed_files': changed_files, 'count': len(changed_files), 'dry_run': DRY_RUN}, f, indent=2)
    print(f"epoch harmonized {len(changed_files)} files; report: {os.path.relpath(report, ROOT)}")

if __name__ == '__main__':
    main()