### ComfyUI Integration (Asset Generation)

Use ComfyUI to generate images for NPCs, Locations, and Items directly from note frontmatter.

#### Prerequisites
- ComfyUI running locally: `python main.py --listen 127.0.0.1 --port 8188`
- Python deps: `pip install requests pyyaml`

#### Workflow
- Use your existing ComfyUI workflow JSON (SD 1.5, SDXL, etc.)
- Prompt templates: `_METADATA/templates/prompt_templates.yaml`
- Output folder: `04_Resources/Assets/Generated/<type>/`

#### Frontmatter fields used
- `type` (npc|location|item), `id`, `name`, `description`, `faction`, `race`, `class`, `role`, `biome`, `mood`, `style`, `era`, `rarity`, `item_type`

#### Run
```bash
# Set your workflow (or pass --workflow explicitly)
export COMFYUI_WORKFLOW="/absolute/path/to/your/workflow.json"
python _SCRIPTS/automation/comfyui_generate_assets.py --types npc location item --limit 5

# Optional overrides
python _SCRIPTS/automation/comfyui_generate_assets.py --workflow \
  "/absolute/path/to/your/workflow.json" --ckpt v1-5-pruned-emaonly.safetensors \
  --width 896 --height 1152 --steps 35 --cfg 6.5

# Optional: init image, LoRA, organize by campaign, and embed output in source note
python _SCRIPTS/automation/comfyui_generate_assets.py --workflow \
  "/absolute/path/to/your/workflow.json" --types npc --limit 3 \
  --init_image "/path/to/pose_or_reference.png" --lora "myLora:0.8" \
  --out_by_campaign --campaign_key campaign --embed
```

#### Notes
- Change `ckpt` to a model you have installed in ComfyUI (Models/Checkpoints).
- For SDXL, swap the workflow to an SDXL version and adjust nodes accordingly.
- You can edit prompt templates to better match your setting/style.
 - The script will try to locate nodes by type and placeholder text (e.g., `PLACEHOLDER_POSITIVE`). If your workflow uses different nodes, specify `--workflow` and ensure it contains `CLIPTextEncode`, `EmptyLatentImage`, `KSampler`, and `SaveImage` nodes.
 - If your workflow includes `LoadImage`, `--init_image` will upload and route the image to that node. If it includes a `LoraLoader*` node, `--lora` can set its name and strength.

