#!/usr/bin/env python3
"""
Community Features Implementation - Phase 5B
Collaborative tools and social features for TTRPG vault
"""

import os
import json
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class CommunityContribution(BaseModel):
    contribution_id: str
    contributor: str
    content_type: str  # npc, location, item, story, homebrew
    title: str
    description: str
    tags: List[str]
    world: str  # Aquabyssos, Aethermoor, Both
    quality_rating: float = 0.0
    community_votes: int = 0
    created_date: str
    status: str = "pending"  # pending, approved, rejected

class CommunityTemplate(BaseModel):
    template_id: str
    template_name: str
    category: str
    fields: List[Dict[str, str]]
    example_content: str
    usage_instructions: str

class CommunityFeatures:
    def __init__(self, vault_root: str):
        self.vault_root = vault_root
        self.community_dir = os.path.join(vault_root, "10_Community")
        self.contributions: Dict[str, CommunityContribution] = {}
        self.templates: Dict[str, CommunityTemplate] = {}
        
        self._ensure_directories()
        self._initialize_templates()
    
    def _ensure_directories(self):
        dirs = [
            "10_Community/Templates",
            "10_Community/Shared", 
            "10_Community/Contributions",
            "10_Community/Reviews"
        ]
        for dir_path in dirs:
            os.makedirs(os.path.join(self.vault_root, dir_path), exist_ok=True)
    
    def _initialize_templates(self):
        """Create standard templates for community contributions"""
        
        # NPC Template
        npc_template = CommunityTemplate(
            template_id="community_npc",
            template_name="Community NPC Template",
            category="npc",
            fields=[
                {"name": "name", "type": "text", "required": "true"},
                {"name": "world", "type": "select", "options": "Aquabyssos,Aethermoor,Both"},
                {"name": "occupation", "type": "text", "required": "true"},
                {"name": "personality", "type": "tags", "required": "false"},
                {"name": "description", "type": "textarea", "required": "true"},
                {"name": "backstory", "type": "textarea", "required": "false"}
            ],
            example_content="""# Marina Tidecaller
            
---
name: Marina Tidecaller
world: Aquabyssos
occupation: Harbor Master
personality: [meticulous, protective, secretive]
type: NPC
tags: [aquabyssos, harbor, official]
---

## Description
Marina Tidecaller oversees the busy harbor district of Port Deepcurrent...

## Backstory
Born into a family of deep-sea navigators...""",
            usage_instructions="Use this template to create NPCs that fit seamlessly into the Cordelia world."
        )
        self.templates["community_npc"] = npc_template
        
        print("✅ Community templates initialized")
    
    def create_contribution_form(self, content_type: str) -> str:
        """Generate HTML form for community contributions"""
        template = self.templates.get(f"community_{content_type}")
        if not template:
            return "Template not found"
        
        form_html = f"""
        <h2>Contribute: {template.template_name}</h2>
        <form class="community-contribution-form">
        """
        
        for field in template.fields:
            if field["type"] == "text":
                form_html += f'<input name="{field["name"]}" placeholder="{field["name"].title()}" required="{field["required"]}"/>'
            elif field["type"] == "textarea":
                form_html += f'<textarea name="{field["name"]}" placeholder="{field["name"].title()}" required="{field["required"]}"></textarea>'
            elif field["type"] == "select":
                options = field["options"].split(",")
                form_html += f'<select name="{field["name"]}">'
                for option in options:
                    form_html += f'<option value="{option}">{option}</option>'
                form_html += '</select>'
        
        form_html += """
        <button type="submit">Submit Contribution</button>
        </form>
        """
        
        return form_html

def main():
    print("Initializing Community Features System...")
    community = CommunityFeatures(".")
    
    # Generate community dashboard
    dashboard = f"""# Community Features Dashboard
    
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
    
## Available Templates
    
- **NPCs**: Create characters that fit the Cordelia world
- **Locations**: Design places for both Aquabyssos and Aethermoor  
- **Items**: Craft magical and mundane objects
- **Stories**: Share campaign tales and lore
    
## Recent Contributions
    
No contributions yet. Be the first to share!
    
## Community Guidelines
    
1. All content should fit the Cordelia world setting
2. Include proper world tags (Aquabyssos/Aethermoor/Both)  
3. Follow established lore and naming conventions
4. Be respectful of other contributors
5. Provide constructive feedback on submissions
    """
    
    dashboard_path = os.path.join(".", "10_Community", "Community_Dashboard.md")
    with open(dashboard_path, 'w') as f:
        f.write(dashboard)
    
    print("✅ Community Features System operational")
    print(f"📊 Dashboard created: 10_Community/Community_Dashboard.md")

if __name__ == "__main__":
    main()
