#!/usr/bin/env python3

import os
from typing import Tuple

from common import (
    ROOT_DIR,
    list_markdown_files,
    read_file,
    write_file,
    split_frontmatter,
    build_frontmatter,
    merge_frontmatter,
    infer_world_from_path,
    guess_entity_type_from_dir,
    guess_entity_type_from_title,
)


def ensure_frontmatter(path: str, fm: dict, body: str) -> Tuple[dict, bool]:
    changed = False

    # Guess world and type
    world = fm.get("world") or infer_world_from_path(path) or "Both"
    etype = fm.get("type") or guess_entity_type_from_dir(path) or guess_entity_type_from_title(
        os.path.splitext(os.path.basename(path))[0]
    )

    updates = {}
    if "created" not in fm:
        updates["created"] = None  # will be set by build_frontmatter/merge
    if "updated" not in fm:
        updates["updated"] = None
    if "world" not in fm and world:
        updates["world"] = world
    if "type" not in fm and etype:
        updates["type"] = etype
    # Default status if missing
    if "status" not in fm:
        # Mark active if enriched marker is present, else draft->active promotion happens elsewhere
        updates["status"] = "active" if "<!-- enriched: true -->" in body else "draft"

    # Normalize tags to include world/type/status
    existing_tags = fm.get("tags")
    if not isinstance(existing_tags, list):
        existing_tags = []
    tag_set = {str(t).strip().lower().replace(" ", "-") for t in existing_tags if str(t).strip()}
    if world:
        tag_set.add(str(world).lower())
    if etype:
        tag_set.add(str(etype).lower())
    if updates.get("status") or fm.get("status"):
        tag_set.add(str(updates.get("status") or fm.get("status")).lower())
    if sorted(existing_tags) != sorted(tag_set):
        updates["tags"] = sorted(tag_set)

    if updates:
        new_fm = merge_frontmatter(fm, updates)
        changed = True
    else:
        new_fm = fm

    return new_fm, changed


def main():
    files = list_markdown_files(ROOT_DIR)
    fixed = 0
    for p in files:
        try:
            md = read_file(p)
        except Exception:
            continue
        fm, body = split_frontmatter(md)
        new_fm, changed = ensure_frontmatter(p, fm, body)
        if not fm and not changed:
            # No frontmatter existed; force-create minimal header
            changed = True
        if changed:
            content = build_frontmatter(new_fm) + "\n" + body
            try:
                write_file(p, content)
                fixed += 1
            except Exception:
                pass
    print(f"frontmatter fixed/normalized in {fixed} files")


if __name__ == "__main__":
    main()


