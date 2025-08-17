#!/usr/bin/env python3
"""
Automated session preparation helper
"""
from pathlib import Path
from datetime import datetime

def create_session_template():
    """Create a new session note template"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    template = f"""# Session {today}

## Campaign
[[Current Campaign]]

## Players Present
- [ ] Player 1
- [ ] Player 2
- [ ] Player 3
- [ ] Player 4

## Session Summary
### Previously
- 

### This Session
- 

### Cliffhanger
- 

## NPCs Met
- 

## Locations Visited
- 

## Items Gained
- 

## XP Earned
- 

## DM Notes
### What Went Well
- 

### To Improve
- 

### Prep for Next Session
- 

---
*Session Date: {today}*
"""
    
    session_file = Path("06_Sessions") / f"Session_{today}.md"
    session_file.parent.mkdir(parents=True, exist_ok=True)
    
    if not session_file.exists():
        with open(session_file, "w") as f:
            f.write(template)
        print(f"Created session template: {session_file}")
    else:
        print(f"Session already exists: {session_file}")
    
    return session_file

def gather_session_npcs():
    """Gather NPCs for upcoming session"""
    npcs_dir = Path("03_People")
    recent_npcs = []
    
    # Get 10 most recently modified NPCs
    npc_files = sorted(npcs_dir.rglob("*.md"), 
                      key=lambda p: p.stat().st_mtime, 
                      reverse=True)[:10]
    
    prep_file = Path("06_Sessions/Session_Prep_NPCs.md")
    with open(prep_file, "w") as f:
        f.write("# Session Prep - Recent NPCs\n\n")
        for npc in npc_files:
            f.write(f"- [[{npc.stem}]]\n")
    
    print(f"Gathered {len(npc_files)} recent NPCs for session prep")
    return prep_file

if __name__ == "__main__":
    print("Preparing for next session...")
    create_session_template()
    gather_session_npcs()
    print("Session prep complete!")
