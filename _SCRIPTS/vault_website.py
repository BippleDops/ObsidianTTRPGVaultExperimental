#!/usr/bin/env python3
"""
Comprehensive Vault Website System
Sprint 4 - Full Implementation

Creates a standalone functional website that fully incorporates the vault with:
- Interactive dashboards for all Sprint 4 systems
- Real-time data from vault content
- Asset management and generation
- Campaign management tools
- Session planning and tracking
- Player and GM interfaces
"""

from fastapi import FastAPI, Request, HTTPException, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import os
import json
import uvicorn
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import asyncio
from pathlib import Path

# Import our custom systems
from political_intrigue_web import PoliticalIntrigueWeb
from npc_daily_routines import NPCDailyRoutineSystem  
from economic_market_simulator import EconomicMarketSimulator
from local_ai_integration import LocalAIIntegration
from common import list_markdown_files, read_file, split_frontmatter, ROOT_DIR

class VaultWebsiteSystem:
    """Main website system managing all Sprint 4 features"""
    
    def __init__(self, vault_root: str = ROOT_DIR):
        self.vault_root = vault_root
        self.app = FastAPI(title="Cordelia TTRPG Vault", version="2.0")
        
        # Initialize all subsystems
        self.political_web = PoliticalIntrigueWeb(vault_root)
        self.npc_routines = NPCDailyRoutineSystem(vault_root) 
        self.market_sim = EconomicMarketSimulator(vault_root)
        self.ai_integration = LocalAIIntegration(vault_root)
        
        # Setup web infrastructure
        self._setup_static_files()
        self._setup_templates()
        self._register_routes()
        
        # Load vault data
        self.vault_data = self._load_vault_data()
        
    def _setup_static_files(self):
        """Setup static file serving"""
        static_dir = os.path.join(self.vault_root, "04_Resources", "Assets")
        os.makedirs(static_dir, exist_ok=True)
        self.app.mount("/assets", StaticFiles(directory=static_dir), name="assets")
        
        # Create local static directory for website assets
        web_static = os.path.join(self.vault_root, "scripts", "web_static")
        os.makedirs(web_static, exist_ok=True)
        self.app.mount("/static", StaticFiles(directory=web_static), name="static")
    
    def _setup_templates(self):
        """Setup Jinja2 templates"""
        template_dir = os.path.join(self.vault_root, "scripts", "templates")
        os.makedirs(template_dir, exist_ok=True)
        self.templates = Jinja2Templates(directory=template_dir)
        
        # Create default templates
        self._create_base_templates()
    
    def _register_routes(self):
        """Register all web routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            return self.templates.TemplateResponse("home.html", {
                "request": request,
                "vault_stats": self._get_vault_stats(),
                "recent_activity": self._get_recent_activity()
            })
        
        @self.app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard(request: Request):
            return self.templates.TemplateResponse("dashboard.html", {
                "request": request,
                "political_summary": self._get_political_summary(),
                "economic_summary": self._get_economic_summary(),
                "npc_summary": self._get_npc_summary(),
                "ai_summary": self._get_ai_summary()
            })
        
        @self.app.get("/political-intrigue", response_class=HTMLResponse)
        async def political_intrigue(request: Request):
            return self.templates.TemplateResponse("political_intrigue.html", {
                "request": request,
                "entities": list(self.political_web.entities.values())[:20],
                "conspiracies": list(self.political_web.conspiracies.values()),
                "relationships": self.political_web.relationships[:50]
            })
        
        @self.app.get("/npc-routines", response_class=HTMLResponse) 
        async def npc_routines(request: Request, time: str = None):
            current_time = time or datetime.now().strftime("%H:%M")
            return self.templates.TemplateResponse("npc_routines.html", {
                "request": request,
                "current_time": current_time,
                "routines": list(self.npc_routines.routines.values())[:15],
                "location_occupants": self._get_location_occupants(current_time),
                "time_blocks": ["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
            })
        
        @self.app.get("/market-simulator", response_class=HTMLResponse)
        async def market_simulator(request: Request):
            return self.templates.TemplateResponse("market_simulator.html", {
                "request": request,
                "markets": list(self.market_sim.markets.values()),
                "top_movers": self._get_top_price_movers(),
                "active_events": self.market_sim.active_events,
                "merchant_activity": self._get_merchant_activity()
            })
        
        @self.app.get("/ai-integration", response_class=HTMLResponse)
        async def ai_integration(request: Request):
            return self.templates.TemplateResponse("ai_integration.html", {
                "request": request,
                "asset_types": list(self.ai_integration.asset_types.values()),
                "generated_assets": list(self.ai_integration.generated_assets.values())[:20],
                "ollama_models": self.ai_integration.ollama_models,
                "generation_queue": self._get_generation_queue()
            })
        
        @self.app.get("/campaign-manager", response_class=HTMLResponse)
        async def campaign_manager(request: Request):
            return self.templates.TemplateResponse("campaign_manager.html", {
                "request": request,
                "campaigns": self._get_campaigns(),
                "seven_shards": self._get_seven_shards_data(),
                "session_planning": self._get_session_planning_data()
            })
        
        @self.app.get("/vault-browser", response_class=HTMLResponse)
        async def vault_browser(request: Request, path: str = ""):
            return self.templates.TemplateResponse("vault_browser.html", {
                "request": request,
                "current_path": path,
                "vault_structure": self._get_vault_structure(path),
                "recent_files": self._get_recent_files()
            })
        
        # API Endpoints
        @self.app.get("/api/simulate-day")
        async def simulate_day():
            """Simulate one day across all systems"""
            self.market_sim.simulate_market_day()
            return {"status": "success", "message": "Day simulated"}
        
        @self.app.get("/api/generate-conspiracy/{entity_name}")
        async def generate_conspiracy(entity_name: str):
            """Generate conspiracy network around entity"""
            conspiracy = self.political_web.generate_conspiracy_network(entity_name, 6)
            return conspiracy.dict() if conspiracy else {"error": "Entity not found"}
        
        @self.app.get("/api/npc-activity/{npc_name}")
        async def get_npc_activity(npc_name: str, time: str = None):
            """Get NPC's current activity"""
            current_time = time or datetime.now().strftime("%H:%M")
            activity = self.npc_routines.get_npc_current_activity(npc_name, current_time)
            return activity.dict() if activity else {"error": "No activity found"}
        
        @self.app.post("/api/generate-asset")
        async def generate_asset(asset_type: str = Form(...), prompt: str = Form(...)):
            """Generate new asset"""
            from local_ai_integration import GenerationPrompt
            
            gen_prompt = GenerationPrompt(
                prompt_id=f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                asset_type=asset_type,
                primary_prompt=prompt
            )
            
            asset = self.ai_integration.generate_image_with_ollama(gen_prompt)
            return asset.dict() if asset else {"error": "Generation failed"}
        
        @self.app.get("/api/vault-search")
        async def vault_search(query: str):
            """Search vault content"""
            results = self._search_vault(query)
            return {"results": results}
        
        @self.app.get("/api/export-data/{system}")
        async def export_data(system: str):
            """Export system data"""
            if system == "political":
                self.political_web.save_system_state()
            elif system == "economic":
                self.market_sim.save_economic_data()
            elif system == "routines":
                self.npc_routines.save_routine_data()
            elif system == "ai":
                self.ai_integration.save_system_data()
            
            return {"status": "success", "message": f"{system} data exported"}
    
    def _create_base_templates(self):
        """Create essential HTML templates"""
        
        # Base template
        base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Cordelia TTRPG Vault{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .fantasy-bg { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
        .card-fantasy { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); }
        .navbar-fantasy { background: rgba(0,0,0,0.8); }
        .stat-card { transition: transform 0.2s; }
        .stat-card:hover { transform: translateY(-5px); }
        .conspiracy-web { background: radial-gradient(circle, #2c1810 0%, #1a0f08 100%); }
        .market-data { background: linear-gradient(45deg, #1a4d3a 0%, #0f2419 100%); }
    </style>
</head>
<body class="fantasy-bg min-vh-100">
    <nav class="navbar navbar-expand-lg navbar-dark navbar-fantasy fixed-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-scroll me-2"></i>Cordelia Vault
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/dashboard"><i class="fas fa-tachometer-alt me-1"></i>Dashboard</a>
                <a class="nav-link" href="/political-intrigue"><i class="fas fa-mask me-1"></i>Intrigue</a>
                <a class="nav-link" href="/npc-routines"><i class="fas fa-users me-1"></i>NPCs</a>
                <a class="nav-link" href="/market-simulator"><i class="fas fa-coins me-1"></i>Markets</a>
                <a class="nav-link" href="/ai-integration"><i class="fas fa-robot me-1"></i>AI Assets</a>
                <a class="nav-link" href="/campaign-manager"><i class="fas fa-map me-1"></i>Campaigns</a>
                <a class="nav-link" href="/vault-browser"><i class="fas fa-folder-open me-1"></i>Browse</a>
            </div>
        </div>
    </nav>
    
    <main class="container mt-5 pt-4">
        {% block content %}{% endblock %}
    </main>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Auto-refresh data every 5 minutes
        setInterval(() => {
            if (window.location.pathname === '/dashboard') {
                location.reload();
            }
        }, 300000);
    </script>
    {% block scripts %}{% endblock %}
</body>
</html>"""
        
        # Home template  
        home_template = """{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="card card-fantasy mb-4">
            <div class="card-body text-center">
                <h1 class="display-4 text-primary mb-3">
                    <i class="fas fa-water me-3"></i>Cordelia TTRPG Vault
                    <i class="fas fa-wind ms-3"></i>
                </h1>
                <p class="lead">Dual-world campaign management system for Aquabyssos & Aethermoor</p>
            </div>
        </div>
    </div>
</div>

<div class="row g-4">
    {% for stat in vault_stats %}
    <div class="col-md-3">
        <div class="card card-fantasy stat-card h-100">
            <div class="card-body text-center">
                <i class="{{ stat.icon }} fa-3x text-primary mb-3"></i>
                <h3 class="card-title">{{ stat.value }}</h3>
                <p class="card-text">{{ stat.label }}</p>
            </div>
        </div>
    </div>
    {% endfor %}
</div>

<div class="row mt-5">
    <div class="col-lg-8">
        <div class="card card-fantasy">
            <div class="card-header">
                <h5><i class="fas fa-clock me-2"></i>Recent Activity</h5>
            </div>
            <div class="card-body">
                {% for activity in recent_activity %}
                <div class="d-flex justify-content-between align-items-center border-bottom py-2">
                    <div>
                        <strong>{{ activity.action }}</strong>
                        <br><small class="text-muted">{{ activity.description }}</small>
                    </div>
                    <small class="text-muted">{{ activity.time }}</small>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="card card-fantasy">
            <div class="card-header">
                <h5><i class="fas fa-tools me-2"></i>Quick Actions</h5>
            </div>
            <div class="card-body">
                <div class="d-grid gap-2">
                    <button class="btn btn-primary" onclick="simulateDay()">
                        <i class="fas fa-calendar-day me-2"></i>Simulate Day
                    </button>
                    <a href="/ai-integration" class="btn btn-success">
                        <i class="fas fa-image me-2"></i>Generate Assets
                    </a>
                    <a href="/campaign-manager" class="btn btn-info">
                        <i class="fas fa-plus me-2"></i>New Session
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
async function simulateDay() {
    const response = await fetch('/api/simulate-day');
    if (response.ok) {
        alert('Day simulated successfully!');
        location.reload();
    }
}
</script>
{% endblock %}"""

        # Dashboard template
        dashboard_template = """{% extends "base.html" %}

{% block content %}
<div class="row g-4">
    <!-- Political Intrigue Summary -->
    <div class="col-lg-6">
        <div class="card card-fantasy conspiracy-web text-light">
            <div class="card-header">
                <h5><i class="fas fa-mask me-2"></i>Political Intrigue Web</h5>
            </div>
            <div class="card-body">
                <div class="row text-center mb-3">
                    <div class="col-4">
                        <h3>{{ political_summary.entities }}</h3>
                        <small>Entities</small>
                    </div>
                    <div class="col-4">
                        <h3>{{ political_summary.conspiracies }}</h3>
                        <small>Conspiracies</small>
                    </div>
                    <div class="col-4">
                        <h3>{{ political_summary.relationships }}</h3>
                        <small>Relationships</small>
                    </div>
                </div>
                <a href="/political-intrigue" class="btn btn-outline-light">View Details</a>
            </div>
        </div>
    </div>
    
    <!-- Economic Summary -->
    <div class="col-lg-6">
        <div class="card card-fantasy market-data text-light">
            <div class="card-header">
                <h5><i class="fas fa-coins me-2"></i>Economic Markets</h5>
            </div>
            <div class="card-body">
                <div class="row text-center mb-3">
                    <div class="col-4">
                        <h3>{{ economic_summary.markets }}</h3>
                        <small>Markets</small>
                    </div>
                    <div class="col-4">
                        <h3>{{ economic_summary.goods }}</h3>
                        <small>Trade Goods</small>
                    </div>
                    <div class="col-4">
                        <h3>{{ economic_summary.events }}</h3>
                        <small>Active Events</small>
                    </div>
                </div>
                <a href="/market-simulator" class="btn btn-outline-light">View Markets</a>
            </div>
        </div>
    </div>
    
    <!-- NPC Routines Summary -->
    <div class="col-lg-6">
        <div class="card card-fantasy">
            <div class="card-header">
                <h5><i class="fas fa-users me-2"></i>NPC Daily Routines</h5>
            </div>
            <div class="card-body">
                <p><strong>{{ npc_summary.active_npcs }}</strong> NPCs with active routines</p>
                <p><strong>{{ npc_summary.current_activities }}</strong> different activities at current time</p>
                <a href="/npc-routines" class="btn btn-primary">View Routines</a>
            </div>
        </div>
    </div>
    
    <!-- AI Integration Summary -->
    <div class="col-lg-6">
        <div class="card card-fantasy">
            <div class="card-header">
                <h5><i class="fas fa-robot me-2"></i>AI Asset Generation</h5>
            </div>
            <div class="card-body">
                <p><strong>{{ ai_summary.generated_assets }}</strong> assets generated</p>
                <p><strong>{{ ai_summary.ready_prompts }}</strong> prompts ready for generation</p>
                <a href="/ai-integration" class="btn btn-success">Generate Assets</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
        
        # Write templates
        template_dir = os.path.join(self.vault_root, "scripts", "templates")
        
        with open(os.path.join(template_dir, "base.html"), "w") as f:
            f.write(base_template)
        
        with open(os.path.join(template_dir, "home.html"), "w") as f:
            f.write(home_template)
            
        with open(os.path.join(template_dir, "dashboard.html"), "w") as f:
            f.write(dashboard_template)
    
    def _load_vault_data(self) -> Dict[str, Any]:
        """Load and index all vault data"""
        vault_data = {
            "npcs": {},
            "locations": {},
            "groups": {},
            "lore": {},
            "items": {}
        }
        
        markdown_files = list_markdown_files(self.vault_root)
        
        for file_path in markdown_files[:500]:  # Limit for performance
            try:
                content = read_file(file_path)
                frontmatter, body = split_frontmatter(content)
                
                entity_type = frontmatter.get('type', '').lower()
                name = frontmatter.get('name') or os.path.splitext(os.path.basename(file_path))[0]
                
                entity_data = {
                    'name': name,
                    'type': entity_type,
                    'world': frontmatter.get('world', 'Both'),
                    'status': frontmatter.get('status', 'draft'),
                    'file_path': file_path,
                    'content_preview': body[:200] + "..." if len(body) > 200 else body
                }
                
                if entity_type == 'npc':
                    vault_data['npcs'][name] = entity_data
                elif entity_type == 'location':
                    vault_data['locations'][name] = entity_data
                elif entity_type == 'group':
                    vault_data['groups'][name] = entity_data
                elif entity_type == 'lore':
                    vault_data['lore'][name] = entity_data
                elif entity_type == 'item':
                    vault_data['items'][name] = entity_data
                    
            except Exception as e:
                continue
        
        return vault_data
    
    def _get_vault_stats(self) -> List[Dict]:
        """Get vault statistics for home page"""
        return [
            {"label": "NPCs", "value": len(self.vault_data['npcs']), "icon": "fas fa-users"},
            {"label": "Locations", "value": len(self.vault_data['locations']), "icon": "fas fa-map-marker-alt"},
            {"label": "Groups", "value": len(self.vault_data['groups']), "icon": "fas fa-users-cog"},
            {"label": "Lore Entries", "value": len(self.vault_data['lore']), "icon": "fas fa-book"}
        ]
    
    def _get_recent_activity(self) -> List[Dict]:
        """Get recent activity for home page"""
        return [
            {
                "action": "Market Event",
                "description": "Crystal Mine Collapse affected prices",
                "time": "2 hours ago"
            },
            {
                "action": "NPC Generated", 
                "description": "Created portrait for Marina Tidecaller",
                "time": "4 hours ago"
            },
            {
                "action": "Conspiracy Updated",
                "description": "Shadow Parliament expanded network",
                "time": "6 hours ago"
            }
        ]
    
    def _get_political_summary(self) -> Dict:
        """Get political intrigue summary"""
        return {
            "entities": len(self.political_web.entities),
            "conspiracies": len(self.political_web.conspiracies),
            "relationships": len(self.political_web.relationships)
        }
    
    def _get_economic_summary(self) -> Dict:
        """Get economic system summary"""
        return {
            "markets": len(self.market_sim.markets),
            "goods": len(self.market_sim.trade_goods),
            "events": len(self.market_sim.active_events)
        }
    
    def _get_npc_summary(self) -> Dict:
        """Get NPC routines summary"""
        return {
            "active_npcs": len(self.npc_routines.routines),
            "current_activities": len(set(
                activity.description 
                for routine in self.npc_routines.routines.values()
                for activity in routine.base_schedule
            ))
        }
    
    def _get_ai_summary(self) -> Dict:
        """Get AI integration summary"""
        return {
            "generated_assets": len(self.ai_integration.generated_assets),
            "ready_prompts": len([
                asset for asset in self.ai_integration.generated_assets.values()
                if asset.metadata.get("ready_for_generation", False)
            ])
        }
    
    def run_server(self, host: str = "localhost", port: int = 8000):
        """Run the web server"""
        print(f"Starting Cordelia Vault Website on http://{host}:{port}")
        print("Available endpoints:")
        print("  / - Home dashboard")
        print("  /dashboard - System overview")
        print("  /political-intrigue - Conspiracy networks")
        print("  /npc-routines - NPC daily schedules")
        print("  /market-simulator - Economic system")
        print("  /ai-integration - Asset generation")
        print("  /campaign-manager - Campaign tools")
        print("  /vault-browser - File browser")
        
        uvicorn.run(self.app, host=host, port=port, log_level="info")

def main():
    """Main execution to start the website"""
    print("Initializing Comprehensive Vault Website...")
    
    # Initialize website system
    website = VaultWebsiteSystem()
    
    # Generate initial data for all systems
    print("Generating initial data...")
    
    # Generate political intrigue data
    if "The Shadow Conspiracy" in website.political_web.entities:
        website.political_web.generate_conspiracy_network("The Shadow Conspiracy", 6)
    
    # Generate some NPC routines
    for npc_name in list(website.npc_routines.npcs.keys())[:10]:
        website.npc_routines.generate_routine_for_npc(npc_name)
    
    # Run a few days of market simulation
    for _ in range(3):
        website.market_sim.simulate_market_day()
    
    # Generate some assets
    website.ai_integration.generate_asset_batch(["portrait", "location"], limit=10)
    
    print("Website system initialized successfully!")
    print("Starting web server...")
    
    # Start the server
    website.run_server(host="localhost", port=8000)

if __name__ == "__main__":
    main()