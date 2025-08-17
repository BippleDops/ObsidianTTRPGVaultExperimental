#!/usr/bin/env python3

import os, re, sys, json, datetime

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'
REPORTS_DIR = os.path.join(ROOT, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

SKIP_RE = re.compile(r"/(\.git|08_Archive|13_Performance|04_Resources/Assets/Generated)(/|$)")

FM_RE = re.compile(r"^---\n([\s\S]*?)\n---\n", re.M)

def parse_date_to_date(s: str):
    if s is None:
        return None
    s = s.strip().strip("'").strip('"')
    if not s:
        return None
    # accept YYYY-MM-DD
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d').date()
    except Exception:
        pass
    # accept ISO with time
    try:
        return datetime.datetime.fromisoformat(s.rstrip('Z')).date()
    except Exception:
        return None

def normalize_dates(fm_text: str):
    lines = fm_text.splitlines()
    created_idx = next((i for i,l in enumerate(lines) if l.lower().startswith('created:')), None)
    updated_idx = next((i for i,l in enumerate(lines) if l.lower().startswith('updated:')), None)
    created_val = None
    updated_val = None
    if created_idx is not None:
        created_val = lines[created_idx].split(':',1)[1].strip()
    if updated_idx is not None:
        updated_val = lines[updated_idx].split(':',1)[1].strip()
    created_dt = parse_date_to_date(created_val) if created_val else None
    updated_dt = parse_date_to_date(updated_val) if updated_val else None

    changed = False
    # If no created, set from file stat
    if not created_dt:
        try:
            st = os.stat(current_fp)
            ts = min(getattr(st, 'st_mtime', None) or st.st_ctime, st.st_ctime)
            created_dt = datetime.datetime.utcfromtimestamp(ts).date()
        except Exception:
            created_dt = datetime.date.today()
        if created_idx is None:
            lines.insert(0, f"created: {created_dt.isoformat()}")
        else:
            lines[created_idx] = f"created: {created_dt.isoformat()}"
        changed = True

    # If updated missing, set to created date (not now)
    if not updated_dt:
        updated_dt = created_dt
        if updated_idx is None:
            insert_pos = created_idx+1 if created_idx is not None else 0
            lines.insert(insert_pos, f"updated: {updated_dt.isoformat()}")
        else:
            lines[updated_idx] = f"updated: {updated_dt.isoformat()}"
        changed = True

    # Ensure updated >= created
    if updated_dt and created_dt and updated_dt < created_dt:
        updated_dt = created_dt
        if updated_idx is None:
            lines.append(f"updated: {updated_dt.isoformat()}")
        else:
            lines[updated_idx] = f"updated: {updated_dt.isoformat()}"
        changed = True

    # Normalize formats to YYYY-MM-DD for both
    def set_line(idx, key, dt):
        nonlocal changed
        if idx is None:
            lines.append(f"{key}: {dt.isoformat()}")
            changed = True
        else:
            new = f"{key}: {dt.isoformat()}"
            if lines[idx] != new:
                lines[idx] = new
                changed = True

    # After potential creation, recalc indices
    created_idx = next((i for i,l in enumerate(lines) if l.lower().startswith('created:')), None)
    updated_idx = next((i for i,l in enumerate(lines) if l.lower().startswith('updated:')), None)
    set_line(created_idx, 'created', created_dt)
    set_line(updated_idx, 'updated', updated_dt)

    return '\n'.join(lines), changed

def process_file(fp: str):
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            txt = f.read()
    except Exception:
        return None
    m = FM_RE.search(txt)
    if not m:
        # add minimal frontmatter
        today = datetime.date.today().isoformat()
        fm = f"created: {today}\nupdated: {today}"
        new = f"---\n{fm}\n---\n\n" + txt
        return new if not DRY_RUN else None

    fm_text = m.group(1)
    # set current file path for stat lookup
    global current_fp
    current_fp = fp
    new_fm, changed = normalize_dates(fm_text)
    if not changed:
        return None
    new_txt = txt[:m.start()] + f"---\n{new_fm}\n---\n" + txt[m.end():]
    return new_txt

def main():
    changes = []
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
            changes.append(os.path.relpath(fp, ROOT))
    report_path = os.path.join(REPORTS_DIR, 'audit_standardize_cr_dates.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({ 'changed_files': changes, 'count': len(changes), 'dry_run': DRY_RUN }, f, indent=2)
    print(f"standardized dates in {len(changes)} files; report: {os.path.relpath(report_path, ROOT)}")

if __name__ == '__main__':
    main()