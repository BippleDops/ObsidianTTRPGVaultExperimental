#!/usr/bin/env python3
"""
AI-Assisted Content Generation Scripts
Intelligent content generation using AI models for TTRPG vault
Part of Phase 4: Advanced Automation & Dynamic Systems
"""

import json
import os
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
import subprocess
import hashlib
import random
from collections import defaultdict

@dataclass
class ContentTemplate:
    template_id: str
    name: str
    content_type: str  # 'npc', 'location', 'quest', 'item', etc.
    prompt_template: str
    output_format: str
    required_inputs: List[str]
    optional_inputs: List[str]
    post_processing: List[str] = field(default_factory=list)

@dataclass
class GenerationRequest:
    template_id: str
    inputs: Dict[str, Any]
    options: Dict[str, Any] = field(default_factory=dict)

class AIContentGenerator:
    """AI-assisted content generation system."""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.config = self.load_config()
        self.templates = self.load_templates()
        self.vault_context = self.load_vault_context()
        
    def load_config(self) -> Dict:
        """Load AI generation configuration."""
        config_path = self.vault_path / "scripts" / "ai_generation_config.json"
        
        default_config = {
            "ai_providers": {
                "openai": {
                    "enabled": False,
                    "api_key_env": "OPENAI_API_KEY",
                    "model": "gpt-4",
                    "max_tokens": 2000,
                    "temperature": 0.7
                },
                "anthropic": {
                    "enabled": False,
                    "api_key_env": "ANTHROPIC_API_KEY", 
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 2000,
                    "temperature": 0.7
                },
                "local": {
                    "enabled": True,
                    "model_path": "",
                    "temperature": 0.7
                }
            },
            "generation_settings": {
                "include_vault_context": True,
                "max_context_length": 4000,
                "enable_post_processing": True,
                "auto_link_entities": True,
                "validate_output": True
            },
            "content_guidelines": {
                "tone": "immersive and detailed",
                "perspective": "third person",
                "include_sensory_details": True,
                "maintain_consistency": True,
                "cross_reference_entities": True
            },
            "output_settings": {
                "auto_save": True,
                "create_backlinks": True,
                "add_metadata": True,
                "suggest_tags": True
            }
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in loaded_config:
                        loaded_config[key] = value
                    elif isinstance(value, dict) and isinstance(loaded_config[key], dict):
                        for subkey, subvalue in value.items():
                            if subkey not in loaded_config[key]:
                                loaded_config[key][subkey] = subvalue
                return loaded_config
            except Exception as e:
                print(f"Error loading AI config: {e}")
                
        # Write default config
        config_path.parent.mkdir(exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
        
    def load_templates(self) -> Dict[str, ContentTemplate]:
        """Load content generation templates."""
        templates_path = self.vault_path / "scripts" / "generation_templates.json"
        
        default_templates = {
            "detailed_npc": ContentTemplate(
                template_id="detailed_npc",
                name="Detailed NPC",
                content_type="npc",
                prompt_template="""Create a detailed NPC for a TTRPG campaign set in the world of Cordelia, which consists of two realms: Aquabyssos (underwater kingdom) and Aethermoor (sky kingdom).

NPC Requirements:
- Name: {name}
- Faction: {faction}
- Realm: {realm}
- Role: {role}

World Context:
{world_context}

Create a comprehensive NPC profile including:
1. Physical description with realm-specific adaptations
2. Personality traits and mannerisms
3. Background and personal history
4. Current motivations and goals
5. Relationships with other faction members
6. Secrets or hidden information
7. Dialogue examples and speech patterns
8. Plot hooks for involving them in adventures

Maintain consistency with the established world lore and faction dynamics.""",
                output_format="markdown",
                required_inputs=["name", "faction", "realm"],
                optional_inputs=["role", "personality_traits", "background_hints"],
                post_processing=["add_frontmatter", "suggest_links", "add_tags"]
            ),
            
            "atmospheric_location": ContentTemplate(
                template_id="atmospheric_location",
                name="Atmospheric Location",
                content_type="location",
                prompt_template="""Create an atmospheric location description for the world of Cordelia.

Location Details:
- Name: {name}
- Type: {location_type}
- Realm: {realm}
- Importance: {importance}

World Context:
{world_context}

Create a rich location description including:
1. Visual description with sensory details
2. Atmospheric elements (sounds, smells, lighting)
3. Architectural or natural features
4. Inhabitants or creatures
5. History and significance
6. Current events or activities
7. Adventure hooks and secrets
8. Connections to other locations

Focus on immersive details that bring the location to life.""",
                output_format="markdown",
                required_inputs=["name", "location_type", "realm"],
                optional_inputs=["importance", "atmosphere", "inhabitants"],
                post_processing=["add_frontmatter", "suggest_links", "add_tags"]
            ),
            
            "faction_intrigue": ContentTemplate(
                template_id="faction_intrigue",
                name="Faction Intrigue",
                content_type="lore",
                prompt_template="""Generate faction intrigue and political maneuvering for the world of Cordelia.

Faction Focus:
- Primary Faction: {primary_faction}
- Secondary Faction: {secondary_faction}
- Conflict Type: {conflict_type}
- Stakes: {stakes}

World Context:
{world_context}

Create compelling faction intrigue including:
1. The core conflict or disagreement
2. Key players on each side
3. Hidden agendas and secret motivations
4. Recent developments or escalating tensions
5. Potential consequences of different outcomes
6. Opportunities for PC involvement
7. Moral complexity and gray areas
8. Connections to larger world events

Ensure the intrigue feels authentic and provides multiple adventure hooks.""",
                output_format="markdown",
                required_inputs=["primary_faction", "secondary_faction", "conflict_type"],
                optional_inputs=["stakes", "key_players", "recent_events"],
                post_processing=["add_frontmatter", "suggest_links", "add_tags"]
            ),
            
            "quest_generator": ContentTemplate(
                template_id="quest_generator", 
                name="Quest Generator",
                content_type="quest",
                prompt_template="""Create a compelling quest for the world of Cordelia.

Quest Parameters:
- Quest Type: {quest_type}
- Level: {level}
- Location: {location}
- Patron: {patron}

World Context:
{world_context}

Design a complete quest including:
1. Hook and initial presentation
2. Background and context
3. Primary objectives
4. Secondary objectives and complications
5. Key NPCs and their motivations
6. Potential obstacles and challenges
7. Multiple possible approaches/solutions
8. Rewards and consequences
9. Connections to campaign themes

Make the quest feel integrated into the living world of Cordelia.""",
                output_format="markdown",
                required_inputs=["quest_type", "level"],
                optional_inputs=["location", "patron", "theme", "complications"],
                post_processing=["add_frontmatter", "suggest_links", "add_tags"]
            ),
            
            "item_creator": ContentTemplate(
                template_id="item_creator",
                name="Magic Item Creator", 
                content_type="item",
                prompt_template="""Create a unique magic item for the world of Cordelia.

Item Specifications:
- Name: {name}
- Rarity: {rarity}
- Type: {item_type}
- Realm Origin: {realm}

World Context:
{world_context}

Design a complete magic item including:
1. Physical description and appearance
2. Magical properties and abilities
3. Origin story and creation
4. Lore and significance in the world
5. Mechanical effects (game stats)
6. Activation methods and limitations
7. Cultural significance or symbolism
8. Potential plot hooks involving the item

Ensure the item feels authentic to Cordelia's dual-realm nature.""",
                output_format="markdown",
                required_inputs=["name", "rarity", "item_type"],
                optional_inputs=["realm", "abilities", "origin_story"],
                post_processing=["add_frontmatter", "suggest_links", "add_tags"]
            )
        }
        
        templates = {}
        
        if templates_path.exists():
            try:
                with open(templates_path, 'r') as f:
                    template_data = json.load(f)
                    
                for template_dict in template_data.get("templates", []):
                    template = ContentTemplate(**template_dict)
                    templates[template.template_id] = template
                    
            except Exception as e:
                print(f"Error loading templates: {e}")
                
        else:
            # Create default templates file
            template_data = {
                "templates": [asdict(template) for template in default_templates.values()],
                "version": "1.0",
                "last_updated": datetime.now().isoformat()
            }
            
            templates_path.parent.mkdir(exist_ok=True)
            with open(templates_path, 'w') as f:
                json.dump(template_data, f, indent=2)
                
            templates = default_templates
            
        return templates
        
    def load_vault_context(self) -> Dict[str, Any]:
        """Load relevant vault context for AI generation."""
        context = {
            "factions": [],
            "locations": [],
            "people": [],
            "lore_summaries": [],
            "world_themes": [
                "Dual-realm existence (ocean depths vs sky heights)",
                "Pressure vs Wind magic systems", 
                "Shadow Conspiracy infiltrating government",
                "Crystal corruption affecting Queen Seraphina",
                "Deep Mother entity threatening reality",
                "Cross-realm trade and diplomatic tensions",
                "Ancient artifacts with reality-altering powers",
                "Parliamentary intrigue and corruption"
            ]
        }
        
        try:
            # Load key factions
            groups_dir = self.vault_path / "02_Worldbuilding" / "Groups"
            if groups_dir.exists():
                for group_file in groups_dir.rglob("*.md"):
                    if group_file.stat().st_size > 100:  # Skip empty files
                        context["factions"].append(group_file.stem)
                        
            # Load major locations
            places_dir = self.vault_path / "02_Worldbuilding" / "Places"
            if places_dir.exists():
                for place_file in places_dir.rglob("*.md"):
                    if place_file.stat().st_size > 100:
                        context["locations"].append(place_file.stem)
                        
            # Load important people
            people_dir = self.vault_path / "02_Worldbuilding" / "People"
            if people_dir.exists():
                for person_file in people_dir.rglob("*.md"):
                    if person_file.stat().st_size > 100:
                        context["people"].append(person_file.stem)
                        
            # Load lore summaries
            lore_dir = self.vault_path / "02_Worldbuilding" / "Lore"
            if lore_dir.exists():
                lore_files = sorted(lore_dir.rglob("*.md"), 
                                  key=lambda x: x.stat().st_size, reverse=True)
                context["lore_summaries"] = [f.stem for f in lore_files[:20]]  # Top 20 by size
                
        except Exception as e:
            print(f"Error loading vault context: {e}")
            
        return context
        
    def format_world_context(self, max_length: int = 4000) -> str:
        """Format world context for inclusion in prompts."""
        context_parts = [
            "WORLD OF CORDELIA - KEY ELEMENTS:",
            "",
            "Core Themes:",
        ]
        
        for theme in self.vault_context["world_themes"]:
            context_parts.append(f"- {theme}")
            
        if self.vault_context["factions"]:
            context_parts.extend([
                "",
                "Major Factions:",
            ])
            for faction in self.vault_context["factions"][:10]:
                context_parts.append(f"- {faction}")
                
        if self.vault_context["locations"]:
            context_parts.extend([
                "",
                "Important Locations:",
            ])
            for location in self.vault_context["locations"][:10]:
                context_parts.append(f"- {location}")
                
        if self.vault_context["people"]:
            context_parts.extend([
                "",
                "Key Figures:",
            ])
            for person in self.vault_context["people"][:8]:
                context_parts.append(f"- {person}")
                
        context_text = '\n'.join(context_parts)
        
        # Truncate if too long
        if len(context_text) > max_length:
            context_text = context_text[:max_length] + "..."
            
        return context_text
        
    def generate_content(self, request: GenerationRequest) -> Dict[str, Any]:
        """Generate content using AI."""
        template = self.templates.get(request.template_id)
        if not template:
            return {"error": f"Template {request.template_id} not found"}
            
        # Validate required inputs
        missing_inputs = []
        for required in template.required_inputs:
            if required not in request.inputs:
                missing_inputs.append(required)
                
        if missing_inputs:
            return {"error": f"Missing required inputs: {missing_inputs}"}
            
        # Prepare prompt
        prompt_vars = request.inputs.copy()
        
        # Add world context if enabled
        if self.config["generation_settings"]["include_vault_context"]:
            prompt_vars["world_context"] = self.format_world_context()
        else:
            prompt_vars["world_context"] = "Use the established world of Cordelia."
            
        try:
            prompt = template.prompt_template.format(**prompt_vars)
        except KeyError as e:
            return {"error": f"Missing template variable: {e}"}
            
        # Generate content using configured AI provider
        content = self.call_ai_provider(prompt, request.options)
        
        if not content or "error" in content:
            return content
            
        # Post-process content
        processed_content = self.post_process_content(
            content["text"], 
            template, 
            request.inputs
        )
        
        return {
            "content": processed_content,
            "metadata": {
                "template_id": template.template_id,
                "generated_at": datetime.now().isoformat(),
                "inputs": request.inputs,
                "word_count": len(processed_content.split())
            }
        }
        
    def call_ai_provider(self, prompt: str, options: Dict) -> Dict[str, Any]:
        """Call configured AI provider."""
        # This is a simplified implementation
        # In practice, you'd integrate with actual AI APIs
        
        enabled_providers = [
            provider for provider, config in self.config["ai_providers"].items()
            if config["enabled"]
        ]
        
        if not enabled_providers:
            return {"error": "No AI providers enabled"}
            
        primary_provider = enabled_providers[0]
        provider_config = self.config["ai_providers"][primary_provider]
        
        if primary_provider == "openai":
            return self.call_openai(prompt, provider_config, options)
        elif primary_provider == "anthropic":
            return self.call_anthropic(prompt, provider_config, options)
        elif primary_provider == "local":
            return self.call_local_ai(prompt, provider_config, options)
        else:
            return {"error": f"Unsupported provider: {primary_provider}"}
            
    def call_openai(self, prompt: str, config: Dict, options: Dict) -> Dict[str, Any]:
        """Call OpenAI API."""
        try:
            import openai
            
            api_key = os.getenv(config["api_key_env"])
            if not api_key:
                return {"error": f"API key not found in {config['api_key_env']}"}
                
            openai.api_key = api_key
            
            response = openai.ChatCompletion.create(
                model=config.get("model", "gpt-4"),
                messages=[
                    {"role": "system", "content": "You are an expert TTRPG content creator specializing in immersive worldbuilding."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=config.get("max_tokens", 2000),
                temperature=config.get("temperature", 0.7)
            )
            
            return {"text": response.choices[0].message.content.strip()}
            
        except ImportError:
            return {"error": "OpenAI library not installed. Run: pip install openai"}
        except Exception as e:
            return {"error": f"OpenAI API error: {e}"}
            
    def call_anthropic(self, prompt: str, config: Dict, options: Dict) -> Dict[str, Any]:
        """Call Anthropic API."""
        try:
            import anthropic
            
            api_key = os.getenv(config["api_key_env"])
            if not api_key:
                return {"error": f"API key not found in {config['api_key_env']}"}
                
            client = anthropic.Anthropic(api_key=api_key)
            
            response = client.messages.create(
                model=config.get("model", "claude-3-sonnet-20240229"),
                max_tokens=config.get("max_tokens", 2000),
                temperature=config.get("temperature", 0.7),
                messages=[{
                    "role": "user",
                    "content": f"You are an expert TTRPG content creator. {prompt}"
                }]
            )
            
            return {"text": response.content[0].text.strip()}
            
        except ImportError:
            return {"error": "Anthropic library not installed. Run: pip install anthropic"}
        except Exception as e:
            return {"error": f"Anthropic API error: {e}"}
            
    def call_local_ai(self, prompt: str, config: Dict, options: Dict) -> Dict[str, Any]:
        """Call local AI model (placeholder for offline generation)."""
        # This would integrate with local models like Ollama, GPT4All, etc.
        # For now, return a template-based response
        
        templates = {
            "npc": self.generate_fallback_npc(),
            "location": self.generate_fallback_location(),
            "quest": self.generate_fallback_quest(),
            "item": self.generate_fallback_item(),
        }
        
        # Determine content type from prompt
        content_type = "npc"  # Default
        if "location" in prompt.lower():
            content_type = "location"
        elif "quest" in prompt.lower():
            content_type = "quest"
        elif "item" in prompt.lower():
            content_type = "item"
            
        return {"text": templates.get(content_type, templates["npc"])}
        
    def generate_fallback_npc(self) -> str:
        """Generate fallback NPC content."""
        return """# Generated NPC

## Basic Information
- **Realm**: Aquabyssos
- **Faction**: Parliament of Echoes
- **Role**: Mid-level bureaucrat

## Physical Description
A mer-folk with bioluminescent markings along their arms and distinctive pressure-adaptation features. Their gills show slight scarring from years of deep-water work.

## Personality
Methodical and detail-oriented, but harbors growing concerns about recent governmental changes. Speaks in measured tones and tends to reference regulations frequently.

## Background
Rose through the ranks via diligent record-keeping and an uncanny ability to navigate parliamentary procedure. Recently assigned to investigate trade route discrepancies.

## Motivations
- Maintain order and stability
- Investigate irregularities in shipping manifests
- Protect family members from political fallout

## Secrets
Has discovered evidence of shadow faction infiltration but doesn't know who to trust with the information.

## Plot Hooks
- Needs discrete assistance investigating suspicious trade records
- Can provide access to restricted government areas
- Potential ally against shadow conspiracy if convinced
"""
        
    def generate_fallback_location(self) -> str:
        """Generate fallback location content."""
        return """# Generated Location

## Description
A mid-depth government archive facility carved into a seamount's slopes. Bioluminescent guide-lights mark the pathways between record chambers, while pressure-sealed document vaults line the walls.

## Atmosphere
The sound of water filtering through specialized barriers creates a constant, gentle susurration. Archive workers move quietly between the stacks, their movements creating brief light-trails in the dim water.

## Features
- Climate-controlled document storage chambers
- Pressure-lock reading rooms for surface-dweller visitors
- Central cataloging nexus with crystal-powered search systems
- Hidden chambers containing classified materials

## Inhabitants
- Archive specialists and researchers
- Government clerks filing reports
- Occasionally, suspicious individuals searching specific records

## Current Events
Recent break-in attempts suggest someone is seeking particular classified documents. Security has been quietly increased.

## Adventure Hooks
- Characters need to access restricted government records
- Mysterious figure offers payment for specific documents
- Evidence of shadow conspiracy might be hidden in archives
"""
        
    def generate_fallback_quest(self) -> str:
        """Generate fallback quest content."""
        return """# Generated Quest

## Quest Hook
A concerned Parliament clerk approaches the party with evidence of shipping manifest irregularities that could indicate shadow conspiracy infiltration of trade networks.

## Background
Trade routes between Aquabyssos and Aethermoor show unexplained cargo discrepancies. Certain shipments are arriving with different contents than listed, and some vessels make unscheduled stops at remote locations.

## Objectives
### Primary
- Investigate suspicious shipping activities
- Identify the source of manifest alterations
- Report findings to trustworthy authorities

### Secondary  
- Protect informant from retaliation
- Gather evidence of broader conspiracy
- Identify compromised officials

## Key NPCs
- **Clerk Meridian Currentwise**: The original informant, nervous but determined
- **Harbormaster Depths**: Either an ally or potential conspiracy member
- **Captain Shadowcurrent**: Suspicious trader with unexplained wealth

## Complications
- Multiple factions want to control information
- Evidence may implicate respected officials
- Shadow agents aware of investigation

## Rewards
- Parliamentary favor and access
- Information about conspiracy operations
- Payment from grateful trade guilds
"""
        
    def generate_fallback_item(self) -> str:
        """Generate fallback item content."""
        return """# Generated Magic Item

## Physical Description
A crystalline compass that shifts between deep blue and silver hues depending on realm proximity. Intricate pressure runes are etched along its edges.

## Properties
- **Navigation Enhancement**: Provides unerring direction to the nearest major settlement in either realm
- **Pressure Adaptation**: Grants the wearer 1 hour of pressure/altitude adaptation per day
- **Realm Detection**: Glows softly when shadow-touched individuals are within 60 feet

## Origin
Crafted by Academy of Depths researchers studying cross-realm navigation. Originally intended for diplomatic couriers traveling between realms.

## Mechanical Effects
- +2 bonus to Survival checks for navigation
- Advantage on Constitution saves against pressure/altitude effects
- Detect shadow corruption within short range

## Activation
Touching the crystal center while focusing on a specific realm or settlement.

## Lore
Several of these compasses have gone missing from Academy inventories. Some suspect shadow conspiracy involvement in the thefts.

## Plot Hooks
- Academy seeks recovery of stolen navigation devices
- Compass reveals unexpected shadow-touched individuals
- Device malfunctions near areas of reality distortion
"""
        
    def post_process_content(self, content: str, template: ContentTemplate, inputs: Dict) -> str:
        """Post-process generated content."""
        processed = content
        
        for processing_step in template.post_processing:
            if processing_step == "add_frontmatter":
                processed = self.add_frontmatter(processed, template, inputs)
            elif processing_step == "suggest_links":
                processed = self.suggest_entity_links(processed)
            elif processing_step == "add_tags":
                processed = self.add_content_tags(processed, template, inputs)
            elif processing_step == "format_markdown":
                processed = self.format_markdown(processed)
                
        return processed
        
    def add_frontmatter(self, content: str, template: ContentTemplate, inputs: Dict) -> str:
        """Add YAML frontmatter to generated content."""
        # Check if frontmatter already exists
        if content.strip().startswith('---'):
            return content
            
        frontmatter = {
            "created": datetime.now().strftime("%Y-%m-%d"),
            "status": "generated",
            "tags": ["generated", template.content_type],
            "type": template.content_type.title(),
            "updated": datetime.now().isoformat()
        }
        
        # Add realm if specified
        if "realm" in inputs:
            frontmatter["world"] = inputs["realm"]
            frontmatter["tags"].append(inputs["realm"].lower())
            
        # Add faction tag if specified
        if "faction" in inputs:
            faction_tag = inputs["faction"].lower().replace(" ", "-")
            frontmatter["tags"].append(faction_tag)
            
        # Convert to YAML
        frontmatter_yaml = "---\n"
        for key, value in frontmatter.items():
            if isinstance(value, list):
                frontmatter_yaml += f"{key}:\n"
                for item in value:
                    frontmatter_yaml += f"- {item}\n"
            else:
                frontmatter_yaml += f"{key}: '{value}'\n"
        frontmatter_yaml += "---\n\n"
        
        return frontmatter_yaml + content
        
    def suggest_entity_links(self, content: str) -> str:
        """Suggest wikilinks for known entities."""
        if not self.config["generation_settings"]["auto_link_entities"]:
            return content
            
        # Simple entity linking - in practice would use the auto_link_suggester
        known_entities = (
            self.vault_context["factions"] + 
            self.vault_context["locations"] + 
            self.vault_context["people"][:10]  # Limit to prevent over-linking
        )
        
        processed = content
        for entity in known_entities:
            if len(entity) > 3:  # Skip very short names
                # Look for the entity name not already in links
                pattern = rf'\b{re.escape(entity)}\b(?![^\[]*\]\])'
                replacement = f'[[{entity}]]'
                
                # Only replace first occurrence to avoid over-linking
                processed = re.sub(pattern, replacement, processed, count=1, flags=re.IGNORECASE)
                
        return processed
        
    def add_content_tags(self, content: str, template: ContentTemplate, inputs: Dict) -> str:
        """Add appropriate tags based on content analysis."""
        # This would analyze content and suggest relevant tags
        # For now, return content unchanged as tags are added in frontmatter
        return content
        
    def format_markdown(self, content: str) -> str:
        """Format content as proper markdown."""
        # Basic markdown formatting
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Ensure proper header spacing
            if line.strip().startswith('#'):
                if formatted_lines and formatted_lines[-1].strip():
                    formatted_lines.append('')
                formatted_lines.append(line)
                formatted_lines.append('')
            else:
                formatted_lines.append(line)
                
        return '\n'.join(formatted_lines)
        
    def save_generated_content(self, content: str, template: ContentTemplate, 
                             inputs: Dict) -> Optional[Path]:
        """Save generated content to appropriate location."""
        if not self.config["output_settings"]["auto_save"]:
            return None
            
        # Determine save location based on content type
        type_dirs = {
            "npc": "02_Worldbuilding/People",
            "location": "02_Worldbuilding/Places", 
            "quest": "01_Adventures",
            "item": "02_Worldbuilding/Items",
            "lore": "02_Worldbuilding/Lore"
        }
        
        content_type = template.content_type
        if content_type not in type_dirs:
            content_type = "lore"  # Default
            
        save_dir = self.vault_path / type_dirs[content_type]
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        if "name" in inputs:
            filename = inputs["name"]
        else:
            filename = f"Generated_{content_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        # Clean filename
        filename = re.sub(r'[^\w\s-]', '', filename).replace(' ', '_')
        filepath = save_dir / f"{filename}.md"
        
        # Avoid overwriting existing files
        counter = 1
        while filepath.exists():
            base_name = filepath.stem
            filepath = save_dir / f"{base_name}_{counter}.md"
            counter += 1
            
        # Write content
        try:
            filepath.write_text(content, encoding='utf-8')
            print(f"Generated content saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving generated content: {e}")
            return None
            
    def batch_generate(self, template_id: str, input_list: List[Dict]) -> List[Dict]:
        """Generate multiple pieces of content from a list of inputs."""
        results = []
        
        for inputs in input_list:
            request = GenerationRequest(template_id=template_id, inputs=inputs)
            result = self.generate_content(request)
            results.append(result)
            
            # Add delay to respect API limits
            if not result.get("error"):
                time.sleep(1)
                
        return results
        
    def list_templates(self) -> List[Dict]:
        """List available templates."""
        return [
            {
                "id": template.template_id,
                "name": template.name,
                "type": template.content_type,
                "required_inputs": template.required_inputs,
                "optional_inputs": template.optional_inputs
            }
            for template in self.templates.values()
        ]

def main():
    """Command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Content Generator")
    parser.add_argument("--vault-path", default=".", help="Path to vault root")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate content")
    gen_parser.add_argument("template_id", help="Template ID to use")
    gen_parser.add_argument("--input", action="append", help="Input key=value pairs")
    gen_parser.add_argument("--save", action="store_true", help="Save generated content")
    
    # List templates command
    list_parser = subparsers.add_parser("list", help="List available templates")
    
    # Batch generate command
    batch_parser = subparsers.add_parser("batch", help="Batch generate content")
    batch_parser.add_argument("template_id", help="Template ID to use")
    batch_parser.add_argument("input_file", help="JSON file with input list")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    generator = AIContentGenerator(args.vault_path)
    
    if args.command == "list":
        templates = generator.list_templates()
        
        print("Available Templates:")
        print("-" * 50)
        
        for template in templates:
            print(f"ID: {template['id']}")
            print(f"Name: {template['name']}")
            print(f"Type: {template['type']}")
            print(f"Required: {', '.join(template['required_inputs'])}")
            print(f"Optional: {', '.join(template['optional_inputs'])}")
            print()
            
    elif args.command == "generate":
        # Parse inputs
        inputs = {}
        if args.input:
            for input_str in args.input:
                if '=' in input_str:
                    key, value = input_str.split('=', 1)
                    inputs[key] = value
                    
        request = GenerationRequest(template_id=args.template_id, inputs=inputs)
        result = generator.generate_content(request)
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(result["content"])
            
            if args.save:
                template = generator.templates[args.template_id]
                filepath = generator.save_generated_content(
                    result["content"], template, inputs
                )
                if filepath:
                    print(f"\nSaved to: {filepath}")
                    
    elif args.command == "batch":
        try:
            with open(args.input_file, 'r') as f:
                input_list = json.load(f)
                
            results = generator.batch_generate(args.template_id, input_list)
            
            for i, result in enumerate(results):
                if "error" in result:
                    print(f"Item {i+1}: Error - {result['error']}")
                else:
                    print(f"Item {i+1}: Generated successfully")
                    
            print(f"\nBatch generation complete: {len(results)} items processed")
            
        except FileNotFoundError:
            print(f"Input file not found: {args.input_file}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in input file: {args.input_file}")

if __name__ == "__main__":
    main()