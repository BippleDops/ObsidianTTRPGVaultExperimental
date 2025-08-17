#!/usr/bin/env python3
"""
Economic Market Simulator
Sprint 4 - Procedural Power Feature #3

Dynamic pricing with supply/demand modeling for living world economy.
Creates realistic trade flows, market fluctuations, and economic events.

Features:
- Dynamic pricing based on supply/demand
- Trade route simulation
- Market event impact modeling
- Cross-world economic relationships
- Resource scarcity tracking
- NPC merchant behavior
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field, validator
import math

from common import (
    list_markdown_files, read_file, write_file, split_frontmatter,
    build_frontmatter, merge_frontmatter, ROOT_DIR, ensure_dirs
)

class ResourceType(Enum):
    FOOD = "food"
    CRAFTING_MATERIALS = "crafting_materials" 
    LUXURY_GOODS = "luxury_goods"
    MAGICAL_COMPONENTS = "magical_components"
    WEAPONS_ARMOR = "weapons_armor"
    INFORMATION = "information"
    SERVICES = "services"
    TRANSPORTATION = "transportation"
    REAL_ESTATE = "real_estate"
    CONTRABAND = "contraband"

class MarketCondition(Enum):
    CRASHED = "crashed"      # Prices 20-40% of baseline
    DEPRESSED = "depressed"  # Prices 40-70% of baseline
    NORMAL = "normal"        # Prices 80-120% of baseline
    INFLATED = "inflated"    # Prices 120-180% of baseline
    BUBBLE = "bubble"        # Prices 180-300% of baseline

class TradeGood(BaseModel):
    """A tradeable commodity in the market"""
    name: str = Field(..., description="Name of the trade good")
    category: ResourceType
    base_price: float = Field(..., description="Base price in gold pieces")
    current_price: float = Field(..., description="Current market price")
    supply_level: int = Field(default=50, description="Current supply (0-100)")
    demand_level: int = Field(default=50, description="Current demand (0-100)")
    volatility: float = Field(default=0.1, description="Price volatility factor")
    world_origin: str = Field(default="Both", description="Primary production world")
    seasonal_modifier: float = Field(default=1.0, description="Seasonal price adjustment")
    quality_grades: Dict[str, float] = Field(default_factory=dict, description="Quality tiers and multipliers")
    trade_restrictions: List[str] = Field(default_factory=list, description="Legal/political restrictions")
    
    @validator('supply_level', 'demand_level')
    def validate_levels(cls, v):
        return max(0, min(100, v))

class Market(BaseModel):
    """A marketplace in the world"""
    name: str = Field(..., description="Market name")
    location: str = Field(..., description="Geographic location")
    world: str = Field(..., description="Aquabyssos, Aethermoor, or Both")
    size: int = Field(default=5, description="Market size (1-10)")
    specializations: List[ResourceType] = Field(default_factory=list, description="Market specialties")
    trade_goods: Dict[str, TradeGood] = Field(default_factory=dict, description="Available goods")
    active_merchants: List[str] = Field(default_factory=list, description="Merchant NPCs present")
    market_condition: MarketCondition = Field(default=MarketCondition.NORMAL)
    transportation_connections: List[str] = Field(default_factory=list, description="Connected markets")
    security_level: int = Field(default=5, description="Market security (1-10)")
    tax_rate: float = Field(default=0.05, description="Transaction tax rate")

class TradeRoute(BaseModel):
    """A connection between markets"""
    name: str = Field(..., description="Route name")
    origin_market: str = Field(..., description="Starting market")
    destination_market: str = Field(..., description="Ending market")
    distance: int = Field(default=100, description="Distance in miles")
    travel_time: int = Field(default=7, description="Travel time in days")
    safety_level: int = Field(default=5, description="Route safety (1-10)")
    transportation_cost: float = Field(default=10.0, description="Cost per unit shipped")
    active_routes: int = Field(default=1, description="Number of active trade runs")
    seasonal_accessibility: Dict[str, bool] = Field(default_factory=dict, description="Seasonal route availability")

class MarketEvent(BaseModel):
    """An event affecting markets"""
    event_id: str = Field(..., description="Unique event identifier")
    name: str = Field(..., description="Event name")
    description: str = Field(..., description="Event description")
    affected_markets: List[str] = Field(default_factory=list, description="Markets impacted")
    affected_goods: List[str] = Field(default_factory=list, description="Goods impacted")
    supply_impact: Dict[str, int] = Field(default_factory=dict, description="Supply changes per good")
    demand_impact: Dict[str, int] = Field(default_factory=dict, description="Demand changes per good")
    duration_days: int = Field(default=30, description="Event duration")
    severity: int = Field(default=5, description="Event severity (1-10)")
    start_date: str = Field(..., description="Event start date")

class MerchantNPC(BaseModel):
    """An NPC merchant operating in the economy"""
    name: str = Field(..., description="Merchant name")
    specialization: ResourceType
    home_market: str = Field(..., description="Primary market")
    trade_routes: List[str] = Field(default_factory=list, description="Known routes")
    capital: float = Field(default=1000.0, description="Available capital")
    inventory: Dict[str, int] = Field(default_factory=dict, description="Current stock")
    reputation: int = Field(default=5, description="Merchant reputation (1-10)")
    risk_tolerance: float = Field(default=0.5, description="Willingness to take risks")
    ai_behavior: str = Field(default="balanced", description="Trading behavior pattern")

class EconomicMarketSimulator:
    """Main system for simulating dynamic markets and trade"""
    
    def __init__(self, vault_root: str = ROOT_DIR):
        self.vault_root = vault_root
        self.markets: Dict[str, Market] = {}
        self.trade_goods: Dict[str, TradeGood] = {}
        self.trade_routes: Dict[str, TradeRoute] = {}
        self.active_events: List[MarketEvent] = []
        self.merchant_npcs: Dict[str, MerchantNPC] = {}
        self.price_history: Dict[str, List[Tuple[str, float]]] = {}
        
        # Initialize the economy
        self._initialize_base_economy()
        self._scan_vault_trade_data()
        self._load_persisted_data()
    
    def _initialize_base_economy(self):
        """Set up foundational trade goods and markets"""
        
        # Initialize core trade goods
        base_goods = {
            # Food & Sustenance
            "Deep Kelp": TradeGood(
                name="Deep Kelp",
                category=ResourceType.FOOD,
                base_price=2.0,
                current_price=2.0,
                world_origin="Aquabyssos",
                quality_grades={"Common": 1.0, "Prime": 1.5, "Royal": 3.0}
            ),
            "Sky Fruit": TradeGood(
                name="Sky Fruit",
                category=ResourceType.FOOD,
                base_price=8.0,
                current_price=8.0,
                world_origin="Aethermoor",
                seasonal_modifier=1.0,
                quality_grades={"Common": 1.0, "Sweet": 1.3, "Golden": 2.5}
            ),
            
            # Crafting Materials
            "Pressure Crystals": TradeGood(
                name="Pressure Crystals",
                category=ResourceType.CRAFTING_MATERIALS,
                base_price=50.0,
                current_price=50.0,
                world_origin="Aquabyssos",
                volatility=0.3,
                quality_grades={"Flawed": 0.7, "Clear": 1.0, "Perfect": 2.0}
            ),
            "Wind Crystals": TradeGood(
                name="Wind Crystals", 
                category=ResourceType.CRAFTING_MATERIALS,
                base_price=45.0,
                current_price=45.0,
                world_origin="Aethermoor",
                volatility=0.25
            ),
            
            # Magical Components
            "Memory Pearls": TradeGood(
                name="Memory Pearls",
                category=ResourceType.MAGICAL_COMPONENTS,
                base_price=200.0,
                current_price=200.0,
                world_origin="Aquabyssos",
                trade_restrictions=["Controlled Substance", "Parliament License Required"],
                volatility=0.4
            ),
            "Void Essence": TradeGood(
                name="Void Essence",
                category=ResourceType.MAGICAL_COMPONENTS,
                base_price=500.0,
                current_price=500.0,
                world_origin="Both",
                trade_restrictions=["Highly Restricted", "Deep Mother Cult Only"],
                volatility=0.6
            ),
            
            # Information & Services
            "Trade Intelligence": TradeGood(
                name="Trade Intelligence",
                category=ResourceType.INFORMATION,
                base_price=100.0,
                current_price=100.0,
                world_origin="Both",
                quality_grades={"Rumors": 0.3, "Verified": 1.0, "Exclusive": 3.0}
            ),
            
            # Contraband
            "Shadow Artifacts": TradeGood(
                name="Shadow Artifacts",
                category=ResourceType.CONTRABAND,
                base_price=300.0,
                current_price=300.0,
                world_origin="Aquabyssos", 
                trade_restrictions=["Illegal", "Shadow Conspiracy Source"],
                volatility=0.8
            )
        }
        
        # Add goods to system
        for name, good in base_goods.items():
            self.trade_goods[name] = good
        
        # Initialize core markets
        core_markets = {
            "Aquabyssos Grand Market": Market(
                name="Aquabyssos Grand Market",
                location="Abyssos Prime",
                world="Aquabyssos", 
                size=10,
                specializations=[ResourceType.MAGICAL_COMPONENTS, ResourceType.CRAFTING_MATERIALS],
                active_merchants=["Marina Tidecaller", "Depth Merchant Guild"]
            ),
            "Aethermoor Crystal Exchange": Market(
                name="Aethermoor Crystal Exchange",
                location="Luminspire",
                world="Aethermoor",
                size=9,
                specializations=[ResourceType.CRAFTING_MATERIALS, ResourceType.LUXURY_GOODS],
                active_merchants=["Crystal Syndicate", "Wind Traders"]
            ),
            "Shadowhaven Black Market": Market(
                name="Shadowhaven Black Market",
                location="Hidden District",
                world="Aquabyssos",
                size=6,
                specializations=[ResourceType.CONTRABAND, ResourceType.INFORMATION],
                security_level=2,
                tax_rate=0.0,
                active_merchants=["Shadow Brokers", "Information Dealers"]
            )
        }
        
        # Populate markets with goods
        for market_name, market in core_markets.items():
            market.trade_goods = {}
            for good_name, good in self.trade_goods.items():
                if good.world_origin == market.world or good.world_origin == "Both" or market.world == "Both":
                    # Add some market-specific price variation
                    market_good = good.copy()
                    market_good.current_price *= random.uniform(0.9, 1.1)
                    market.trade_goods[good_name] = market_good
            
            self.markets[market_name] = market
    
    def _scan_vault_trade_data(self):
        """Scan vault for existing trade-related content"""
        markdown_files = list_markdown_files(self.vault_root)
        
        for file_path in markdown_files:
            try:
                content = read_file(file_path)
                frontmatter, body = split_frontmatter(content)
                
                # Look for merchant NPCs
                if frontmatter.get('type') == 'NPC':
                    if self._is_merchant_npc(frontmatter, body):
                        merchant = self._extract_merchant_data(file_path, frontmatter, body)
                        if merchant:
                            self.merchant_npcs[merchant.name] = merchant
                
                # Look for trade goods in item files
                if frontmatter.get('type') == 'Item':
                    trade_good = self._extract_trade_good(frontmatter, body)
                    if trade_good:
                        self.trade_goods[trade_good.name] = trade_good
                        
            except Exception as e:
                continue  # Skip malformed files
    
    def _is_merchant_npc(self, frontmatter: Dict, body: str) -> bool:
        """Check if NPC is a merchant/trader"""
        indicators = ['merchant', 'trader', 'seller', 'buyer', 'commerce', 'trade', 'goods', 'market']
        
        text_to_check = (
            str(frontmatter.get('name', '')) + ' ' +
            str(frontmatter.get('occupation', '')) + ' ' +
            body.lower()
        ).lower()
        
        return any(indicator in text_to_check for indicator in indicators)
    
    def _extract_merchant_data(self, file_path: str, frontmatter: Dict, body: str) -> Optional[MerchantNPC]:
        """Extract merchant NPC data from vault file"""
        name = frontmatter.get('name') or os.path.splitext(os.path.basename(file_path))[0]
        
        # Determine specialization
        specialization = ResourceType.CRAFTING_MATERIALS  # Default
        body_lower = body.lower()
        
        if any(term in body_lower for term in ['food', 'kelp', 'fruit', 'meal']):
            specialization = ResourceType.FOOD
        elif any(term in body_lower for term in ['crystal', 'gem', 'materials']):
            specialization = ResourceType.CRAFTING_MATERIALS
        elif any(term in body_lower for term in ['magic', 'component', 'essence']):
            specialization = ResourceType.MAGICAL_COMPONENTS
        elif any(term in body_lower for term in ['weapon', 'armor', 'blade']):
            specialization = ResourceType.WEAPONS_ARMOR
        elif any(term in body_lower for term in ['information', 'secret', 'intelligence']):
            specialization = ResourceType.INFORMATION
        
        # Determine home market
        world = frontmatter.get('world', 'Both')
        home_market = "Aquabyssos Grand Market" if world == "Aquabyssos" else "Aethermoor Crystal Exchange"
        
        return MerchantNPC(
            name=name,
            specialization=specialization,
            home_market=home_market,
            capital=random.uniform(500.0, 5000.0),
            reputation=random.randint(3, 8),
            risk_tolerance=random.uniform(0.2, 0.8)
        )
    
    def simulate_market_day(self):
        """Simulate one day of market activity"""
        
        # Update supply and demand based on various factors
        self._update_supply_demand()
        
        # Process merchant activities
        self._process_merchant_behaviors()
        
        # Apply market events
        self._apply_active_events()
        
        # Update prices based on supply/demand
        self._update_prices()
        
        # Record price history
        self._record_price_history()
        
        # Random chance of new market events
        if random.random() < 0.05:  # 5% chance per day
            self._generate_random_event()
    
    def _update_supply_demand(self):
        """Update supply and demand levels for all goods"""
        
        for market in self.markets.values():
            for good_name, good in market.trade_goods.items():
                
                # Natural supply/demand drift
                supply_change = random.randint(-3, 3)
                demand_change = random.randint(-3, 3)
                
                # Seasonal effects
                if good.seasonal_modifier != 1.0:
                    current_month = datetime.now().month
                    if good.world_origin == "Aethermoor" and current_month in [6, 7, 8]:  # Summer sky fruits
                        supply_change += 10
                    elif good.world_origin == "Aquabyssos" and current_month in [12, 1, 2]:  # Winter deep kelp
                        supply_change += 5
                
                # Apply changes
                good.supply_level = max(0, min(100, good.supply_level + supply_change))
                good.demand_level = max(0, min(100, good.demand_level + demand_change))
                
                # Update market condition based on aggregate supply/demand
                avg_supply = sum(g.supply_level for g in market.trade_goods.values()) / len(market.trade_goods)
                avg_demand = sum(g.demand_level for g in market.trade_goods.values()) / len(market.trade_goods)
                
                ratio = avg_demand / max(avg_supply, 1)
                
                if ratio < 0.5:
                    market.market_condition = MarketCondition.CRASHED
                elif ratio < 0.7:
                    market.market_condition = MarketCondition.DEPRESSED
                elif ratio < 1.3:
                    market.market_condition = MarketCondition.NORMAL
                elif ratio < 1.8:
                    market.market_condition = MarketCondition.INFLATED
                else:
                    market.market_condition = MarketCondition.BUBBLE
    
    def _update_prices(self):
        """Update current prices based on supply and demand"""
        
        for market in self.markets.values():
            for good_name, good in market.trade_goods.items():
                
                # Calculate supply/demand ratio
                demand_ratio = good.demand_level / 50.0  # Normalize around 50
                supply_ratio = good.supply_level / 50.0
                
                # Price adjustment based on supply/demand
                price_multiplier = (demand_ratio / max(supply_ratio, 0.1))
                
                # Apply volatility
                volatility_adjustment = 1.0 + random.uniform(-good.volatility, good.volatility)
                
                # Calculate new price
                new_price = good.base_price * price_multiplier * volatility_adjustment * good.seasonal_modifier
                
                # Smooth price changes to prevent wild swings
                price_change_limit = 0.20  # Max 20% change per day
                max_change = good.current_price * price_change_limit
                
                if abs(new_price - good.current_price) > max_change:
                    if new_price > good.current_price:
                        new_price = good.current_price + max_change
                    else:
                        new_price = good.current_price - max_change
                
                good.current_price = max(0.1, new_price)  # Minimum price floor
    
    def _process_merchant_behaviors(self):
        """Simulate merchant NPC trading behaviors"""
        
        for merchant in self.merchant_npcs.values():
            
            # Merchants adjust their behavior based on market conditions
            home_market = self.markets.get(merchant.home_market)
            if not home_market:
                continue
            
            # Find goods in merchant's specialization
            relevant_goods = [
                good for good in home_market.trade_goods.values()
                if good.category == merchant.specialization
            ]
            
            for good in relevant_goods:
                
                # Buy when prices are low, sell when high
                price_ratio = good.current_price / good.base_price
                
                if price_ratio < 0.8 and merchant.capital > good.current_price * 10:
                    # Buy opportunity
                    quantity_to_buy = min(10, int(merchant.capital / good.current_price / 10))
                    merchant.inventory[good.name] = merchant.inventory.get(good.name, 0) + quantity_to_buy
                    merchant.capital -= good.current_price * quantity_to_buy
                    
                    # Reduce market supply
                    good.supply_level = max(0, good.supply_level - quantity_to_buy)
                
                elif price_ratio > 1.2 and merchant.inventory.get(good.name, 0) > 0:
                    # Sell opportunity
                    quantity_to_sell = min(merchant.inventory[good.name], 5)
                    merchant.capital += good.current_price * quantity_to_sell
                    merchant.inventory[good.name] -= quantity_to_sell
                    
                    # Increase market supply
                    good.supply_level = min(100, good.supply_level + quantity_to_sell)
    
    def _generate_random_event(self):
        """Generate a random market event"""
        
        event_templates = [
            {
                "name": "Crystal Mine Collapse",
                "description": "A major crystal mine has collapsed, disrupting production",
                "affected_goods": ["Pressure Crystals", "Wind Crystals"],
                "supply_impact": {"Pressure Crystals": -20, "Wind Crystals": -15},
                "severity": 7,
                "duration_days": 60
            },
            {
                "name": "Merchant Fleet Lost", 
                "description": "A merchant fleet carrying luxury goods has been lost at sea",
                "affected_goods": ["Sky Fruit", "Luxury Items"],
                "supply_impact": {"Sky Fruit": -15},
                "demand_impact": {"Sky Fruit": 10},
                "severity": 6,
                "duration_days": 30
            },
            {
                "name": "Shadow Conspiracy Raid",
                "description": "Shadow Conspiracy raids have disrupted black market operations",
                "affected_markets": ["Shadowhaven Black Market"],
                "affected_goods": ["Shadow Artifacts", "Trade Intelligence"],
                "supply_impact": {"Shadow Artifacts": -30, "Trade Intelligence": -20},
                "severity": 8,
                "duration_days": 45
            },
            {
                "name": "Deep Mother Cult Activity",
                "description": "Increased cult activity has made void essence more valuable",
                "affected_goods": ["Void Essence"],
                "demand_impact": {"Void Essence": 25},
                "severity": 9,
                "duration_days": 90
            }
        ]
        
        event_template = random.choice(event_templates)
        
        event = MarketEvent(
            event_id=f"event_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            name=event_template["name"],
            description=event_template["description"],
            affected_markets=event_template.get("affected_markets", []),
            affected_goods=event_template["affected_goods"],
            supply_impact=event_template.get("supply_impact", {}),
            demand_impact=event_template.get("demand_impact", {}),
            severity=event_template["severity"],
            duration_days=event_template["duration_days"],
            start_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        self.active_events.append(event)
        print(f"New market event: {event.name}")
    
    def _apply_active_events(self):
        """Apply effects of active market events"""
        
        events_to_remove = []
        
        for event in self.active_events:
            # Check if event has expired
            event_start = datetime.strptime(event.start_date, "%Y-%m-%d")
            if (datetime.now() - event_start).days > event.duration_days:
                events_to_remove.append(event)
                continue
            
            # Apply event effects
            for market_name, market in self.markets.items():
                if not event.affected_markets or market_name in event.affected_markets:
                    
                    for good_name in event.affected_goods:
                        if good_name in market.trade_goods:
                            good = market.trade_goods[good_name]
                            
                            # Apply supply impact (one-time adjustment)
                            if good_name in event.supply_impact:
                                supply_change = event.supply_impact[good_name] // event.duration_days
                                good.supply_level = max(0, min(100, good.supply_level + supply_change))
                            
                            # Apply demand impact
                            if good_name in event.demand_impact:
                                demand_change = event.demand_impact[good_name] // event.duration_days
                                good.demand_level = max(0, min(100, good.demand_level + demand_change))
        
        # Remove expired events
        for event in events_to_remove:
            self.active_events.remove(event)
    
    def _record_price_history(self):
        """Record current prices for historical tracking"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        for market_name, market in self.markets.items():
            for good_name, good in market.trade_goods.items():
                history_key = f"{market_name}:{good_name}"
                
                if history_key not in self.price_history:
                    self.price_history[history_key] = []
                
                self.price_history[history_key].append((today, good.current_price))
                
                # Keep only last 365 days
                if len(self.price_history[history_key]) > 365:
                    self.price_history[history_key] = self.price_history[history_key][-365:]
    
    def get_market_report(self, market_name: str) -> Dict[str, Any]:
        """Generate a comprehensive market report"""
        if market_name not in self.markets:
            return {}
        
        market = self.markets[market_name]
        
        # Calculate market statistics
        goods_data = []
        for good_name, good in market.trade_goods.items():
            price_change = ((good.current_price - good.base_price) / good.base_price) * 100
            
            goods_data.append({
                "name": good_name,
                "category": good.category.value,
                "current_price": round(good.current_price, 2),
                "base_price": round(good.base_price, 2),
                "price_change_percent": round(price_change, 1),
                "supply_level": good.supply_level,
                "demand_level": good.demand_level,
                "availability": "High" if good.supply_level > 70 else "Medium" if good.supply_level > 30 else "Low"
            })
        
        return {
            "market_name": market_name,
            "location": market.location,
            "world": market.world,
            "size": market.size,
            "condition": market.market_condition.value,
            "active_merchants": market.active_merchants,
            "security_level": market.security_level,
            "tax_rate": market.tax_rate * 100,  # Convert to percentage
            "goods": goods_data,
            "specializations": [spec.value for spec in market.specializations]
        }
    
    def create_economic_dashboard(self) -> str:
        """Create comprehensive economic dashboard"""
        dashboard = []
        
        dashboard.append("# Economic Market Dashboard")
        dashboard.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        
        # System overview
        dashboard.append("## Market Overview")
        dashboard.append(f"- Total Markets: {len(self.markets)}")
        dashboard.append(f"- Total Trade Goods: {len(self.trade_goods)}")
        dashboard.append(f"- Active Merchants: {len(self.merchant_npcs)}")
        dashboard.append(f"- Active Events: {len(self.active_events)}")
        dashboard.append("")
        
        # Market conditions
        dashboard.append("## Market Conditions")
        for market_name, market in self.markets.items():
            dashboard.append(f"### {market_name}")
            dashboard.append(f"- **Condition:** {market.market_condition.value.title()}")
            dashboard.append(f"- **Size:** {market.size}/10")
            dashboard.append(f"- **Security:** {market.security_level}/10")
            dashboard.append(f"- **Active Merchants:** {len(market.active_merchants)}")
            dashboard.append("")
        
        # Top price movers
        dashboard.append("## Price Movements")
        
        all_goods_changes = []
        for market_name, market in self.markets.items():
            for good_name, good in market.trade_goods.items():
                change_pct = ((good.current_price - good.base_price) / good.base_price) * 100
                all_goods_changes.append((f"{good_name} ({market_name})", change_pct, good.current_price))
        
        # Sort by absolute change
        all_goods_changes.sort(key=lambda x: abs(x[1]), reverse=True)
        
        dashboard.append("**Top Movers:**")
        for item, change_pct, price in all_goods_changes[:10]:
            direction = "📈" if change_pct > 0 else "📉"
            dashboard.append(f"- {direction} {item}: {change_pct:+.1f}% ({price:.1f} gp)")
        
        dashboard.append("")
        
        # Active events
        dashboard.append("## Active Market Events")
        if self.active_events:
            for event in self.active_events:
                days_remaining = event.duration_days - (datetime.now() - datetime.strptime(event.start_date, "%Y-%m-%d")).days
                dashboard.append(f"### {event.name}")
                dashboard.append(f"- **Description:** {event.description}")
                dashboard.append(f"- **Severity:** {event.severity}/10")
                dashboard.append(f"- **Days Remaining:** {max(0, days_remaining)}")
                dashboard.append(f"- **Affected Goods:** {', '.join(event.affected_goods)}")
                dashboard.append("")
        else:
            dashboard.append("*No active market events*")
        
        return "\n".join(dashboard)
    
    def save_economic_data(self):
        """Persist economic system data"""
        ensure_dirs()
        data_dir = os.path.join(self.vault_root, "09_Performance")
        os.makedirs(data_dir, exist_ok=True)
        
        # Save markets
        markets_data = {name: market.dict() for name, market in self.markets.items()}
        with open(os.path.join(data_dir, "markets.json"), "w") as f:
            json.dump(markets_data, f, indent=2, default=str)
        
        # Save trade goods
        goods_data = {name: good.dict() for name, good in self.trade_goods.items()}
        with open(os.path.join(data_dir, "trade_goods.json"), "w") as f:
            json.dump(goods_data, f, indent=2, default=str)
        
        # Save merchants
        merchants_data = {name: merchant.dict() for name, merchant in self.merchant_npcs.items()}
        with open(os.path.join(data_dir, "merchant_npcs.json"), "w") as f:
            json.dump(merchants_data, f, indent=2, default=str)
        
        # Save events
        events_data = [event.dict() for event in self.active_events]
        with open(os.path.join(data_dir, "market_events.json"), "w") as f:
            json.dump(events_data, f, indent=2, default=str)
        
        # Save price history
        with open(os.path.join(data_dir, "price_history.json"), "w") as f:
            json.dump(self.price_history, f, indent=2, default=str)
    
    def _load_persisted_data(self):
        """Load previously saved economic data"""
        data_dir = os.path.join(self.vault_root, "09_Performance")
        
        try:
            # Load saved data if it exists
            markets_file = os.path.join(data_dir, "markets.json")
            if os.path.exists(markets_file):
                with open(markets_file) as f:
                    markets_data = json.load(f)
                    # Convert back to Pydantic models (simplified for now)
                    pass
        except:
            pass  # Use initialized data

def main():
    """Main execution for economic market simulator"""
    print("Initializing Economic Market Simulator...")
    
    simulator = EconomicMarketSimulator()
    
    # Run a few days of simulation
    print("Running market simulation...")
    for day in range(7):  # Simulate a week
        print(f"Simulating day {day + 1}...")
        simulator.simulate_market_day()
    
    # Generate sample market reports
    print("\nGenerating market reports...")
    for market_name in list(simulator.markets.keys()):
        report = simulator.get_market_report(market_name)
        print(f"\n{market_name} Summary:")
        print(f"- Condition: {report['condition']}")
        print(f"- Goods Available: {len(report['goods'])}")
        
        # Show top 3 price movers
        goods = sorted(report['goods'], key=lambda x: abs(x['price_change_percent']), reverse=True)
        for good in goods[:3]:
            change = good['price_change_percent']
            direction = "↑" if change > 0 else "↓"
            print(f"  {direction} {good['name']}: {change:+.1f}%")
    
    # Save system state
    simulator.save_economic_data()
    
    # Create dashboard
    dashboard_content = simulator.create_economic_dashboard()
    
    # Write dashboard to vault
    dashboard_path = os.path.join(simulator.vault_root, "06_GM_Resources", "Economic_Market_Dashboard.md")
    write_file(dashboard_path, dashboard_content)
    
    print(f"\nEconomic Market Simulator initialized successfully!")
    print(f"Dashboard saved to: Economic_Market_Dashboard.md")
    print(f"System data saved to: 09_Performance/")

if __name__ == "__main__":
    main()