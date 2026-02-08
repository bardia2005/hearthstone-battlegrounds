from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Callable, List

if TYPE_CHECKING:
    from .player import Player
    from .game import Game


class Card(ABC):
    def __init__(self, name: str, mana_cost: int, description: str = "", rarity: str = "Common"):
        self.name = name
        self.mana_cost = mana_cost
        self.description = description
        self.rarity = rarity  # Common, Rare, Epic, Legendary

    @abstractmethod
    def play(self, owner: 'Player', game: 'Game', target=None) -> bool:
        pass

    def can_play(self, owner: 'Player') -> bool:
        return owner.mana >= self.mana_cost

    def __repr__(self):
        return f"{self.name} ({self.mana_cost} mana)"


class MinionCard(Card):
    def __init__(self, name: str, mana_cost: int, attack: int, health: int, 
                 description: str = "", rarity: str = "Common",
                 taunt: bool = False, charge: bool = False, divine_shield: bool = False,
                 windfury: bool = False, stealth: bool = False, poisonous: bool = False,
                 lifesteal: bool = False, battlecry: Optional[Callable] = None, 
                 deathrattle: Optional[Callable] = None):
        super().__init__(name, mana_cost, description, rarity)
        self.attack = attack
        self.health = health
        self.taunt = taunt
        self.charge = charge
        self.divine_shield = divine_shield
        self.windfury = windfury
        self.stealth = stealth
        self.poisonous = poisonous
        self.lifesteal = lifesteal
        self.battlecry = battlecry
        self.deathrattle = deathrattle

    def play(self, owner: 'Player', game: 'Game', target=None) -> bool:
        from .minion import Minion
        if len(owner.board) >= 7:
            game.add_log(f"Board is full!")
            return False
        
        minion = Minion(
            self.name, self.attack, self.health,
            taunt=self.taunt, charge=self.charge, divine_shield=self.divine_shield,
            windfury=self.windfury, stealth=self.stealth, poisonous=self.poisonous,
            lifesteal=self.lifesteal, deathrattle=self.deathrattle
        )
        owner.board.append(minion)
        owner.mana -= self.mana_cost
        
        game.add_log(f"{owner.name} plays {self.name}")
        
        if self.battlecry:
            self.battlecry(owner, game, target)
        
        return True

    def copy(self) -> 'MinionCard':
        return MinionCard(
            self.name, self.mana_cost, self.attack, self.health,
            self.description, self.rarity, self.taunt, self.charge,
            self.divine_shield, self.windfury, self.stealth, self.poisonous,
            self.lifesteal, self.battlecry, self.deathrattle
        )

    def __repr__(self):
        attrs = []
        if self.taunt: attrs.append("Taunt")
        if self.charge: attrs.append("Charge")
        if self.divine_shield: attrs.append("Divine Shield")
        if self.windfury: attrs.append("Windfury")
        attr_str = f" [{', '.join(attrs)}]" if attrs else ""
        return f"{self.name} ({self.mana_cost}) - {self.attack}/{self.health}{attr_str}"
