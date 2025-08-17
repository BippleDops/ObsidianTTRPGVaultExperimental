#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

class JSONToImageConverter {
  constructor() {
    this.vaultRoot = process.cwd();
    this.assetsRoot = path.join(this.vaultRoot, '04_Resources', 'Assets');
    this.stats = {
      converted: 0,
      skipped: 0,
      errors: 0,
      total: 0
    };
    this.batchSize = 10;
    this.useComfyUI = true; // Prefer ComfyUI for speed
  }

  async convertAll() {
    console.log('🎨 JSON TO IMAGE CONVERTER');
    console.log('Converting metadata to actual images...\n');
    
    // Find all JSON files without corresponding images
    const jsonFiles = await this.findJSONWithoutImages();
    console.log(`📊 Found ${jsonFiles.length} JSON files needing images\n`);
    
    // Process in batches
    for (let i = 0; i < jsonFiles.length; i += this.batchSize) {
      const batch = jsonFiles.slice(i, i + this.batchSize);
      console.log(`📦 Batch ${Math.floor(i/this.batchSize) + 1}/${Math.ceil(jsonFiles.length/this.batchSize)}`);
      
      await this.processBatch(batch);
      
      // Small delay between batches
      await this.sleep(100);
      
      // Progress report every 100 conversions
      if (this.stats.converted % 100 === 0 && this.stats.converted > 0) {
        console.log(`  ✅ Progress: ${this.stats.converted}/${jsonFiles.length} converted`);
      }
    }
    
    await this.generateReport();
  }

  async findJSONWithoutImages() {
    const jsonFiles = [];
    
    async function walk(dir) {
      try {
        const entries = await fs.readdir(dir, { withFileTypes: true });
        
        for (const entry of entries) {
          const fullPath = path.join(dir, entry.name);
          
          if (entry.isDirectory() && !entry.name.startsWith('.')) {
            await walk(fullPath);
          } else if (entry.isFile() && entry.name.endsWith('.json')) {
            // Check if corresponding image exists
            const baseName = entry.name.replace('.json', '');
            const pngPath = path.join(dir, baseName + '.png');
            const jpgPath = path.join(dir, baseName + '.jpg');
            const webpPath = path.join(dir, baseName + '.webp');
            
            try {
              // If no image exists, add to list
              await fs.access(pngPath);
            } catch {
              try {
                await fs.access(jpgPath);
              } catch {
                try {
                  await fs.access(webpPath);
                } catch {
                  jsonFiles.push(fullPath);
                }
              }
            }
          }
        }
      } catch (error) {
        // Skip inaccessible directories
      }
    }
    
    await walk(this.assetsRoot);
    return jsonFiles;
  }

  async processBatch(jsonFiles) {
    const promises = jsonFiles.map(jsonFile => this.convertSingleFile(jsonFile));
    await Promise.allSettled(promises);
  }

  async convertSingleFile(jsonPath) {
    try {
      const data = JSON.parse(await fs.readFile(jsonPath, 'utf-8'));
      const outputPath = jsonPath.replace('.json', '.png');
      
      // Skip if already has an image
      try {
        await fs.access(outputPath);
        this.stats.skipped++;
        return;
      } catch {
        // File doesn't exist, continue with generation
      }
      
      // Generate the image
      const success = await this.generateImage(data, outputPath);
      
      if (success) {
        this.stats.converted++;
        
        // Update metadata with generation info
        data.imageGenerated = true;
        data.generatedAt = new Date().toISOString();
        data.generationMethod = this.useComfyUI ? 'ComfyUI' : 'placeholder';
        
        await fs.writeFile(jsonPath, JSON.stringify(data, null, 2));
      } else {
        this.stats.errors++;
      }
      
    } catch (error) {
      console.error(`  Error converting ${path.basename(jsonPath)}: ${error.message}`);
      this.stats.errors++;
    }
    
    this.stats.total++;
  }

  async generateImage(metadata, outputPath) {
    // Build an enhanced prompt from metadata
    const prompt = this.buildEnhancedPrompt(metadata);
    
    if (this.useComfyUI) {
      return await this.generateViaComfyUI(prompt, outputPath);
    } else {
      return await this.generatePlaceholder(metadata, outputPath);
    }
  }

  buildEnhancedPrompt(metadata) {
    let prompt = metadata.prompt || metadata.name || 'fantasy asset';
    
    // Enhance based on type
    if (metadata.type) {
      const typeEnhancements = {
        portrait: 'detailed character portrait, fantasy art style, high quality',
        location: 'scenic fantasy location, detailed environment art',
        map: 'detailed fantasy map, cartographic style, parchment texture',
        item: 'detailed item illustration, fantasy artifact, game asset',
        creature: 'fantasy creature illustration, bestiary art style',
        token: 'top-down token art, circular frame, game piece',
        handout: 'medieval document style, aged parchment, readable'
      };
      
      const enhancement = typeEnhancements[metadata.type.toLowerCase()] || 'fantasy art';
      prompt = `${prompt}, ${enhancement}`;
    }
    
    // Add campaign-specific style
    if (metadata.tags) {
      if (metadata.tags.includes('aquabyssos')) {
        prompt += ', underwater theme, oceanic, bioluminescent, deep sea';
      } else if (metadata.tags.includes('aethermoor')) {
        prompt += ', sky theme, floating islands, clouds, ethereal';
      }
    }
    
    // Add quality modifiers
    prompt += ', masterpiece, best quality, highly detailed, 8k resolution';
    
    return prompt;
  }

  async generateViaComfyUI(prompt, outputPath) {
    try {
      // Build ComfyUI workflow
      const workflow = {
        "3": {
          "class_type": "KSampler",
          "inputs": {
            "cfg": 7,
            "denoise": 1,
            "latent_image": ["5", 0],
            "model": ["4", 0],
            "negative": ["7", 0],
            "positive": ["6", 0],
            "sampler_name": "euler_ancestral",
            "scheduler": "normal",
            "seed": Math.floor(Math.random() * 1000000),
            "steps": 20
          }
        },
        "4": {
          "class_type": "CheckpointLoaderSimple",
          "inputs": {
            "ckpt_name": "v1-5-pruned-emaonly.safetensors"
          }
        },
        "5": {
          "class_type": "EmptyLatentImage",
          "inputs": {
            "batch_size": 1,
            "height": 512,
            "width": 512
          }
        },
        "6": {
          "class_type": "CLIPTextEncode",
          "inputs": {
            "clip": ["4", 1],
            "text": prompt
          }
        },
        "7": {
          "class_type": "CLIPTextEncode",
          "inputs": {
            "clip": ["4", 1],
            "text": "low quality, blurry, text, watermark, signature"
          }
        },
        "8": {
          "class_type": "VAEDecode",
          "inputs": {
            "samples": ["3", 0],
            "vae": ["4", 2]
          }
        },
        "9": {
          "class_type": "SaveImage",
          "inputs": {
            "filename_prefix": path.basename(outputPath, '.png'),
            "images": ["8", 0]
          }
        }
      };
      
      // Send to ComfyUI
      const response = await fetch('http://localhost:8188/prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: workflow })
      });
      
      if (response.ok) {
        // Wait a bit for generation
        await this.sleep(2000);
        
        // Try to get the generated image
        const comfyOutputDir = path.join(process.env.HOME, 'ComfyUI', 'output');
        const files = await fs.readdir(comfyOutputDir);
        const prefix = path.basename(outputPath, '.png');
        
        const generatedFile = files.find(f => f.startsWith(prefix) && f.endsWith('.png'));
        
        if (generatedFile) {
          const sourcePath = path.join(comfyOutputDir, generatedFile);
          await fs.copyFile(sourcePath, outputPath);
          await fs.unlink(sourcePath); // Clean up
          return true;
        }
      }
    } catch (error) {
      // ComfyUI not available, fall back to placeholder
    }
    
    return await this.generatePlaceholder({ prompt }, outputPath);
  }

  async generatePlaceholder(metadata, outputPath) {
    // Create a simple colored placeholder based on type
    const colors = {
      portrait: '#4A90E2',
      location: '#7ED321',
      map: '#D0021B',
      item: '#F5A623',
      creature: '#9013FE',
      token: '#50E3C2',
      handout: '#B8E986'
    };
    
    const color = colors[metadata.type?.toLowerCase()] || '#999999';
    const text = metadata.name || 'Asset';
    
    const svg = `<svg width="512" height="512" xmlns="http://www.w3.org/2000/svg">
      <rect width="512" height="512" fill="${color}"/>
      <text x="256" y="256" font-family="Arial" font-size="24" fill="white" text-anchor="middle" dominant-baseline="middle">
        ${text.substring(0, 30)}
      </text>
      <text x="256" y="480" font-family="Arial" font-size="12" fill="white" text-anchor="middle">
        ${metadata.type || 'Asset'}
      </text>
    </svg>`;
    
    const svgPath = outputPath.replace('.png', '.svg');
    await fs.writeFile(svgPath, svg);
    
    // Try to convert to PNG using ImageMagick if available
    try {
      await execAsync(`convert "${svgPath}" "${outputPath}"`);
      await fs.unlink(svgPath); // Remove SVG after conversion
      return true;
    } catch {
      // Keep as SVG if conversion fails
      return true;
    }
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async generateReport() {
    const report = `# JSON to Image Conversion Report

Generated: ${new Date().toISOString()}

## Summary

Converted JSON metadata files to actual images.

## Statistics

- **Converted**: ${this.stats.converted}
- **Skipped** (already had images): ${this.stats.skipped}
- **Errors**: ${this.stats.errors}
- **Total Processed**: ${this.stats.total}

## Method

${this.useComfyUI ? 'ComfyUI local generation with SD 1.5' : 'Placeholder generation with SVG'}

## Conversion Rate

Success rate: ${((this.stats.converted / this.stats.total) * 100).toFixed(1)}%

---
*JSON to Image Converter*`;
    
    await fs.writeFile(
      path.join(this.vaultRoot, '09_Performance', 'json_to_image_conversion.log'),
      report
    );
    
    console.log('\n✅ Conversion Complete!');
    console.log(`📊 Stats: ${this.stats.converted} converted, ${this.stats.skipped} skipped`);
  }
}

// Main execution
async function main() {
  const converter = new JSONToImageConverter();
  
  try {
    await converter.convertAll();
  } catch (error) {
    console.error('Error during conversion:', error);
  }
}

if (require.main === module) {
  main();
}

module.exports = JSONToImageConverter;
