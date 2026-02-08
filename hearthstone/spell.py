from .card import Card
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from .player import Player
    from .game import Game


class SpellCard(Card):
    def __init__(self, name: str, mana_cost: int, effect: Callable, 
                 description: str = "", rarity: str = "Common",
                 requires_target: bool = False, target_type: str = "any"):
        super().__init__(name, mana_cost, description, rarity)
        self.effect = effect
        self.requires_target = requires_target
        self.target_type = target_type  # "any", "minion", "enemy_minion", "friendly_minion", "hero"

    def play(self, owner: 'Player', game: 'Game', target=None) -> bool:
        if self.requires_target and target is None:
            game.add_log("This spell requires a target!")
            return False
        
        owner.mana -= self.mana_cost
        self.effect(owner, game, target)
        game.add_log(f"{owner.name} casts {self.name}")
        return True

    def copy(self) -> 'SpellCard':
        return SpellCard(
            self.name, self.mana_cost, self.effect,
            self.description, self.rarity, self.requires_target, self.target_type
        )

    def __repr__(self):
        return f"{self.name} ({self.mana_cost}) - Spell: {self.description}"


class WeaponCard(Card):
    def __init__(self, name: str, mana_cost: int, attack: int, durability: int,
                 description: str = "", rarity: str = "Common",
                 battlecry: Optional[Callable] = None, deathrattle: Optional[Callable] = None):
        super().__init__(name, mana_cost, description, rarity)
        self.attack = attack
        self.durability = durability
        self.battlecry = battlecry
        self.deathrattle = deathrattle

    def play(self, owner: 'Player', game: 'Game', target=None) -> bool:
        # Destroy existing weapon
        if owner.weapon:
            if owner.weapon.deathrattle:
                owner.weapon.deathrattle(owner, game)
        
        owner.weapon = Weapon(self.name, self.attack, self.durability, self.deathrattle)
        owner.mana -= self.mana_cost
        
        game.add_log(f"{owner.name} equips {self.name}")
        
        if self.battlecry:
            self.battlecry(owner, game, target)
        
        return True

    def copy(self) -> 'WeaponCard':
        return WeaponCard(
            self.name, self.mana_cost, self.attack, self.durability,
            self.description, self.rarity, self.battlecry, self.deathrattle
        )


class Weapon:
    def __init__(self, name: str, attack: int, durability: int, deathrattle=None):
        self.name = name
        self.attack = attack
        self.durability = durability
        self.deathrattle = deathrattle

    def use(self):
        self.durability -= 1
        return self.durability <= 0
