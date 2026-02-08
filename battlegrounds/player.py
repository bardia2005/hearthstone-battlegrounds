from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from .minion import BGMinion


@dataclass
class Hero:
    card_id: str
    name: str
    health: int = 40
    armor: int = 0
    hero_power_cost: int = 2
    hero_power_used: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "card_id": self.card_id,
            "name": self.name,
            "health": self.health,
            "armor": self.armor,
            "hero_power_cost": self.hero_power_cost,
            "hero_power_used": self.hero_power_used
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hero':
        if isinstance(data, str):
            return cls(card_id="default", name=data)
        return cls(
            card_id=data.get("card_id", "default"),
            name=data.get("name", "Unknown Hero"),
            health=data.get("health", 40),
            armor=data.get("armor", 0),
            hero_power_cost=data.get("hero_power_cost", 2),
            hero_power_used=data.get("hero_power_used", False)
        )


@dataclass
class ShopMinion:
    slot: int
    card_id: str
    name: str = "Unknown"
    attack: int = 1
    health: int = 1
    tier: int = 1
    sim_tier: int = 1
    cost: int = 3
    frozen: bool = False
    is_golden: bool = False
    keywords: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "slot": self.slot,
            "card_id": self.card_id,
            "name": self.name,
            "attack": self.attack,
            "health": self.health,
            "tier": self.tier,
            "sim_tier": self.sim_tier,
            "cost": self.cost,
            "frozen": self.frozen,
            "is_golden": self.is_golden,
            "keywords": self.keywords
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ShopMinion']:
        if data is None:
            return None
        return cls(
            slot=data.get("slot", 0),
            card_id=data.get("card_id", "unknown"),
            name=data.get("name", "Unknown"),
            attack=data.get("attack", 1),
            health=data.get("health", 1),
            tier=data.get("tier", 1),
            sim_tier=data.get("sim_tier", 1),
            cost=data.get("cost", 3),
            frozen=data.get("frozen", False),
            is_golden=data.get("is_golden", False),
            keywords=data.get("keywords", [])
        )


@dataclass
class BGPlayer:
    """Battlegrounds player state"""
    player_id: str
    hero: Hero
    health: int = 40
    armor: int = 0
    gold: int = 3
    max_gold: int = 3
    tavern_tier: int = 1
    upgrade_cost: int = 5
    refresh_cost: int = 1
    timer_ms: int = 30000
    board: List[BGMinion] = field(default_factory=list)
    hand: List[BGMinion] = field(default_factory=list)
    shop: List[Optional[ShopMinion]] = field(default_factory=list)
    shop_frozen: bool = False
    ready: bool = False
    
    def __post_init__(self):
        if isinstance(self.hero, dict):
            self.hero = Hero.from_dict(self.hero)
        elif isinstance(self.hero, str):
            self.hero = Hero(card_id="default", name=self.hero)
    
    def get_board_minion(self, slot: int) -> Optional[BGMinion]:
        for m in self.board:
            if m.slot == slot:
                return m
        return None
    
    def get_board_minion_by_id(self, instance_id: str) -> Optional[BGMinion]:
        for m in self.board:
            if m.instance_id == instance_id:
                return m
        return None
    
    def add_to_board(self, minion: BGMinion, slot: Optional[int] = None) -> bool:
        if len(self.board) >= 7:
            return False
        
        if slot is None:
            used_slots = {m.slot for m in self.board}
            for i in range(7):
                if i not in used_slots:
                    slot = i
                    break
        
        minion.slot = slot
        self.board.append(minion)
        self.board.sort(key=lambda m: m.slot or 0)
        return True
    
    def remove_from_board(self, instance_id: str) -> Optional[BGMinion]:
        for i, m in enumerate(self.board):
            if m.instance_id == instance_id:
                return self.board.pop(i)
        return None
    
    def add_to_hand(self, minion: BGMinion) -> bool:
        if len(self.hand) >= 10:
            return False
        self.hand.append(minion)
        return True
    
    def buy_minion(self, shop_slot: int) -> Optional[BGMinion]:
        if self.gold < 3:
            return None
        
        shop_minion = None
        for sm in self.shop:
            if sm and sm.slot == shop_slot:
                shop_minion = sm
                break
        
        if not shop_minion:
            return None
        
        self.gold -= shop_minion.cost
        self.shop = [s for s in self.shop if s != shop_minion]
        
        minion = BGMinion(
            card_id=shop_minion.card_id,
            name=shop_minion.name,
            attack=shop_minion.attack,
            health=shop_minion.health,
            tier=shop_minion.tier,
            keywords=shop_minion.keywords,
            is_golden=shop_minion.is_golden
        )
        
        if not self.add_to_hand(minion):
            return None
        
        return minion
    
    def sell_minion(self, instance_id: str) -> bool:
        minion = self.remove_from_board(instance_id)
        if minion:
            self.gold += 1
            return True
        return False
    
    def take_damage(self, amount: int) -> int:
        if self.armor > 0:
            absorbed = min(self.armor, amount)
            self.armor -= absorbed
            amount -= absorbed
        self.health -= amount
        self.hero.health = self.health
        return amount
    
    def is_dead(self) -> bool:
        return self.health <= 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "player_id": self.player_id,
            "hero": self.hero.to_dict() if self.hero else None,
            "health": self.health,
            "armor": self.armor,
            "gold": self.gold,
            "max_gold": self.max_gold,
            "tavern_tier": self.tavern_tier,
            "upgrade_cost": self.upgrade_cost,
            "refresh_cost": self.refresh_cost,
            "timer_ms": self.timer_ms,
            "board": [m.to_dict() for m in self.board],
            "hand": [m.to_dict() for m in self.hand],
            "shop": [s.to_dict() if s else None for s in self.shop],
            "flags": {"shop_frozen": self.shop_frozen, "ready": self.ready}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BGPlayer':
        hero_data = data.get("hero", "Unknown")
        hero = Hero.from_dict(hero_data) if isinstance(hero_data, dict) else Hero(card_id="default", name=str(hero_data))
        
        flags = data.get("flags", {})
        
        player = cls(
            player_id=data.get("player_id", "unknown"),
            hero=hero,
            health=data.get("health", hero.health),
            armor=data.get("armor", hero.armor),
            gold=data.get("gold", 3),
            max_gold=data.get("max_gold", data.get("gold", 3)),
            tavern_tier=data.get("tavern_tier", 1),
            upgrade_cost=data.get("upgrade_cost", 5),
            refresh_cost=data.get("refresh_cost", 1),
            timer_ms=data.get("timer_ms", 30000),
            shop_frozen=flags.get("shop_frozen", False),
            ready=flags.get("ready", False)
        )
        
        # Parse board
        for m_data in data.get("board", []):
            minion = BGMinion.from_dict(m_data)
            player.board.append(minion)
        
        # Parse hand
        for m_data in data.get("hand", []):
            minion = BGMinion.from_dict(m_data)
            player.hand.append(minion)
        
        # Parse shop
        for s_data in data.get("shop", []):
            shop_minion = ShopMinion.from_dict(s_data)
            player.shop.append(shop_minion)
        
        return player
