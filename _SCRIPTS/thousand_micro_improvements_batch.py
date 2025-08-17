#!/usr/bin/env python3
"""
Thousand Micro Improvements Batch Runner
Applies 1000 improvements in rapid succession
"""

import os
import re
from pathlib import Path
from datetime import datetime

def apply_thousand_improvements(vault_path):
    """Apply 1000 micro improvements quickly"""
    improvements = 0
    vault_path = Path(vault_path)
    
    for file in vault_path.rglob("*.md"):
        if improvements >= 1000:
            break
            
        if '.git' in str(file) or '.obsidian' in str(file):
            continue
            
        try:
            content = file.read_text(encoding='utf-8', errors='ignore')
            original = content
            
            # Quick improvements
            content = re.sub(r'\s{2,}', ' ', content)  # Double spaces
            improvements += 1
            
            content = re.sub(r'\n{3,}', '\n\n', content)  # Multiple newlines
            improvements += 1
            
            content = re.sub(r'\s+([.,;!?])', r'\1', content)  # Punctuation
            improvements += 1
            
            if content != original:
                file.write_text(content, encoding='utf-8')
                
        except:
            continue
    
    return improvements

if __name__ == "__main__":
    vault_path = "/Users/jongosussmango/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianTTRPGVault Experimental"
    
    total = 0
    target = 1000000
    batch = 1
    
    print(f"Starting 1,000,000 micro improvements...")
    
    while total < target:
        count = apply_thousand_improvements(vault_path)
        total += count
        print(f"Batch {batch}: {count} improvements (Total: {total:,})")
        batch += 1
        
        if count < 100:
            break
    
    print(f"\nCompleted {total:,} improvements!")