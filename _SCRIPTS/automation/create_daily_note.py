#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path

def create_daily_note():
    vault_path = Path(__file__).parent.parent.parent
    daily_folder = vault_path / "06_Sessions" / "Daily_Notes"
    daily_folder.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = daily_folder / f"{today}.md"
    
    if not daily_file.exists():
        content = f'''---
type: daily_note
tags: [daily, session_prep]
date: {today}
---

# Daily Note - {today}

## Today's Plans
- [ ] 

## Campaign Updates
- 

## Session Prep
- [ ] Review last session
- [ ] Prepare encounters
- [ ] Update world state

## Notes
- 
'''
        daily_file.write_text(content)
        print(f"Created daily note: {today}.md")

if __name__ == "__main__":
    create_daily_note()
