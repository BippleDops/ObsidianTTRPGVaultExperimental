import os
import re
import json
import shutil
import datetime
from typing import Tuple, Dict, Any, List, Optional, Iterable

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

ROOT_DIR = os.environ.get("ROOT_DIR") or os.environ.get("WORKSPACE_DIR") or os.getcwd()
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
DATA_DIR = os.path.join(ROOT_DIR, "data")
BACKUP_DIR = os.environ.get("BACKUP_DIR", "")
DRY_RUN = os.environ.get("DRY_RUN", "").strip() == "1"

MARKDOWN_EXTENSIONS = {".md", ".markdown"}

WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")

# Worlds and epochs mapping
WORLD_EPOCHS = {
    "Aethermoor": {"valid": {"AC", "BC"}, "invalid": {"AS", "BS"}},
    "Aquabyssos": {"valid": {"AS", "BS"}, "invalid": {"AC", "BC"}},
    "Both": {"valid": {"AC", "BC", "AS", "BS"}, "invalid": set()},
}

DANGER_LEVELS = ["Low", "Moderate", "High", "Extreme"]
STATUS_VALUES = ["draft", "active", "deprecated", "stub"]
TYPE_VALUES = [
    "NPC", "Location", "Lore", "Group", "Quest", "Item", "Hazard", "Event", "Mechanic", "Index"
]
WORLDS = ["Aethermoor", "Aquabyssos", "Both"]

SKIP_DIR_SUBSTRINGS = [
    f"{os.sep}.git{os.sep}",
    f"{os.sep}.obsidian{os.sep}",
    f"{os.sep}node_modules{os.sep}",
    f"{os.sep}reports{os.sep}",
    f"{os.sep}scripts{os.sep}",
    f"{os.sep}backups{os.sep}",
    f"{os.sep}data{os.sep}",
    f"{os.sep}04_Resources{os.sep}Assets{os.sep}",
    f"{os.sep}03_Mechanics{os.sep}CLI{os.sep}",
]


def ensure_dirs():
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    if BACKUP_DIR and not DRY_RUN:
        os.makedirs(BACKUP_DIR, exist_ok=True)


def is_markdown(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in MARKDOWN_EXTENSIONS


def list_markdown_files(root: Optional[str] = None) -> List[str]:
    if root is None:
        root = ROOT_DIR
    result: List[str] = []
    for base, dirs, files in os.walk(root):
        # Skip noisy directories early
        skip = False
        for sub in SKIP_DIR_SUBSTRINGS:
            if sub in base + os.sep:
                skip = True
                break
        if skip:
            continue
        if any(part.startswith(".") for part in base.split(os.sep)):
            continue
        for f in files:
            p = os.path.join(base, f)
            if is_markdown(p):
                result.append(p)
    return result


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def write_file(path: str, content: str):
    if DRY_RUN:
        return
    # ensure dir exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def backup_file(path: str):
    if DRY_RUN:
        return
    if not BACKUP_DIR:
        return
    rel = os.path.relpath(path, ROOT_DIR)
    dest = os.path.join(BACKUP_DIR, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(path):
        shutil.copy2(path, dest)


def split_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end != -1:
            yaml_str = content[4:end]
            body = content[end + 5 :]
            data: Dict[str, Any] = {}
            if yaml:
                try:
                    data = yaml.safe_load(yaml_str) or {}
                except Exception:
                    data = {}
            else:
                # naive fallback: no YAML support
                data = {}
            return data, body
    return {}, content


def build_frontmatter(data: Dict[str, Any]) -> str:
    # ensure updated timestamp gets ISO-8601 if missing
    if "updated" not in data:
        data["updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if yaml:
        yaml_str = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
    else:
        yaml_str = json.dumps(data, ensure_ascii=False, indent=2)
    return f"---\n{yaml_str}\n---\n"


def merge_frontmatter(original: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(original)
    for k, v in updates.items():
        merged[k] = v
    # Always bump updated when changes occur
    merged["updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return merged


def infer_world_from_path(path: str) -> Optional[str]:
    lower = path.lower()
    if "aquabyssos" in lower:
        return "Aquabyssos"
    if "aethermoor" in lower:
        return "Aethermoor"
    return None


def extract_title_from_path(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def find_wiki_links(markdown: str) -> List[str]:
    links: List[str] = []
    for m in WIKI_LINK_PATTERN.finditer(markdown):
        inner = m.group(1).strip()
        if "|" in inner:
            target = inner.split("|", 1)[0].strip()
        else:
            target = inner
        # Skip anchors, external and embeds
        if not target or target.startswith("#"):
            continue
        if "://" in target or target.startswith("mailto:"):
            continue
        # Skip file paths (we'll normalize elsewhere)
        if "/" in target or "\\" in target:
            continue
        links.append(target)
    return links


def iter_wiki_links_with_spans(markdown: str) -> Iterable[Tuple[int, int, str, str, Optional[str]]]:
    # yields (start, end, full_match, target, alias)
    for m in WIKI_LINK_PATTERN.finditer(markdown):
        inner = m.group(1).strip()
        target = inner
        alias = None
        if "|" in inner:
            target, alias = inner.split("|", 1)
            target = target.strip()
            alias = alias.strip() or None
        yield m.start(), m.end(), m.group(0), target, alias


def normalize_epoch_tokens(text: str) -> str:
    # Normalize punctuation variants like A.C. -> AC, B.S. -> BS, etc.
    text = re.sub(r"\bA\.?\s*C\.\b", "AC", text)
    text = re.sub(r"\bB\.?\s*C\.\b", "BC", text)
    text = re.sub(r"\bA\.?\s*S\.\b", "AS", text)
    text = re.sub(r"\bB\.?\s*S\.\b", "BS", text)
    return text


def contains_any_epoch(text: str) -> bool:
    return any(tok in text for tok in ("AC", "BC", "AS", "BS"))


def detect_mixed_epochs(text: str) -> bool:
    present = {tok for tok in ("AC", "BC", "AS", "BS") if tok in text}
    # Mixed if both Aethermoor and Aquabyssos tokens co-exist
    return (present & {"AC", "BC"}) and (present & {"AS", "BS"})


def load_json(path: str, default: Any) -> Any:
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except Exception:
            return default


def save_json(path: str, data: Any):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)


def write_report(name: str, content: str):
    ensure_dirs()
    path = os.path.join(REPORTS_DIR, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def set_default_frontmatter(data: Dict[str, Any], inferred_world: Optional[str]) -> Dict[str, Any]:
    new_data = dict(data)
    # Ensure keys by type (best-effort)
    entity_type = new_data.get("type")
    # required base keys
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if "created" not in new_data:
        new_data["created"] = now_iso
    new_data["updated"] = now_iso
    if "status" not in new_data:
        new_data["status"] = "draft"
    if "world" not in new_data and inferred_world:
        new_data["world"] = inferred_world
    if "tags" not in new_data or not isinstance(new_data["tags"], list):
        new_data["tags"] = []
    # Ensure required tags presence (world/type/status)
    required_tag_values = []
    if new_data.get("world"):
        required_tag_values.append(str(new_data["world"]).lower())
    if entity_type:
        required_tag_values.append(str(entity_type).lower())
    if new_data.get("status"):
        required_tag_values.append(str(new_data["status"]).lower())
    tag_set = {str(t).strip().lower().replace(" ", "-") for t in new_data["tags"] if str(t).strip()}
    tag_set.update(required_tag_values)
    new_data["tags"] = sorted(tag_set)
    return new_data


def ensure_section(markdown: str, heading: str) -> Tuple[str, bool]:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    if pattern.search(markdown):
        return markdown, False
    # Append section at end
    addition = f"\n\n## {heading}\n\n"
    return markdown + addition, True


def add_backlink(markdown: str, source_title: str) -> Tuple[str, bool]:
    # Use a Connections section to store backlinks
    updated, created = ensure_section(markdown, "Connections")
    link_line = f"- [[{source_title}]]\n"
    if link_line in updated:
        return updated, False
    return updated + link_line, True


def guess_entity_type_from_dir(path: str) -> Optional[str]:
    parts = [p.lower() for p in path.split(os.sep)]
    if "people" in parts or "npc" in parts:
        return "NPC"
    if "places" in parts:
        return "Location"
    if "quests" in parts:
        return "Quest"
    if "groups" in parts or "orgs" in parts or "organizations" in parts:
        return "Group"
    if "lore" in parts:
        return "Lore"
    if "items" in parts:
        return "Item"
    if "hazards" in parts:
        return "Hazard"
    if "events" in parts:
        return "Event"
    if "gm_resources" in parts or "session_tools" in parts or "reference_cards" in parts:
        return "Mechanic"
    if "player_resources" in parts or "templates" in parts or "indexes" in parts:
        return "Index"
    return None


def guess_entity_type_from_title(title: str) -> Optional[str]:
    t = title.lower()
    # Heuristic keywords
    if any(k in t for k in ["port", "temple", "keep", "wastes", "palace", "harbor", "cathedral", "isle", "lake", "reef", "cavern", "quarter", "district"]):
        return "Location"
    if any(k in t for k in ["order", "guild", "syndicate", "cabal", "company", "crew", "clan", "family", "parliament", "academy", "authority", "church", "cult"]):
        return "Group"
    if any(k in t for k in ["doctrine", "process", "ritual", "legend", "myth", "treatise", "artifact", "phenomenon", "tradition", "heresy", "chronicle"]):
        return "Lore"
    if any(k in t for k in ["king", "queen", "duke", "archon", "captain", "lord", "lady", "abbot", "abbess", "priest", "bishop", "emperor", "empress", "sir", "madam"]):
        return "NPC"
    return None


def build_seed_scaffold(entity_type: str, world: Optional[str]) -> str:
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    frontmatter: Dict[str, Any] = {
        "tags": [str(world or "both").lower(), entity_type.lower(), "draft"],
        "type": entity_type,
        "world": world or "Both",
        "status": "draft",
        "created": now_iso,
        "updated": now_iso,
    }
    fm = build_frontmatter(frontmatter)
    scaffold_sections = {
        "NPC": ["Overview", "Appearance", "Personality", "Goals", "Relationships", "Hooks", "Stat Block"],
        "Location": ["Overview", "History", "Layout", "Notables", "Threats", "Hooks"],
        "Lore": ["Overview", "Historical Context", "Current Relevance", "See Also"],
        "Group": ["Overview", "Structure", "Goals", "Assets", "Conflicts", "Hooks"],
    }
    sections = scaffold_sections.get(entity_type, ["Overview"])
    body = "\n".join([f"## {s}\n\nTODO" for s in sections]) + "\n"
    return fm + "\n" + body


def write_diff_summary(original: str, updated: str, max_lines: int = 80) -> str:
    if original == updated:
        return "(no changes)"
    import difflib
    diff = difflib.unified_diff(
        original.splitlines(), updated.splitlines(), lineterm=""
    )
    lines = list(diff)
    if len(lines) > max_lines:
        head = "\n".join(lines[: max_lines // 2])
        tail = "\n".join(lines[-max_lines // 2 :])
        return head + "\n...\n" + tail
    return "\n".join(lines)