#!/usr/bin/env python3

import os, sys, subprocess, shutil

ROOT = os.environ.get('WORKSPACE_DIR', os.getcwd())
ARCH_ROOT = os.path.join(ROOT, '08_Archive', 'tmp_dedupe', 'dupe_files')
DRY_RUN = os.environ.get('DRY_RUN', '0') == '1'

def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, check=True)

def run_out(cmd) -> str:
    res = subprocess.run(cmd, cwd=ROOT, check=True, stdout=subprocess.PIPE)
    return res.stdout.decode('utf-8', errors='ignore')

def git_ls_files() -> list[str]:
    out = run_out(['git', 'ls-files'])
    return [line.strip() for line in out.splitlines() if line.strip()]

def is_suffix_two_md(path: str) -> bool:
    return path.endswith(' 2.md')

def compare_same(a: str, b: str) -> bool:
    try:
        with open(os.path.join(ROOT, a), 'rb') as fa, open(os.path.join(ROOT, b), 'rb') as fb:
            return fa.read() == fb.read()
    except Exception:
        return False

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def main():
    files = [f for f in git_ls_files() if is_suffix_two_md(f)]
    removed = moved = renamed = 0
    for f in files:
        orig = f[:-6] + '.md'  # replace ' 2.md' with '.md'
        f_abs = os.path.join(ROOT, f)
        orig_abs = os.path.join(ROOT, orig)
        if os.path.exists(orig_abs):
            if compare_same(f, orig):
                # exact dup; remove the ' 2.md'
                if not DRY_RUN:
                    run(['git', 'rm', '-f', '--', f])
                removed += 1
            else:
                # different; archive the ' 2.md'
                dest = os.path.join(ARCH_ROOT, f)
                if not DRY_RUN:
                    ensure_dir(os.path.dirname(dest))
                    # use git mv to keep history
                    run(['git', 'mv', '-f', '--', f, dest])
                moved += 1
        else:
            # no original; rename to original name
            if not DRY_RUN:
                run(['git', 'mv', '-f', '--', f, orig])
            renamed += 1
    print(f'removed:{removed} moved_to_archive:{moved} renamed:{renamed}')

if __name__ == '__main__':
    main()


