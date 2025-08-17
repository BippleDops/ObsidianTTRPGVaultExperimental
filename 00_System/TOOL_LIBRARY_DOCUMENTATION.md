---
title: TOOL_LIBRARY_DOCUMENTATION
type: note
tags:
- quest
- note
created: '2025-01-15'
modified: '2025-01-15'
---

# TOOL_LIBRARY_DOCUMENTATION

---
title: TOOL LIBRARY DOCUMENTATION
type: note
tags:
- active
- note
created: '2025-08-14'
modified: '2025-08-14'
---

## Overview

This is a comprehensive AI tool library that provides unified access to all major AI generation tools, both local and cloud-based. All tools are installed globally on your system and can be used across any project.

### Quick Install (Recommended)
```bash
# Run the global installation script

bash scripts/install_global_tools.sh

# Reload your shell

source ~/.zshrc  # or ~/.bashrc
```
This installs:
- **ComfyUI** - Advanced image generation
- **Stable Diffusion WebUI** - User-friendly image generation
- **AnimateDiff** - Text-to-video generation
- **AudioCraft** - Music and audio generation
- **Ollama** - Local LLMs (Llama 2, Code Llama, Mistral)
- **N8N** - Workflow automation
- **PM2** - Process management

### Import in Any Project
```javascript
// Import the tool library
const { ToolLibrary } = require('./path/to/tool_library.js');

// Create an instance
const tools = new ToolLibrary({
  outputDir: './output',
  apiKeys: {
    openai: { api_key: 'your-key' },
    stability: { api_key: 'your-key' }
  }
});

// Generate an image
const image = await tools.generateImage('fantasy castle at sunset');

// Generate a video
const video = await tools.generateVideo('dragon breathing fire');

// Generate audio
const audio = await tools.generateAudio('epic battle music');

// Generate text
const text = await tools.generateText('Write a quest description');

### Quick Functions

const { quickImage, quickVideo, quickAudio, quickText } = require('./tool_library.js');

// One-line generation
const image = await quickImage('cyberpunk city');
const video = await quickVideo('magic portal opening');
const audio = await quickAudio('ambient dungeon sounds');
const text = await quickText('Generate NPC dialogue');

### Command Line Usage

# Start services

node tool_library.js start comfyui
node tool_library.js start n8n
node tool_library.js start ollama

# Check service status

node tool_library.js check

# Generate content

node tool_library.js image "fantasy landscape"
node tool_library.js video "lightning strike"
node tool_library.js audio "tavern ambience"
node tool_library.js text "describe a magical item"

## Global Commands

After installation, these commands are available globally:

### Service Launchers

comfyui          # Start ComfyUI on port 8188

sdwebui          # Start Stable Diffusion WebUI

animatediff      # Run AnimateDiff

audiocraft       # Start AudioCraft

n8n-start        # Start N8N on port 5678

ollama serve     # Start Ollama server

### Process Management

# Start all services at once

pm2 start ~/AITools/ecosystem.config.js

# Check status

pm2 status

# View logs

pm2 logs

# Stop all

pm2 stop all

### Model Management

# Download models

download-models

# Ollama models

ollama pull llama2
ollama pull codellama
ollama pull mistral
ollama run llama2  # Run interactively

## Service URLs

Once running, access services at:

- **ComfyUI**: http://localhost:8188
- **SD WebUI**: http://localhost:7860
- **N8N**: http://localhost:5678
- **Ollama API**: http://localhost:11434

### Batch Generation

const tools = new ToolLibrary();

const batch = [
  { type: 'image', prompt: 'forest path', options: { width: 1024 } },
  { type: 'video', prompt: 'waterfall', options: { frames: 24 } },
  { type: 'audio', prompt: 'birds chirping', options: { duration: 30 } },
  { type: 'text', prompt: 'describe a tavern' }
];

const results = await tools.generateBatch(batch);

### Custom Workflows with N8N

// Create a workflow
const workflow = await tools.createWorkflow('Asset Pipeline', [
  { type: 'webhook', name: 'Trigger' },
  { type: 'function', name: 'Process' },
  { type: 'http', name: 'Generate' }
]);

// Trigger it
const result = await tools.triggerWorkflow(workflow.id, {
  prompt: 'epic battle scene'

### Fallback Chain

The library automatically falls back through services:
1. **Local services** (ComfyUI, SD WebUI) - Free, fast
2. **N8N workflows** - Orchestrated pipelines
3. **Cloud APIs** (Stability, OpenAI) - High quality
4. **Error handling** - Graceful degradation

### Integration with Obsidian Vault

// In your vault scripts
const { ToolLibrary } = require('../scripts/tool_library.js');

  outputDir: '04_Resources/Assets',
  apiKeys: require('./.obsidian/api_config.json')

// Generate assets for your campaign
async function generateCampaignAssets() {
  const portraits = await tools.generateImage('heroic adventurer portrait');
  const battleMap = await tools.generateImage('dungeon battle map, top down');
  const ambience = await tools.generateAudio('cave ambience with dripping water');

  return { portraits, battleMap, ambience };
}

## File Structure

~/AITools/
├── bin/                 # Global command shortcuts

│   ├── comfyui
│   ├── sdwebui
│   ├── animatediff
│   └── download-models
├── ComfyUI/            # ComfyUI installation

├── stable-diffusion-webui/  # SD WebUI

├── animatediff-cli/    # AnimateDiff

├── audiocraft/         # AudioCraft

├── models/             # Shared models

│   ├── stable-diffusion/
│   ├── animatediff/
│   └── audiocraft/
├── workflows/          # N8N workflows

├── ecosystem.config.js # PM2 configuration

└── TOOL_LIBRARY.md    # This documentation

## Environment Variables

# Add to ~/.zshrc or ~/.bashrc

export AITOOLS_HOME="$HOME/AITools"
export PATH="$AITOOLS_HOME/bin:$PATH"

# Optional API keys

export OPENAI_API_KEY="your-key"
export STABILITY_API_KEY="your-key"
export N8N_WEBHOOK_URL="http://localhost:5678/"

### Service won't start

# Check if port is in use

lsof -i :8188  # ComfyUI

lsof -i :5678  # N8N

# Kill process using port

kill -9 $(lsof -t -i:8188)

### Out of memory

# For ComfyUI on Mac

export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

### Models not found

# Download models

# Or manually download to:

~/AITools/models/stable-diffusion/

### Complete Asset Generation Script

#!/usr/bin/env node

const { ToolLibrary } = require('./tool_library.js');
const fs = require('fs');
const path = require('path');

async function generateRPGAssets() {
  const tools = new ToolLibrary();

  // Start services
  await tools.startService('comfyui');
  await tools.startService('n8n');

  // Check they're running
  const status = await tools.checkAllServices();
  console.log('Services:', status);

  // Generate character portraits
  const characters = [
    'brave knight in shining armor',
    'mysterious wizard with glowing staff',
    'stealthy rogue in dark leather'
  ];

  for (const char of characters) {
    const image = await tools.generateImage(char, {
      width: 512,
      height: 512,
      method: 'comfyui'
    });

    const filename = char.replace(/\s+/g, '_') + '.png';
    fs.writeFileSync(path.join('./portraits', filename), image);
    console.log(`Generated: ${filename}`);

  // Generate ambient audio
  const audio = await tools.generateAudio('medieval tavern ambience', {
    duration: 60
  });

  // Generate quest text
  const quest = await tools.generateText(
    'Create a quest about retrieving a magical artifact from a dragon'
  );

  console.log('Quest:', quest);

generateRPGAssets().catch(console.error);

### Automated Workflow

// Create an automated asset pipeline

// Every time a new character is added, generate their portrait
async function onNewCharacter(characterData) {
  const { name, description } = characterData;

  // Generate portrait
  const portrait = await tools.generateImage(
    `${description}, fantasy character portrait`,
    { method: 'auto' }

  // Generate backstory
  const backstory = await tools.generateText(
    `Write a backstory for ${name}: ${description}`

  // Generate theme music
  const theme = await tools.generateAudio(
    `character theme music for ${description}`,
    { duration: 30 }

  return { portrait, backstory, theme };

## Performance Tips

1. **Use local services when possible** - Free and fast
2. **Batch operations** - Process multiple items together
3. **Cache results** - Store generated content for reuse
4. **Use PM2** - Keeps services running reliably
5. **Monitor resources** - Check GPU/CPU usage with `htop`

## License

This tool library integrates various open-source projects. Please respect their individual licenses:
- ComfyUI: GPL-3.0
- Stable Diffusion: CreativeML Open RAIL-M
- Ollama: MIT
- N8N: Fair-code

---

**Created for the TTRPG Vault Project**
*All tools installed globally for use across any project*

## Related

*Links to related content will be added here.*

## DM Notes

*Private notes for campaign integration:*
- Can be adapted to fit current story needs
- Scalable threat/reward based on party level
- Multiple entry points for different play styles
- Connections to overarching campaign themes
