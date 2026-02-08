from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
import uuid


@dataclass
class BGMinion:
    """Battlegrounds minion on board or in hand"""
    card_id: str
    name: str
    attack: int
    health: int
    base_attack: int = 0
    base_health: int = 0
    tier: int = 1
    instance_id: str = field(default_factory=lambda: f"inst-{uuid.uuid4().hex[:8]}")
    slot: Optional[int] = None
    keywords: List[str] = field(default_factory=list)
    is_golden: bool = False
    has_divine_shield: bool = False
    has_reborn: bool = False
    reborn_used: bool = False
    has_taunt: bool = False
    has_windfury: bool = False
    has_poisonous: bool = False
    has_deathrattle: bool = False
    attacks_this_combat: int = 0
    
    def __post_init__(self):
        if self.base_attack == 0:
            self.base_attack = self.attack
        if self.base_health == 0:
            self.base_health = self.health
        self._parse_keywords()
    
    def _parse_keywords(self):
        kw = [k.lower() for k in self.keywords]
        self.has_divine_shield = "divine shield" in kw or self.has_divine_shield
        self.has_reborn = "reborn" in kw or self.has_reborn
        self.has_taunt = "taunt" in kw or self.has_taunt
        self.has_windfury = "windfury" in kw or self.has_windfury
        self.has_poisonous = "poisonous" in kw or self.has_poisonous
        self.has_deathrattle = "deathrattle" in kw or self.has_deathrattle
    
    def take_damage(self, amount: int) -> Dict[str, Any]:
        """Returns event data for damage taken"""
        if amount <= 0:
            return {"blocked": True, "amount": 0}
        
        if self.has_divine_shield:
            self.has_divine_shield = False
            return {"divine_shield_popped": True, "amount": 0}
        
        self.health -= amount
        return {"amount": amount, "new_health": self.health, "died": self.health <= 0}
    
    def is_dead(self) -> bool:
        return self.health <= 0
    
    def can_attack(self) -> bool:
        max_attacks = 2 if self.has_windfury else 1
        return self.attack > 0 and self.attacks_this_combat < max_attacks
    
    def buff(self, attack: int, health: int):
        self.attack += attack
        self.health += health
        self.base_attack += attack
        self.base_health += health
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "card_id": self.card_id,
            "name": self.name,
            "attack": self.attack,
            "health": self.health,
            "base_attack": self.base_attack,
            "base_health": self.base_health,
            "tier": self.tier,
            "slot": self.slot,
            "keywords": self.keywords,
            "is_golden": self.is_golden,
            "has_divine_shield": self.has_divine_shield,
            "reborn_used": self.reborn_used
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BGMinion':
        return cls(
            card_id=data.get("card_id", "unknown"),
            name=data.get("name", "Unknown"),
            attack=data.get("attack", 1),
            health=data.get("health", 1),
            base_attack=data.get("base_attack", data.get("attack", 1)),
            base_health=data.get("base_health", data.get("health", 1)),
            tier=data.get("tier", 1),
            instance_id=data.get("instance_id", f"inst-{uuid.uuid4().hex[:8]}"),
            slot=data.get("slot"),
            keywords=data.get("keywords", []),
            is_golden=data.get("is_golden", False),
            has_divine_shield=data.get("has_divine_shield", False),
            reborn_used=data.get("reborn_used", False)
        )
    
    def copy(self) -> 'BGMinion':
        return BGMinion.from_dict(self.to_dict())
