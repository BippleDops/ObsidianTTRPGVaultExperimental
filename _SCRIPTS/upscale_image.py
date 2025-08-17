#!/usr/bin/env python3
import torch
from PIL import Image
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
import sys
import os

def upscale_image(input_path, output_path, scale=4):
    """Upscale image using Real-ESRGAN"""
    
    # Load model
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
    model_path = os.path.expanduser('~/ComfyUI/models/upscale_models/RealESRGAN_x4plus.pth')
    
    upsampler = RealESRGANer(
        scale=scale,
        model_path=model_path,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=False
    )
    
    # Load and upscale image
    img = Image.open(input_path).convert('RGB')
    output, _ = upsampler.enhance(np.array(img), outscale=scale)
    
    # Save result
    Image.fromarray(output).save(output_path)
    print(f"Upscaled: {input_path} -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python upscale.py <input> <output>")
        sys.exit(1)
    
    upscale_image(sys.argv[1], sys.argv[2])
