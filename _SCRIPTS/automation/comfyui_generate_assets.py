#!/usr/bin/env python3
"""
Generate TTRPG assets using ComfyUI based on Obsidian note frontmatter.

Requirements:
  pip install requests pyyaml

Usage examples:
  python _SCRIPTS/automation/comfyui_generate_assets.py --types npc location --limit 5
  python _SCRIPTS/automation/comfyui_generate_assets.py --folders 03_People/NPCs --ckpt v1-5-pruned-emaonly.safetensors

ComfyUI server:
  Start ComfyUI with API enabled (default):
    python main.py --listen 127.0.0.1 --port 8188

This script will:
  - Read frontmatter from target notes
  - Build prompts via `_METADATA/templates/prompt_templates.yaml` (fallbacks included)
  - Submit a workflow to ComfyUI using `.comfyui/workflows/ttrpg_sd15_asset.json`
  - Download generated images into `04_Resources/Assets/Generated/<type>/`
"""

from __future__ import annotations

import argparse
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml  # type: ignore
    import requests  # type: ignore
except Exception as exc:  # pragma: no cover
    print("Missing dependencies. Please run:\n  pip install requests pyyaml\n")
    raise

VAULT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKFLOW = VAULT_ROOT / ".comfyui" / "workflows" / "ttrpg_sd15_asset.json"
TEMPLATES_FILE = VAULT_ROOT / "_METADATA" / "templates" / "prompt_templates.yaml"
OUTPUT_BASE = VAULT_ROOT / "04_Resources" / "Assets" / "Generated"


def read_frontmatter(note_path: Path) -> Dict[str, Any]:
    text = note_path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---"):
        return {}
    match = re.search(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL | re.MULTILINE)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1)) or {}
        if not isinstance(data, dict):
            return {}
        return data
    except Exception:
        return {}


def load_templates() -> Dict[str, Dict[str, str]]:
    if TEMPLATES_FILE.exists():
        try:
            return yaml.safe_load(TEMPLATES_FILE.read_text(encoding="utf-8")) or {}
        except Exception:
            pass
    # Fallbacks
    return {
        "npc": {
            "positive": (
                "portrait of {name}, {race} {class} {role}. {description}. cinematic lighting, "
                "detailed face, expressive eyes, intricate costume, {faction} influence, {mood} mood, "
                "artstation, highly detailed, sharp focus, 8k, masterpiece {style}"
            ),
            "negative": (
                "worst quality, lowres, blurry, text, logo, watermark, disfigured, extra fingers, "
                "mangled hands, deformed, low contrast, jpeg artifacts"
            ),
        },
        "location": {
            "positive": (
                "{biome} location named {name}. {description}. sweeping scale, atmospheric perspective, "
                "volumetric light, intricate details, {era} architecture, {mood} mood, concept art, "
                "matte painting, 8k, ultra-detailed {style}"
            ),
            "negative": (
                "worst quality, lowres, blurry, text, logo, watermark, humans, characters, cartoon, oversaturated, noisy"
            ),
        },
        "item": {
            "positive": (
                "studio photo of {name}, a {rarity} {item_type}. {description}. product photography, "
                "dramatic lighting, high detail, textured materials, 8k macro, museum catalog style {style}"
            ),
            "negative": (
                "worst quality, lowres, blurry, text, logo, watermark, hands, people, oversaturated, noise"
            ),
        },
    }


def safe_format(template: str, data: Dict[str, Any]) -> str:
    class SafeDict(dict):
        def __missing__(self, key):
            return ""

    return template.format_map(SafeDict(**data))


def find_nodes(graph: Dict[str, Any]) -> Dict[str, str]:
    """Best-effort role detection for common nodes in a ComfyUI workflow.

    Returns a mapping with keys: checkpoint, positive_clip, negative_clip,
    empty_latent, ksampler, save_image, load_image, lora (first detected).
    """
    roles: Dict[str, str] = {}
    # Detect CLIPTextEncode nodes; prefer placeholders if present
    clip_nodes = []
    for nid, node in graph.items():
        if node.get("class_type") == "CLIPTextEncode":
            clip_nodes.append((nid, node))
    # Placeholder-aware assignment
    for nid, node in clip_nodes:
        text = (node.get("inputs", {}) or {}).get("text", "")
        if isinstance(text, str) and "PLACEHOLDER_POSITIVE" in text:
            roles["positive_clip"] = nid
        if isinstance(text, str) and "PLACEHOLDER_NEGATIVE" in text:
            roles["negative_clip"] = nid
    # Fallback: first two CLIP nodes
    if "positive_clip" not in roles and clip_nodes:
        roles["positive_clip"] = clip_nodes[0][0]
    if "negative_clip" not in roles and len(clip_nodes) > 1:
        roles["negative_clip"] = clip_nodes[1][0]

    # Checkpoint, EmptyLatentImage, KSampler, SaveImage, LoadImage, LoraLoader
    for nid, node in graph.items():
        ct = node.get("class_type")
        if ct == "CheckpointLoaderSimple" and "checkpoint" not in roles:
            roles["checkpoint"] = nid
        elif ct == "EmptyLatentImage" and "empty_latent" not in roles:
            roles["empty_latent"] = nid
        elif ct == "KSampler" and "ksampler" not in roles:
            roles["ksampler"] = nid
        elif ct == "SaveImage" and "save_image" not in roles:
            roles["save_image"] = nid
        elif ct == "LoadImage" and "load_image" not in roles:
            roles["load_image"] = nid
        elif (ct == "LoraLoader" or ct == "LoraLoaderModelOnly") and "lora" not in roles:
            roles["lora"] = nid
    return roles


def build_graph(base_graph: Dict[str, Any], *, positive: str, negative: str, seed: int, steps: int,
                cfg: float, width: int, height: int, ckpt_name: Optional[str], filename_prefix: str,
                init_image_name: Optional[str], lora_name: Optional[str], lora_strength: Optional[float]) -> Dict[str, Any]:
    graph = {k: (v.copy() if isinstance(v, dict) else v) for k, v in base_graph.items()}
    roles = find_nodes(graph)

    # Update CLIPTextEncode inputs
    pos_id = roles.get("positive_clip")
    neg_id = roles.get("negative_clip")
    if pos_id:
        graph[pos_id]["inputs"]["text"] = positive
    if neg_id:
        graph[neg_id]["inputs"]["text"] = negative

    # Update latent size
    latent_id = roles.get("empty_latent")
    if latent_id:
        graph[latent_id]["inputs"]["width"] = width
        graph[latent_id]["inputs"]["height"] = height

    # Sampler params
    ks_id = roles.get("ksampler")
    if ks_id:
        graph[ks_id]["inputs"]["seed"] = int(seed)
        graph[ks_id]["inputs"]["steps"] = int(steps)
        graph[ks_id]["inputs"]["cfg"] = float(cfg)

    # Checkpoint override
    if ckpt_name and roles.get("checkpoint"):
        graph[roles["checkpoint"]]["inputs"]["ckpt_name"] = ckpt_name

    # Output filename prefix
    if roles.get("save_image"):
        graph[roles["save_image"]]["inputs"]["filename_prefix"] = filename_prefix

    # Init image (if a LoadImage node exists and an image name provided)
    if init_image_name and roles.get("load_image"):
        graph[roles["load_image"]]["inputs"]["image"] = init_image_name

    # LoRA (only if workflow already contains a LoRA node)
    if lora_name and roles.get("lora"):
        lnode = graph[roles["lora"]]
        inputs = lnode.get("inputs", {})
        inputs["lora_name"] = lora_name
        if lora_strength is not None:
            # Try common fields
            if "strength_model" in inputs:
                inputs["strength_model"] = float(lora_strength)
            if "strength_clip" in inputs:
                inputs["strength_clip"] = float(max(0.0, min(1.0, lora_strength)))
    return graph


def comfy_post_prompt(server: str, graph: Dict[str, Any]) -> str:
    resp = requests.post(
        f"{server.rstrip('/')}/prompt",
        json={"prompt": graph, "client_id": "obsidian_vault"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("prompt_id") or data.get("id")


def comfy_wait_and_fetch(server: str, prompt_id: str, timeout_s: int = 300) -> List[Dict[str, Any]]:
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        hist = requests.get(f"{server.rstrip('/')}/history/{prompt_id}", timeout=15)
        if hist.status_code == 200:
            j = hist.json()
            if isinstance(j, dict) and j:
                last = j.get(prompt_id) or next(iter(j.values()))
                if last and last.get("status", {}).get("completed"):
                    break
        time.sleep(1.0)
    if not last:
        return []
    # Collect image descriptors
    images: List[Dict[str, Any]] = []
    for node_id, node_outputs in (last.get("outputs") or {}).items():
        imgs = node_outputs.get("images") or []
        for im in imgs:
            images.append(im)
    return images


def comfy_download_image(server: str, image_info: Dict[str, Any]) -> bytes:
    params = {
        "filename": image_info.get("filename"),
        "subfolder": image_info.get("subfolder", ""),
        "type": image_info.get("type", "output"),
    }
    r = requests.get(f"{server.rstrip('/')}/view", params=params, timeout=60)
    r.raise_for_status()
    return r.content


def comfy_upload_image(server: str, file_path: Path) -> str:
    """Upload an image to ComfyUI's input folder; returns the filename.
    Requires ComfyUI API with /upload/image route available.
    """
    with open(file_path, "rb") as f:
        files = {"image": (file_path.name, f, "application/octet-stream")}
        r = requests.post(f"{server.rstrip('/')}/upload/image", files=files, timeout=120)
        r.raise_for_status()
    return file_path.name


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def iter_target_files(vault_root: Path, folders: List[str], types: List[str]) -> List[Path]:
    results: List[Path] = []
    if folders:
        for rel in folders:
            base = vault_root / rel
            if base.is_dir():
                results.extend(base.rglob("*.md"))
    else:
        # Default folders by type
        mapping = {
            "npc": ["03_People/NPCs"],
            "location": ["02_Worldbuilding/Locations"],
            "item": ["02_Worldbuilding/Items"],
        }
        for t in types:
            for rel in mapping.get(t, []):
                d = vault_root / rel
                if d.is_dir():
                    results.extend(d.rglob("*.md"))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate assets via ComfyUI from Obsidian notes")
    parser.add_argument("--server", default=os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188"))
    parser.add_argument("--types", nargs="*", default=["npc", "location", "item"], help="entity types to generate")
    parser.add_argument("--folders", nargs="*", default=[], help="explicit folders to scan")
    parser.add_argument("--limit", type=int, default=10, help="max number of notes to process")
    parser.add_argument("--ckpt", default=None, help="checkpoint filename in ComfyUI models folder")
    parser.add_argument("--workflow", default=os.environ.get("COMFYUI_WORKFLOW"), help="path to ComfyUI workflow JSON (or set COMFYUI_WORKFLOW)")
    parser.add_argument("--width", type=int, default=768)
    parser.add_argument("--height", type=int, default=768)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--cfg", type=float, default=7.0)
    parser.add_argument("--init_image", default=None, help="path to an init image to feed any LoadImage node (will be uploaded)")
    parser.add_argument("--lora", default=None, help="LoRA name (must exist in workflow). Optionally use name:strength (0-1)")
    parser.add_argument("--embed", action="store_true", help="append markdown embed of generated image to the source note")
    parser.add_argument("--out_by_campaign", action="store_true", help="organize outputs into subfolders by campaign")
    parser.add_argument("--campaign_key", default="campaign", help="frontmatter key for campaign name")
    args = parser.parse_args()

    templates = load_templates()
    if not args.workflow:
        raise SystemExit("No workflow specified. Use --workflow /path/to/workflow.json or set COMFYUI_WORKFLOW.")
    wf_path = Path(args.workflow)
    base_graph = yaml.safe_load(wf_path.read_text(encoding="utf-8")) if wf_path.exists() else {}
    if not base_graph:
        raise SystemExit(f"Workflow not found or empty: {wf_path}")

    files = iter_target_files(VAULT_ROOT, args.folders, args.types)
    if not files:
        print("No markdown files found to process.")
        return

    processed = 0
    for note_path in files:
        if processed >= args.limit:
            break
        fm = read_frontmatter(note_path)
        entity_type = (fm.get("type") or "").lower()
        if entity_type not in args.types:
            # Allow override via folder targeting
            if not args.folders:
                continue
            # Infer from folder name
            infer = None
            for t in args.types:
                if f"/{t}".lower() in str(note_path.parent).lower():
                    infer = t
                    break
            entity_type = infer or (args.types[0] if args.types else "npc")

        name = fm.get("name") or note_path.stem
        data = {
            **fm,
            "name": name,
            "tags": ", ".join(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else str(fm.get("tags", "")),
        }

        tpl = templates.get(entity_type) or templates.get("npc")
        positive = safe_format(tpl.get("positive", "{name}"), data)
        negative = safe_format(tpl.get("negative", ""), data)

        filename_prefix = f"{entity_type}_{fm.get('id', '')}_{name}".replace(" ", "_")

        # Optional: upload init image
        init_image_name: Optional[str] = None
        if args.init_image:
            img_path = Path(args.init_image)
            if img_path.exists():
                try:
                    init_image_name = comfy_upload_image(args.server, img_path)
                except Exception as e:
                    print(f"Init image upload failed: {e}")

        # Optional: LoRA config (only applied if node exists)
        lora_name = None
        lora_strength: Optional[float] = None
        if args.lora:
            if ":" in args.lora:
                l_name, l_str = args.lora.split(":", 1)
                lora_name = l_name
                try:
                    lora_strength = float(l_str)
                except ValueError:
                    lora_strength = None
            else:
                lora_name = args.lora
        graph = build_graph(
            base_graph,
            positive=positive,
            negative=negative,
            seed=int(time.time()) % 2_000_000_000,
            steps=args.steps,
            cfg=args.cfg,
            width=args.width,
            height=args.height,
            ckpt_name=args.ckpt,
            filename_prefix=filename_prefix,
            init_image_name=init_image_name,
            lora_name=lora_name,
            lora_strength=lora_strength,
        )

        try:
            prompt_id = comfy_post_prompt(args.server, graph)
            images = comfy_wait_and_fetch(args.server, prompt_id)
            if not images:
                print(f"No images for {note_path}")
                continue
            # Save outputs
            # Output directory, optionally by campaign
            if args.out_by_campaign:
                campaign = str(fm.get(args.campaign_key, "_uncategorized")).strip() or "_uncategorized"
                out_dir = OUTPUT_BASE / entity_type / campaign
            else:
                out_dir = OUTPUT_BASE / entity_type
            ensure_dir(out_dir)
            for im in images:
                content = comfy_download_image(args.server, im)
                target = out_dir / im.get("filename", f"{filename_prefix}.png")
                with open(target, "wb") as f:
                    f.write(content)
                # Optional: embed into note
                if args.embed:
                    try:
                        rel_path = os.path.relpath(target, VAULT_ROOT)
                        append = f"\n\n## Generated Art\n![[{rel_path}]]\n"
                        with open(note_path, "a", encoding="utf-8") as nf:
                            nf.write(append)
                    except Exception as e:
                        print(f"Embed append failed for {note_path}: {e}")
            processed += 1
            print(f"Generated {len(images)} image(s) for {note_path}")
        except Exception as e:  # pragma: no cover
            print(f"Error for {note_path}: {e}")


if __name__ == "__main__":
    main()


