#!/usr/bin/env python3
import os
from pathlib import Path

def process_captures():
    vault_path = Path(__file__).parent.parent.parent
    inbox = vault_path / "00_System" / "Quick_Capture_Inbox"
    
    processed = 0
    for capture_file in inbox.glob("*.md"):
        if capture_file.name == "README.md":
            continue
        
        # Simple processing - move to appropriate folder based on content
        content = capture_file.read_text()
        
        if "type: npc" in content:
            dest = vault_path / "03_People" / capture_file.name
        elif "type: location" in content:
            dest = vault_path / "02_Worldbuilding" / capture_file.name
        elif "type: quest" in content:
            dest = vault_path / "01_Adventures" / "Quests" / capture_file.name
        else:
            continue
            
        dest.parent.mkdir(parents=True, exist_ok=True)
        capture_file.rename(dest)
        processed += 1
    
    print(f"Processed {processed} quick captures")

if __name__ == "__main__":
    process_captures()
